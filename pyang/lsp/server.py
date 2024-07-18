"""pyang LSP Server"""

from __future__ import absolute_import
import optparse  #pylint: disable=deprecated-module
import os
import tempfile
from typing import Any, List, Union
import importlib

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.workspace import TextDocument
from pygls.uris import from_fs_path, to_fs_path

from pyang import error, grammar
from pyang import yang_parser
from pyang import context
from pyang import plugin
from pyang import syntax
from pyang import statements
from pyang.plugins import lint
from pyang.statements import Statement, ModSubmodStatement
from pyang.translators import yang
from pyang.lsp import code_lens, folding_range, glue, completion, helper, inline_value, maps
from pyang.lsp.rfcref import rfcref_stmt_map, rfcref_type_map

ext_deps = ['pygls']
def try_import_deps():
    """Raises `ModuleNotFoundError` if external module dependencies are missing"""
    for dep in ext_deps:
        importlib.import_module(dep)

SERVER_NAME = "pyang"
SERVER_VERSION = "v0.1"

SERVER_MODE_IO = "io"
SERVER_MODE_TCP = "tcp"
SERVER_MODE_WS = "ws"
supported_modes = [
    SERVER_MODE_IO,
    SERVER_MODE_TCP,
    SERVER_MODE_WS,
]
default_mode = SERVER_MODE_IO
default_host = "127.0.0.1"
default_port = 2087

# Default Formatting parameters
default_line_length = 80
default_canonical_order = False
default_remove_unused_imports = False
default_remove_comments = False

class PyangLanguageServer(LanguageServer):
    def __init__(self):
        self.ctx : context.Context
        self.yangfmt : yang.YANGPlugin
        self.modules : dict[str, ModSubmodStatement] = {}
        self.doc_symbols : dict[str, List[lsp.DocumentSymbol] | None] = {}
        self.diagnostics : dict[str, List[lsp.Diagnostic] | None] = {}
        super().__init__(
            name=SERVER_NAME,
            version=SERVER_VERSION,
            text_document_sync_kind=lsp.TextDocumentSyncKind.Full
        )

pyangls = PyangLanguageServer()


def add_opts(optparser: optparse.OptionParser):
    optlist = [
        # use capitalized versions of std options help and version
        optparse.make_option("--lsp-config-schema",
                             dest="lsp_config_schema",
                             action="store_true",
                             help="Generate JSON schema for supported errors " \
                                 "and warnings as per the plugins and option " \
                                 "codes and exit."),
        optparse.make_option("--lsp-mode",
                             dest="pyangls_mode",
                             default=default_mode,
                             metavar="LSP_MODE",
                             help="Provide LSP Service in this mode" \
                             "Supported LSP server modes are: " +
                             ', '.join(supported_modes)),
        optparse.make_option("--lsp-host",
                             dest="pyangls_host",
                             default=default_host,
                             metavar="LSP_HOST",
                             help="Bind LSP Server to this address"),
        optparse.make_option("--lsp-port",
                             dest="pyangls_port",
                             type="int",
                             default=default_port,
                             metavar="LSP_PORT",
                             help="Bind LSP Server to this port"),
        ]
    g = optparser.add_option_group("LSP Server specific options")
    g.add_options(optlist)

def gen_config_schema():
    return


def start_server(optargs, ctx: context.Context, fmts: dict):
    pyangls.ctx = ctx
    pyangls.yangfmt = fmts['yang']
    if optargs.pyangls_mode == SERVER_MODE_TCP:
        pyangls.start_tcp(optargs.pyangls_host, optargs.pyangls_port)
    elif optargs.pyangls_mode == SERVER_MODE_WS:
        pyangls.start_ws(optargs.pyangls_host, optargs.pyangls_port)
    else:
        pyangls.start_io()


def _delete_from_ctx(text_doc: TextDocument):
    if not pyangls.modules:
        return
    try:
        module = pyangls.modules[text_doc.uri]
    except KeyError:
        return
    pyangls.ctx.del_module(module)
    del pyangls.modules[text_doc.uri]


def _add_to_ctx(text_doc: TextDocument):
    assert text_doc.filename
    m = syntax.re_filename.search(text_doc.filename)
    if m is not None:
        name, rev, in_format = m.groups()
        assert in_format == 'yang'
        module = pyangls.ctx.add_module(text_doc.path, text_doc.source,
                                        in_format, name, rev,
                                        expect_failure_error=False,
                                        primary_module=True)
    else:
        module = pyangls.ctx.add_module(text_doc.path, text_doc.source,
                                        primary_module=True)
    if module:
        pyangls.modules[text_doc.uri] = module
    return module


def _update_ctx_module(text_doc: TextDocument):
    _delete_from_ctx(text_doc)
    return _add_to_ctx(text_doc)


def _update_ctx_modules():
    for text_doc in pyangls.workspace.documents.values():
        _delete_from_ctx(text_doc)
    for text_doc in pyangls.workspace.documents.values():
        _add_to_ctx(text_doc)


def _clear_stmt_validation(stmt: Statement):
    stmt.i_is_validated = False
    substmt : Statement
    for substmt in stmt.substmts:
        _clear_stmt_validation(substmt)


def _clear_ctx_validation():
    pyangls.doc_symbols = {}
    pyangls.diagnostics = {}
    # pyangls.ctx.internal_reset()
    pyangls.ctx.errors = []
    module : Statement
    for module in pyangls.ctx.modules.values():
        module.internal_reset()
        # _clear_stmt_validation(module)


def _validate_ctx_modules():
    # ls.show_message_log("Validating YANG...")
    modules = helper._get_ctx_modules(pyangls.ctx)

    p : plugin.PyangPlugin

    for p in plugin.plugins:
        p.pre_validate_ctx(pyangls.ctx, modules)

    pyangls.ctx.validate()

    for _m in modules:
        _m.prune()

    for p in plugin.plugins:
        p.post_validate_ctx(pyangls.ctx, modules)


def _build_doc_diagnostics(ref: str) -> List[lsp.Diagnostic]:
    """Builds lsp diagnostics from pyang context"""
    diagnostics = []
    # TODO: revisit sorting. VS code seems to prefer ordering on line numbers
    pyangls.ctx.errors.sort(key=lambda e: (e[0].ref, e[0].line), reverse=True)
    for epos, etag, eargs in pyangls.ctx.errors:
        if epos.ref != ref:
            continue
        msg = error.err_to_str(etag, eargs)

        def epos_to_lsp_range(etag: str, epos: error.Position) -> lsp.Range:
            start_line = epos.arg_sline
            start_col = epos.arg_schar
            end_line = epos.arg_eline
            end_col = epos.arg_echar
            if etag == 'LONG_LINE' and pyangls.ctx.max_line_len is not None:
                start_line = epos.line - 1
                start_col = pyangls.ctx.max_line_len
                end_line = epos.line
                end_col = 0
            elif etag == 'LONG_IDENTIFIER' and pyangls.ctx.max_identifier_len is not None:
                start_col = epos.arg_schar + pyangls.ctx.max_identifier_len
            elif 'KEYWORD' in etag:
                start_line = epos.kwd_sline
                start_col = epos.kwd_schar
                end_line = epos.kwd_eline
                end_col = epos.kwd_echar
            return lsp.Range(
                start=lsp.Position(line=start_line, character=start_col),
                end=lsp.Position(line=end_line, character=end_col),
            )

        def line_to_lsp_range(etag: str, line: int) -> lsp.Range:
            # pyang just stores line context, not keyword/argument context
            start_line = line - 1
            if etag == 'LONG_LINE' and pyangls.ctx.max_line_len is not None:
                start_col = pyangls.ctx.max_line_len
            else:
                start_col = 0
            end_line = line
            end_col = 0
            return lsp.Range(
                start=lsp.Position(line=start_line, character=start_col),
                end=lsp.Position(line=end_line, character=end_col),
            )

        def level_to_lsp_severity(level) -> lsp.DiagnosticSeverity:
            if level == 1 or level == 2:
                return lsp.DiagnosticSeverity.Error
            elif level == 3:
                return lsp.DiagnosticSeverity.Warning
            elif level == 4:
                return lsp.DiagnosticSeverity.Information
            else:
                return lsp.DiagnosticSeverity.Hint

        diag_tags=[]
        rel_info=[]
        unused_etags = [
            'UNUSED_IMPORT',
            'UNUSED_TYPEDEF',
            'UNUSED_GROUPING',
        ]
        duplicate_1_etags = [
            'DUPLICATE_ENUM_NAME',
            'DUPLICATE_ENUM_VALUE',
            'DUPLICATE_BIT_POSITION',
            'DUPLICATE_CHILD_NAME',
        ]
        if etag in unused_etags:
            diag_tags.append(lsp.DiagnosticTag.Unnecessary)
        elif etag in duplicate_1_etags:
            if etag == 'DUPLICATE_ENUM_NAME':
                dup_arg = 1
                dup_msg = 'Original Enumeration'
            elif etag == 'DUPLICATE_ENUM_VALUE':
                dup_arg = 1
                dup_msg = 'Original Enumeration with Value'
            elif etag == 'DUPLICATE_BIT_POSITION':
                dup_arg = 1
                dup_msg = 'Original Bit Position'
            elif etag == 'DUPLICATE_CHILD_NAME':
                dup_arg = 3
                dup_msg = 'Original Child'
            dup_uri = from_fs_path(eargs[dup_arg].ref)
            dup_range = line_to_lsp_range(etag, eargs[dup_arg].line)
            if dup_uri:
                dup_loc = lsp.Location(uri=dup_uri, range=dup_range)
                rel_info.append(lsp.DiagnosticRelatedInformation(location=dup_loc,
                                                             message=dup_msg))
        elif etag == 'DUPLICATE_NAMESPACE':
            # TODO: handle
            pass

        code_desc = None
        (_severity, _fmt, uri) = error.error_codes[etag]
        if uri:
            code_desc = lsp.CodeDescription(href=uri)
        else:
            if etag == 'LINT_MISSING_REQUIRED_SUBSTMT':
                kwd = eargs[1]
                (_stmts, _rfc_sec, uri) = lint._required_substatements[kwd]  #pylint: disable=protected-access
                code_desc = lsp.CodeDescription(href=uri)
            elif etag == 'LINT_MISSING_RECOMMENDED_SUBSTMT':
                kwd = eargs[1]
                (_stmts, _rfc_sec, uri) = lint._recommended_substatements[kwd]  #pylint: disable=protected-access
                code_desc = lsp.CodeDescription(href=uri)

        d = lsp.Diagnostic(
            range=epos_to_lsp_range(etag, epos),
            message=msg,
            severity=level_to_lsp_severity(error.err_level(etag)),
            tags=diag_tags,
            related_information=rel_info,
            code=etag,
            code_description=code_desc,
            source=SERVER_NAME,
        )

        diagnostics.append(d)

    return diagnostics


def _publish_doc_diagnostics(text_doc: TextDocument,
                             diagnostics: List[lsp.Diagnostic] | None = None):
    if not pyangls.client_capabilities.text_document:
        return
    if not pyangls.client_capabilities.text_document.publish_diagnostics:
        return
    if not diagnostics:
        diagnostics = _build_doc_diagnostics(text_doc.path)
    pyangls.publish_diagnostics(text_doc.uri, diagnostics)
    pyangls.diagnostics[text_doc.uri] = diagnostics


def _publish_workspace_diagnostics():
    for text_doc in pyangls.workspace.text_documents.values():
        _publish_doc_diagnostics(text_doc)


def _get_folder_yang_uris(folder_uri) -> List[str]:
    """Recursively find all .yang files in the given folder."""
    folder = to_fs_path(folder_uri)
    assert folder
    yang_files = []
    for root, _, files in os.walk(folder):
        file : str
        for file in files:
            if file.endswith(".yang") and not file.startswith('.#'):
                yang_files.append(from_fs_path(os.path.join(root, file)))
    return yang_files


def _have_parser_errors() -> bool:
    for _, etag, _ in pyangls.ctx.errors:
        if etag in yang_parser.errors:
            return True
    return False


def _format_yang(source: str, opts, module) -> str:
    if opts.insert_spaces is False:
        pyangls.log_trace("insert_spaces is currently restricted to True")
    if opts.tab_size:
        pyangls.ctx.opts.yang_indent_size = opts.tab_size # type: ignore
    if opts.trim_trailing_whitespace is False:
        pyangls.log_trace("trim_trailing_whitespace is currently restricted to True")
    if opts.trim_final_newlines is False:
        pyangls.log_trace("trim_final_newlines is currently restricted to True")
    pyangls.ctx.opts.yang_canonical = default_canonical_order # type: ignore
    pyangls.ctx.opts.yang_line_length = default_line_length # type: ignore
    pyangls.ctx.opts.yang_remove_unused_imports = default_remove_unused_imports # type: ignore
    pyangls.ctx.opts.yang_remove_comments = default_remove_comments # type: ignore

    pyangls.yangfmt.setup_fmt(pyangls.ctx)
    tmpfd = tempfile.TemporaryFile(mode="w+", encoding="utf-8")

    pyangls.yangfmt.emit(pyangls.ctx, [module], tmpfd)

    tmpfd.seek(0)
    fmt_text = tmpfd.read()
    tmpfd.close()

    # pyang only supports unix file endings and inserts a final one if missing
    if not opts.insert_final_newline and not source.endswith('\n'):
        fmt_text.rstrip('\n')

    return fmt_text


def _process_workspace_configuration(_scope: str | None, _config: List[Any]):
    pass


def _stmt_to_lsp_symbol_kind(stmt: Statement) -> lsp.SymbolKind:
    if stmt.arg is None:
        return lsp.SymbolKind.Property
    match stmt.keyword:
        case str():
            match stmt.keyword:
                case 'leaf':
                    def get_base_type(stmt: statements.Statement):
                        stmt_type = stmt.search_one('type')
                        if stmt_type:
                            if stmt_type.arg in maps.type_lsp_kind:
                                return stmt_type.arg
                            typedef = helper.referenced_stmt_from_stmt_arg(pyangls.ctx, stmt_type)
                            if typedef:
                                return get_base_type(typedef)
                        return None

                    def leaf_symbol_kind(
                        leaf: statements.LeafLeaflistStatement
                    ) -> lsp.SymbolKind:
                        stmt_type = get_base_type(leaf)
                        if not stmt_type:
                            return lsp.SymbolKind.Null
                        if stmt_type == 'leafref':
                            if hasattr(leaf, 'i_leafref_expanded') and leaf.i_leafref_expanded:
                                (ref_stmt, _) = leaf.i_leafref_ptr
                            else:
                                # TODO: check why i_leafref is not always populated
                                if not hasattr(leaf, 'i_leafref'):
                                    return lsp.SymbolKind.Null
                                # TODO: check why i_leafref_ptr is not always populated
                                if not leaf.i_leafref or not hasattr(leaf.i_leafref, 'i_target_node'):
                                    return lsp.SymbolKind.Null
                                ref_stmt = leaf.i_leafref.i_target_node
                            if not ref_stmt:
                                return lsp.SymbolKind.Null
                            return leaf_symbol_kind(ref_stmt) # type: ignore
                        try:
                            return maps.type_lsp_kind[stmt_type]['symbol']
                        except KeyError:
                            return lsp.SymbolKind.Field

                    return leaf_symbol_kind(stmt) # type: ignore

                case _:
                    try:
                        return maps.keyword_lsp_kind[stmt.keyword]['symbol']
                    except KeyError:
                        return lsp.SymbolKind.Null
        case (str(), str()):
            return lsp.SymbolKind.Null
        case _:
            raise TypeError


def _build_doc_stmt_symbols(
    stmt: Statement,
    parent_deprecated: bool = False,
    feature_cond: bool = False,
    when_cond: bool = False,
    augmented_pos: error.Position | None = None,
) -> lsp.DocumentSymbol | None:
    if stmt.keyword in ['description', 'reference', 'type', 'status', 'contact',
                        'mandatory', 'revision', 'namespace', 'prefix', 'config',
                        'import', 'yang-version', 'presence', 'default', 'uses',
                        '_comment', 'if-feature', 'when', 'must', 'organization',
                        'units', 'key', 'max-elements', 'min-elements', 'base',
                        'augment', 'argument', 'ordered-by', 'deviation', 'unique']:
        return None
    if stmt.arg is None:
        return None

    symbol_tags = None
    symbol_children = []
    symbol_kind = _stmt_to_lsp_symbol_kind(stmt)


    deprecated = False
    stmt_status: Statement | None = stmt.search_one('status')
    if stmt_status and stmt_status.arg in ['deprecated', 'obsolete'] or parent_deprecated:
        symbol_tags = [lsp.SymbolTag.Deprecated]
        deprecated = True

    # Since pyang expansions have already been done, and augmentation by nature
    # come from external documents, augmented symbols need to be resolved to the
    # root augmented symbol and symbol selection.
    # TODO: Consider augmentations over augmentations
    augmented = False
    symbol_select_range = None
    if augmented_pos:
        augmented = True
        symbol_range = glue.stmt_lsp_range(augmented_pos)
        symbol_select_range = glue.arg_lsp_selection_range(augmented_pos)
    elif hasattr(stmt, 'i_augment') and stmt.i_augment: # type: ignore
        augmented = True
        augmented_pos = stmt.parent.pos
        symbol_range = glue.stmt_lsp_range(stmt.parent.pos)
        symbol_select_range = glue.arg_lsp_selection_range(stmt.parent.pos)
    else:
        symbol_range = glue.stmt_lsp_range(stmt.pos)

    deviated = False
    # TODO: Mark deviated statements

    if stmt.arg:
        if stmt.parent and stmt.parent.keyword in ['rpc', 'action']:
            symbol_detail = ''
            symbol_name = stmt.keyword
            if not symbol_select_range:
                symbol_select_range = glue.kwd_lsp_selection_range(stmt.pos)
        else:
            extra_detail = ' '
            extra_detail += '['
            if feature_cond or stmt.search('if-feature'):
                extra_detail += 'f'
                feature_cond = True
            if when_cond or stmt.search('when'):
                extra_detail += 'w'
                when_cond = True
            extra_detail += ']'
            extra_detail += ' '
            for (kwd, _) in grammar.data_def_stmts:
                if stmt.keyword == kwd:
                    extra_detail += '('
                    if hasattr(stmt, 'i_is_key') and stmt.i_is_key: # type: ignore
                        extra_detail += 'K'
                    if hasattr(stmt, 'i_uniques') and stmt.i_uniques:
                        extra_detail += 'U'
                    if hasattr(stmt, 'i_config') and stmt.i_config:
                        extra_detail += 'C'
                    if ((m := stmt.search_one('mandatory')) and m.arg == 'true') or \
                        ((m := stmt.search_one('min-elements')) and int(m.arg) >= 1):
                        extra_detail += 'M'
                    if stmt.search_one('presence'):
                        extra_detail += 'P'
                    if hasattr(stmt, 'i_default') and stmt.i_default: # type: ignore
                        extra_detail += 'D'
                    extra_detail += ')'
                    extra_detail += ' '
                    if (t := stmt.search_one('type')) and t.arg == 'leafref':
                        extra_detail += '*'
                    if hasattr(stmt, 'i_uses') and stmt.i_uses:
                        extra_detail += '@'
                    if augmented:
                        extra_detail += 'Σ'
                    if deviated:
                        extra_detail += 'Δ'
                    break
            if isinstance(stmt.keyword, str):
                symbol_detail = stmt.keyword
            else:
                (prefix, keyword) = stmt.keyword
                if prefix == stmt.top.arg:
                    symbol_detail = keyword
                else:
                    symbol_detail = prefix + ':' + keyword
            symbol_detail += extra_detail
            symbol_name = stmt.arg
            if not symbol_select_range:
                symbol_select_range = glue.arg_lsp_selection_range(stmt.pos)
    else:
        # Handling extension statements
        symbol_detail = 'extension'
        assert stmt.keyword
        if isinstance(stmt.keyword, str):
            symbol_name = stmt.keyword
        else:
            (prefix, keyword) = stmt.keyword
            if prefix == stmt.top.arg:
                symbol_name = keyword
            else:
                symbol_name = prefix + ':' + keyword
        if not symbol_select_range:
            symbol_select_range = glue.kwd_lsp_selection_range(stmt.pos)

    # Since pyang expansions have already been done, document external groupings
    # need to be resolved to the uses statement symbol and symbol selection.
    # For consistency, even document local groupings are handled the same way.
    if not augmented and hasattr(stmt, 'i_uses') and stmt.i_uses and stmt.i_uses_pos:
        # TODO: Consider keeping direct references to file local groupings
        symbol_range = glue.stmt_lsp_range(stmt.i_uses_pos)
        symbol_select_range = glue.arg_lsp_selection_range(stmt.i_uses_pos)

    if hasattr(stmt, 'i_children'):
        for s in stmt.i_children:
            # Do not add hanging input/output entries
            if s.keyword in ['input', 'output'] and not s.i_children:
                continue

            symbols = _build_doc_stmt_symbols(s, deprecated,
                                              feature_cond,
                                              when_cond,
                                              augmented_pos)
            if symbols:
                symbol_children.append(symbols)

    if stmt.substmts:
        s: Statement
        for s in stmt.substmts:
            # Do not duplicate i_children added above
            if hasattr(stmt, 'i_children'):
                if s in stmt.i_children:
                    continue
            if s.parent.keyword == 'case':
                continue

            symbols = _build_doc_stmt_symbols(s, deprecated,
                                              feature_cond,
                                              when_cond,
                                              augmented_pos)
            if symbols:
                symbol_children.append(symbols)

    return lsp.DocumentSymbol(
        name=symbol_name,
        kind=symbol_kind,
        range=symbol_range,
        selection_range=symbol_select_range,
        detail=symbol_detail,
        tags=symbol_tags,
        children=symbol_children,
    )


def _build_ws_stmt_symbols(
    stmt: Statement,
    doc_uri: str,
    query: str,
    container: str | None,
) -> List[lsp.WorkspaceSymbol]:
    if stmt.keyword in ['description', 'reference', 'type', 'config', 'status',
                        'mandatory', 'contact', 'organization', 'revision',
                        'import', 'yang-version', 'presence', 'base', 'default',
                        'namespace', 'if-feature', 'case', 'choice', 'prefix',
                        'deviation', 'augment', 'input', 'output', 'uses',
                        '_comment']:
        return []

    ctx_symbols = []
    container_name = None
    if stmt.arg:
        if isinstance(stmt.arg, str):
            symbol_name = stmt.arg
            container_name = stmt.arg
        else:
            (prefix, symbol_name) = stmt.arg
            container_name = prefix + ':' + symbol_name
            stmt_module: Statement = stmt.top
            if prefix != stmt_module.arg:
                return ctx_symbols
            if stmt_module.search_one('prefix', prefix) is None:
                # not own module prefix, skip for now
                # TODO: handle
                return ctx_symbols
        if not symbol_name.startswith(query):
            return ctx_symbols

    if stmt.substmts:
        for s in stmt.substmts:
            symbols = _build_ws_stmt_symbols(s, doc_uri, query, container_name)
            if symbols:
                ctx_symbols += symbols
    if hasattr(stmt, 'i_children'):
        for s in stmt.i_children:
            symbols = _build_ws_stmt_symbols(s, doc_uri, query, container_name)
            if symbols:
                ctx_symbols += symbols

    if stmt.arg:
        if isinstance(stmt.arg, str):
            symbol_name = stmt.arg
            container_name = stmt.arg
        else:
            (prefix, symbol_name) = stmt.arg
            container_name = prefix + ':' + symbol_name
            stmt_module: Statement = stmt.top
            if prefix != stmt_module.arg:
                return ctx_symbols
            if stmt_module.search_one('prefix', prefix) is None:
                # not own module prefix, skip for now
                # TODO: handle
                return ctx_symbols
        if not symbol_name.startswith(query):
            return ctx_symbols
    else:
        return ctx_symbols

    symbol_location = lsp.Location(
        uri=doc_uri,
        range=glue.arg_lsp_selection_range(stmt.pos),
    )
    symbol_tags = None
    symbol_kind = _stmt_to_lsp_symbol_kind(stmt)

    stmt_status: Statement | None = stmt.search_one('status')
    if stmt_status and stmt_status.arg in ['deprecated', 'obsolete']:
        symbol_tags = [lsp.SymbolTag.Deprecated]

    stmt_symbol = lsp.WorkspaceSymbol(
        location=symbol_location,
        name=symbol_name,
        kind=symbol_kind,
        data=None,
        tags=symbol_tags,
        container_name=container,
    )
    ctx_symbols.append(stmt_symbol)

    return ctx_symbols


def stmts_to_lsp_locations(
    stmts: List[statements.Statement]
) -> List[lsp.Location]:
    locs: List[lsp.Location] = []
    for stmt in stmts:
        stmt_uri = from_fs_path(stmt.pos.ref)
        if not stmt_uri:
            continue
        loc = lsp.Location(
            uri=stmt_uri,
            range=glue.arg_lsp_selection_range(stmt.pos)
        )
        locs.append(loc)
    return locs


################################################################################
#-------------------------------------------------------------------------------
# LSP Lifecycle Messages
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.INITIALIZED)
def initialized(
    ls: LanguageServer,
    params: lsp.InitializedParams,  # pylint: disable=unused-argument
):
    """Handles LSP `initialized` notification."""

    _clear_ctx_validation()

    if ls.workspace.folders:
        # TODO: Handle more than one workspace folder
        folder = next(iter(ls.workspace.folders.values()))
        yang_uris = _get_folder_yang_uris(folder.uri)
        for yang_uri in yang_uris:
            if not yang_uri in ls.workspace.text_documents.keys():
                yang_file = to_fs_path(yang_uri)
                assert yang_file
                with open(yang_file, 'r', encoding='utf-8') as file:
                    yang_source = file.read()
                    file.close()
                ls.workspace.put_text_document(
                    lsp.TextDocumentItem(
                        uri=yang_uri,
                        language_id='yang',
                        version=0,
                        text=yang_source,
                    )
                )

    _update_ctx_modules()
    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################
#-------------------------------------------------------------------------------
# Document Synchronization
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def text_document_did_open(
    ls: LanguageServer,
    params: lsp.DidOpenTextDocumentParams
):
    """Handles LSP `textDocument/didOpen` notification."""

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    orig_source = text_doc._source

    # Prevent direct file read on next TextDocument.source access
    text_doc._source = params.text_document.text

    if params.text_document.text == orig_source:
        # Some LSP clients like Emacs/eglot do not consume an earlier diagnostic
        # publishing for the
        _publish_doc_diagnostics(text_doc)
        return

    # File content of opened file is not matching ex
    _clear_ctx_validation()
    _update_ctx_modules()
    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################


# pyang supports LSP `TextDocumentSyncKind` `Full` but not `Incremental`
# The mapping is provided via initialization parameters of pygls LanguageServer
@pyangls.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def text_document_did_change(
    ls: LanguageServer,
    params: lsp.DidChangeTextDocumentParams
):
    """Handles LSP `textDocument/didChange` notification."""

    _clear_ctx_validation()

    for content_change in params.content_changes:
        ls.workspace.update_text_document(params.text_document, content_change)

    _update_ctx_modules()
    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
def text_document_did_close(
    ls: LanguageServer,
    params: lsp.DidCloseTextDocumentParams
):
    """Handles LSP `textDocument/didClose` notification."""

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    orig_source = text_doc._source
    # Force text document read from file system on next get_text_document()
    text_doc._source = None
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    # Text document source is now corresponding to the file system

    # If last cached source is not different from file system then return
    if text_doc._source == orig_source:
        return

    # Validation is rerun and textDocument/PublishDiagnostics is resent for all
    # workspace files due to LSP clients such as Emacs/eglot which do not send a
    # textDocument/didChange notification before textDocument/didClose for the
    # case when an edited buffer window is killed without saving so that the
    # project diagnostics are still consistent
    _clear_ctx_validation()
    _update_ctx_modules()
    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################
#-------------------------------------------------------------------------------
# LSP Language Features
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DEFINITION)
def text_document_definition(
    ls: PyangLanguageServer,
    params: lsp.ReferenceParams
) -> Union[lsp.Definition, List[lsp.DefinitionLink], None]:
    """Handles LSP `textDocument/definition` request."""

    module = ls.modules[params.text_document.uri]
    definition_uri = None
    origin_select_range = None
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'kwd'):
            origin_select_range = glue.kwd_lsp_selection_range(stmt.pos)
            try:
                try:
                    uri = rfcref_stmt_map[stmt.parent.keyword]['substmt'][stmt.keyword]['uri']
                except (KeyError, AttributeError):
                    uri = rfcref_stmt_map[stmt.keyword]['uri']
                definition_link = lsp.LocationLink(
                    target_uri=uri,
                    target_range=lsp.Range(lsp.Position(0,0),lsp.Position(0,0)),
                    target_selection_range=lsp.Range(lsp.Position(0,0),lsp.Position(0,0)),
                    origin_selection_range=origin_select_range,
                )
                return [definition_link]
            except (KeyError, AttributeError):
                pass
            ref_stmt = helper.ext_stmt_from_stmt_kwd(ls.ctx, stmt)
            if not ref_stmt:
                return
            for uri, module in ls.modules.items():
                if ref_stmt.top == module:
                    definition_uri = uri
                    break
        case (stmt, 'arg'):
            ref_stmt = None
            match stmt.keyword:
                case 'augment':
                    aug: statements.AugmentStatement = stmt # type: ignore
                    ref_stmt = helper.get_augmented_stmt(aug)
                    if not ref_stmt:
                        return
                    for uri, module in ls.modules.items():
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'refine':
                    ref_stmt = helper.get_refined_stmt(stmt)
                    if not ref_stmt:
                        return
                    for uri, module in ls.modules.items():
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'deviation':
                    dev: statements.DeviationStatement = stmt # type: ignore
                    ref_stmt = helper.get_deviated_stmt(dev)
                    if not ref_stmt:
                        return
                    for uri, module in ls.modules.items():
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'path':
                    ref_stmt = helper.get_leafrefed_stmt(stmt)
                    if not ref_stmt:
                        return
                    for uri, module in ls.modules.items():
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'uses' | 'if-feature' | 'type' | 'base':
                    ref_stmt = helper.referenced_stmt_from_stmt_arg(ls.ctx, stmt)
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items():
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'import':
                    revision = None
                    r = stmt.search_one('revision-date')
                    if r is not None:
                        revision = r.arg
                    module = ls.ctx.get_module(stmt.arg, revision)
                    if module:
                        for uri, module in ls.modules.items():
                            ref_stmt = module
                            # TODO: handle multiple module revisions
                            if ref_stmt.arg == stmt.arg:
                                definition_uri = uri
                                break
                case 'key':
                    if stmt.arg:
                        keys = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(keys) > 1 or \
                            (len(keys) == 1 and arglen == (len(keys[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        key = None
                        for key in keys:
                            echar = schar + len(key)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(key) + 1
                        if not key:
                            return None
                        if hasattr(stmt.parent, 'i_key') and stmt.parent.i_key:
                            for ref_stmt in stmt.parent.i_key:
                                if key == ref_stmt.arg:
                                    break
                        else:
                            # TODO: check why i_key was not populated in some cases
                            for substmt in stmt.parent.substmts:
                                if substmt.keyword == 'leaf' and key == substmt.arg:
                                    ref_stmt = substmt
                                    break
                        if not ref_stmt:
                            return None
                        origin_select_range = lsp.Range(
                            start=lsp.Position(line=stmt.pos.arg_sline, character=schar),
                            end=lsp.Position(line=stmt.pos.arg_eline, character=echar),
                        )
                        for uri, module in ls.modules.items():
                            if ref_stmt.top == module:
                                definition_uri = uri
                                break
                    if not ref_stmt:
                        return None
                case 'unique':
                    if stmt.arg:
                        uniques = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(uniques) > 1 or \
                            (len(uniques) == 1 and arglen == (len(uniques[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        unique = None
                        for unique in uniques:
                            echar = schar + len(unique)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(unique) + 1
                        if not unique:
                            return None
                        for i_unique in stmt.parent.i_unique:
                            (_, unique_stmts) = i_unique
                            for ref_stmt in unique_stmts:
                                if unique == ref_stmt.arg:
                                    origin_select_range = lsp.Range(
                                        start=lsp.Position(
                                            line=stmt.pos.arg_sline,
                                            character=schar,
                                        ),
                                        end=lsp.Position(
                                            line=stmt.pos.arg_eline,
                                            character=echar,
                                        ),
                                    )
                                    break
                        if not ref_stmt:
                            return None
                        for uri, module in ls.modules.items():
                            if ref_stmt.top == module:
                                definition_uri = uri
                                break
                    if not ref_stmt:
                        return None
                case _:
                    return None
            if not origin_select_range:
                origin_select_range = glue.arg_lsp_selection_range(stmt.pos)
        case _:
            return None

    if not ref_stmt or not definition_uri:
        return None
    definition_range = glue.stmt_lsp_range(ref_stmt.pos)
    definition_select_range = glue.arg_lsp_selection_range(ref_stmt.pos)
    definition_link = lsp.LocationLink(
        target_uri=definition_uri,
        target_range=definition_range,
        target_selection_range=definition_select_range,
        origin_selection_range=origin_select_range,
    )
    # TODO: Add all arg definitions in workspace
    # TODO: Send definitions in all modules since implemented one is
    #       not known in the context
    return [definition_link]


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_TYPE_DEFINITION)
def text_document_type_definition(
    _ls: LanguageServer,
    params: lsp.TypeDefinitionParams
) -> Union[lsp.Definition, List[lsp.DefinitionLink], None]:
    """Handles LSP `textDocument/typeDefinition` request."""

    module = pyangls.modules[params.text_document.uri]
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'arg'):
            pass
        case _:
            return None
    if stmt and stmt.keyword == 'type' and stmt.arg:
        prefix_parts = str(stmt.arg).rsplit(':')
        if len(prefix_parts) == 1:
            typedef_name = prefix_parts[0]
            typedef_uri = params.text_document.uri
            typedef_module = module
        elif len(prefix_parts) == 2:
            typedef_name = prefix_parts[1]
            imp_mods = module.search('import')
            imp_mod = None
            for imp_mod in imp_mods:
                imp_prefix = imp_mod.search_one('prefix')
                if imp_prefix.arg == prefix_parts[0]:
                    break
            if not imp_mod:
                return None
            typedef_module = None
            for uri, module in pyangls.modules.items():
                typedef_module = module
                if module.arg == imp_mod.arg:
                    typedef_uri = uri
                    break
        else:
            return None
        if not typedef_module:
            return None
        typedefs = typedef_module.search('typedef')
        typedef: Statement
        for typedef in typedefs:
            if typedef.arg == typedef_name:
                typedef_range = glue.stmt_lsp_range(typedef.pos)
                typedef_select_range = glue.arg_lsp_selection_range(typedef.pos)
                definition_link = lsp.LocationLink(
                    target_uri=typedef_uri,
                    target_range=typedef_range,
                    target_selection_range=typedef_select_range,
                    origin_selection_range=glue.stmt_lsp_range(stmt.pos)
                )
                # TODO: Send definitions in all modules since implemented one is
                #       not known in the context
                return [definition_link]


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_REFERENCES)
def text_document_references(
    ls: PyangLanguageServer,
    params: lsp.ReferenceParams
) -> Union[List[lsp.Location], None]:
    """Handles LSP `textDocument/references` request."""

    module = ls.modules[params.text_document.uri]
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'arg'):
            ref_stmts = helper.find_stmt_references(ls.ctx, stmt)
            match stmt.keyword:
                case 'path' | 'augment' | 'deviation':
                    pass
                case _:
                    # lookup stmt is a reference as well
                    ref_stmts.append(stmt)
        case _:
            return None
    return stmts_to_lsp_locations(ref_stmts)


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_HIGHLIGHT)
def text_document_document_highlight(
    ls: PyangLanguageServer,
    params: lsp.DocumentHighlightParams
) -> Union[List[lsp.DocumentHighlight], None]:
    """Handles LSP `textDocument/documentHighlight` notification."""

    module = ls.modules[params.text_document.uri]
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'kwd'):
            highlight_range = glue.kwd_lsp_selection_range(stmt.pos)
            highlight_kind = lsp.DocumentHighlightKind.Text
        case (stmt, 'arg'):
            highlight_kind = lsp.DocumentHighlightKind.Text
            highlight_range = glue.arg_lsp_selection_range(stmt.pos)
            match stmt.keyword:
                case 'module' | 'submodule' | 'feature':
                    highlight_kind = lsp.DocumentHighlightKind.Write
                case 'import' | 'include' | 'if-feature':
                    highlight_kind = lsp.DocumentHighlightKind.Read
                case 'key':
                    highlight_kind = lsp.DocumentHighlightKind.Read
                    if stmt.arg:
                        keys = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(keys) > 1 or \
                            (len(keys) == 1 and arglen == (len(keys[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        key = None
                        for key in keys:
                            echar = schar + len(key)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(key) + 1
                        if hasattr(stmt.parent, 'i_key') and stmt.parent.i_key:
                            for ref_stmt in stmt.parent.i_key:
                                if key == ref_stmt.arg:
                                    break
                        else:
                            # TODO: check why i_key was not populated in some cases
                            for substmt in stmt.parent.substmts:
                                if substmt.keyword == 'leaf' and key == substmt.arg:
                                    ref_stmt = substmt
                                    break
                        highlight_range = lsp.Range(
                            start=lsp.Position(line=stmt.pos.arg_sline, character=schar),
                            end=lsp.Position(line=stmt.pos.arg_eline, character=echar),
                        )
                case 'unique':
                    highlight_kind = lsp.DocumentHighlightKind.Read
                    if stmt.arg:
                        uniques = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(uniques) > 1 or \
                            (len(uniques) == 1 and arglen == (len(uniques[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        unique = None
                        for unique in uniques:
                            echar = schar + len(unique)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(unique) + 1
                        for i_unique in stmt.parent.i_unique:
                            (_, unique_stmts) = i_unique
                            for unique_stmt in unique_stmts:
                                if unique == unique_stmt.arg:
                                    highlight_range = lsp.Range(
                                        start=lsp.Position(
                                            line=stmt.pos.arg_sline,
                                            character=schar
                                        ),
                                        end=lsp.Position(
                                            line=stmt.pos.arg_eline,
                                            character=echar
                                        ),
                                    )
                                    break
        case _:
            return None
    highlight = lsp.DocumentHighlight(
        range=highlight_range,
        kind=highlight_kind,
    )
    # TODO: Add all other highlights in file
    return [highlight]


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_HOVER)
def text_document_hover(
    ls: PyangLanguageServer,
    params: lsp.HoverParams
) -> lsp.Hover:
    """Handles LSP `textDocument/hover` request."""

    module = ls.modules[params.text_document.uri]

    hover_value = ''

    def append_hover(current: str, value: str) -> str:
        if current != '':
            current += '\n___\n'
        return current + value

    def append_ref_info(current: str, stmt: Statement) -> str:
        ref_stmt = helper.referenced_stmt_from_stmt_arg(ls.ctx, stmt)
        if ref_stmt:
            desc = statements.get_description(ref_stmt)
            if desc and desc.strip() != '':
                value = '**' + helper.ref_map[stmt.keyword] + '**: ' + desc
                return append_hover(current, value)
        return current

    def rfcref_value(rfcref: dict[str, str]) -> str:
        return rfcref['title'] + ' ' + rfcref['uri']

    hover_range = None
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'kwd'):
            target: Statement
            try:
                target = stmt.parent
                try:
                    parent_map = rfcref_stmt_map[target.keyword]['substmt']
                    kwd_rfcref = parent_map[stmt.keyword]
                except (KeyError, AttributeError):
                    # No parent specific reference map exists, use generic map
                    kwd_rfcref = rfcref_stmt_map[stmt.keyword]
                hover_value = append_hover(hover_value, rfcref_value(kwd_rfcref))
            except KeyError:
                match stmt.keyword:
                    case 'config' | 'mandatory' | 'default' | 'min-elements' | 'max-elements':
                        # deviation
                        target = stmt.parent.parent.i_target_node
                        try:
                            parent_map = rfcref_stmt_map[target.keyword]['substmt']
                            kwd_rfcref = parent_map[stmt.keyword]
                        except (KeyError, AttributeError):
                            # No parent specific reference map exists, use generic map
                            kwd_rfcref = rfcref_stmt_map[stmt.keyword]
                        hover_value = append_hover(hover_value, rfcref_value(kwd_rfcref))
                    case _:
                        # not an inbuilt keyword
                        ext_stmt = helper.ext_stmt_from_stmt_kwd(ls.ctx, stmt)
                        if ext_stmt:
                            # extension
                            desc = statements.get_description(ext_stmt)
                            if desc and desc.strip() != '':
                                value = '**extension**: ' + desc
                                hover_value = append_hover(hover_value, value)
            hover_range = glue.kwd_lsp_selection_range(stmt.pos)
        case (stmt, 'arg'):
            desc = statements.get_description(stmt)
            if desc and desc.strip() != '':
                if stmt.keyword == 'refine':
                    value = '**refined**: ' + desc
                else:
                    value = desc
                hover_value = append_hover(hover_value, value)
            ref = helper.get_reference(stmt)
            if ref and ref.strip() != '':
                hover_value += '\n\n*See*: ' + ref
            match stmt.keyword:
                case 'augment':
                    aug: statements.AugmentStatement = stmt # type: ignore
                    aug_stmt = helper.get_augmented_stmt(aug)
                    if aug_stmt:
                        desc = statements.get_description(aug_stmt)
                        if desc and desc.strip() != '':
                            value = '**' + aug_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'refine':
                    ref_stmt = helper.get_refined_stmt(stmt)
                    if ref_stmt and hasattr(ref_stmt, 'i_refined'):
                        if 'description' in ref_stmt.i_refined:
                            desc = ref_stmt.i_refined['description']
                        else:
                            desc = statements.get_description(ref_stmt)
                        if desc and desc.strip() != '':
                            value = '**original**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'deviation':
                    dev: statements.DeviationStatement = stmt # type: ignore
                    dev_stmt = helper.get_deviated_stmt(dev)
                    if dev_stmt:
                        desc = statements.get_description(dev_stmt)
                        if desc and desc.strip() != '':
                            value = '**' + dev_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'path':
                    ref_stmt = helper.get_leafrefed_stmt(stmt)
                    if ref_stmt:
                        desc = statements.get_description(ref_stmt)
                        if desc and desc.strip() != '':
                            value = '**' + ref_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'uses' | 'if-feature' | 'base':
                    hover_value = append_ref_info(hover_value, stmt)
                case 'import':
                    revision = None
                    r = stmt.search_one('revision-date')
                    if r is not None:
                        revision = r.arg
                    module = ls.ctx.get_module(stmt.arg, revision)
                    if module:
                        desc = statements.get_description(module)
                        if desc:
                            value = '**module**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'type':
                    try:
                        type_rfcref = rfcref_type_map[stmt.arg] # type: ignore
                        hover_value = append_hover(hover_value, rfcref_value(type_rfcref))
                    except KeyError:
                        # not an inbuilt type
                        hover_value = append_ref_info(hover_value, stmt)
                case 'default':
                    type_ = stmt.parent.search_one('type')
                    desc_stmt = None
                    match type_.arg:
                        case 'enumeration':
                            for substmt in type_.substmts:
                                if substmt.keyword == 'enum' and substmt.arg == stmt.arg:
                                    desc_stmt = substmt
                                    break
                    if desc_stmt:
                        desc = statements.get_description(desc_stmt)
                        if desc:
                            value = '**' + desc_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'key':
                    if stmt.arg:
                        keys = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(keys) > 1 or \
                            (len(keys) == 1 and arglen == (len(keys[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        key = None
                        for key in keys:
                            echar = schar + len(key)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(key) + 1
                        if hasattr(stmt.parent, 'i_key') and stmt.parent.i_key:
                            for key_stmt in stmt.parent.i_key:
                                if key == key_stmt.arg:
                                    break
                        else:
                            # TODO: check why i_key was not populated in some cases
                            for substmt in stmt.parent.substmts:
                                if substmt.keyword == 'leaf' and key == substmt.arg:
                                    key_stmt = substmt
                                    break
                        if key_stmt:
                            desc = statements.get_description(key_stmt)
                            if desc and desc.strip() != '':
                                value = '**leaf**: ' + desc
                                hover_value = append_hover(hover_value, value)
                            # TODO: handle keys on different lines
                            hover_range = lsp.Range(
                                start=lsp.Position(line=stmt.pos.arg_sline, character=schar),
                                end=lsp.Position(line=stmt.pos.arg_eline, character=echar),
                            )
                case 'unique':
                    if stmt.arg:
                        uniques = str(stmt.arg).split(' ')
                        arglen = stmt.pos.arg_echar - stmt.pos.arg_schar
                        quoted = 0
                        if len(uniques) > 1 or \
                            (len(uniques) == 1 and arglen == (len(uniques[0]) + 2)):
                            quoted = 1
                        schar = stmt.pos.arg_schar + quoted
                        unique = None
                        for unique in uniques:
                            echar = schar + len(unique)
                            if schar <= params.position.character < echar:
                                break
                            schar += len(unique) + 1
                        if unique:
                            for i_unique in stmt.parent.i_unique:
                                (_, unique_stmts) = i_unique
                                for unique_stmt in unique_stmts:
                                    if unique == unique_stmt.arg:
                                        desc = statements.get_description(unique_stmt)
                                        if desc and desc.strip() != '':
                                            value = '**leaf**: ' + desc
                                            hover_value = append_hover(hover_value, value)
                                        hover_range = lsp.Range(
                                            start=lsp.Position(
                                                line=stmt.pos.arg_sline,
                                                character=schar,
                                            ),
                                            end=lsp.Position(
                                                line=stmt.pos.arg_eline,
                                                character=echar,
                                            ),
                                        )
                                        break
            if not hover_range:
                hover_range = glue.arg_lsp_selection_range(stmt.pos)
        case _:
            hover_range = lsp.Range(start=params.position, end=params.position)

    return lsp.Hover(
        contents=lsp.MarkupContent(
            kind=lsp.MarkupKind.Markdown,
            value=hover_value,
        ),
        range=hover_range
    )


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_CODE_LENS)
def text_document_code_lens(
    ls: PyangLanguageServer,
    params: lsp.CodeLensParams,
) -> Union[List[lsp.CodeLens], None]:
    module = ls.modules[params.text_document.uri]
    if not module:
        return None
    return code_lens.build_list(ls.ctx, module, params.text_document.uri)


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_FOLDING_RANGE)
def text_document_folding_range(
    ls: PyangLanguageServer,
    params: lsp.FoldingRangeParams,
) -> Union[List[lsp.FoldingRange], None]:
    module = ls.modules[params.text_document.uri]
    if not module:
        return None
    return folding_range.build_list(module)


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
async def text_document_document_symbol(
    ls: PyangLanguageServer,
    params: lsp.DocumentSymbolParams,
) -> List[lsp.DocumentSymbol] | None:
    """Handles LSP `textDocument/documentSymbol` request."""

    try:
        module = ls.modules[params.text_document.uri]
        if module is None:
            return None
    except KeyError:
        if _have_parser_errors():
            ls.show_message_log("Syntactically invalid document is not outlined.",
                                msg_type=lsp.MessageType.Debug)
        return None

    try:
        if pyangls.doc_symbols[params.text_document.uri]:
            return pyangls.doc_symbols[params.text_document.uri]
    except KeyError:
        pass

    document_symbols = []
    for substmt in module.substmts:
        module_symbols = _build_doc_stmt_symbols(substmt)
        if module_symbols:
            document_symbols.append(module_symbols)
    pyangls.doc_symbols[params.text_document.uri] = document_symbols
    return document_symbols


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_INLINE_VALUE)
def text_document_inline_value(
    ls: PyangLanguageServer,
    params: lsp.InlineValueParams,
) -> Union[List[lsp.InlineValueText], None]:
    module = ls.modules[params.text_document.uri]
    if not module:
        return None
    return inline_value.build_list(module, params.text_document.uri)


################################################################################


@pyangls.feature(
    lsp.TEXT_DOCUMENT_COMPLETION,
    lsp.CompletionOptions(trigger_characters=completion.trigger_characters),
)
def text_document_completion(
    ls: PyangLanguageServer,
    params: lsp.CompletionParams,
) -> Union[List[lsp.CompletionItem], lsp.CompletionList, None]:
    module = ls.modules[params.text_document.uri]
    if not module:
        return None
    return completion.build_list(ls.ctx, module, params.position)


################################################################################


@pyangls.feature(
    lsp.TEXT_DOCUMENT_DIAGNOSTIC,
    lsp.DiagnosticOptions(
        identifier=SERVER_NAME,
        inter_file_dependencies=True,
        workspace_diagnostics=True,
    ),
)
def text_document_diagnostic(
    params: lsp.DocumentDiagnosticParams,
) -> lsp.DocumentDiagnosticReport:
    """Handles LSP `textDocument/diagnostic` request."""

    if pyangls.client_capabilities.text_document is None or \
        pyangls.client_capabilities.text_document.diagnostic is None:
        pyangls.show_message("Unexpected textDocument/diagnostic from incapable client.")

    if not (items := pyangls.diagnostics[params.text_document.uri]):
        text_doc = pyangls.workspace.get_text_document(params.text_document.uri)
        doc_items = _build_doc_diagnostics(text_doc.path)
        if doc_items is None:
            items = []
        else:
            items = doc_items

    # TODO: check if there are any errors which provide related diagnostics
    return lsp.RelatedFullDocumentDiagnosticReport(
        items=items,
    )


################################################################################


@pyangls.feature(lsp.WORKSPACE_DIAGNOSTIC)
def workspace_diagnostic(
    params: lsp.WorkspaceDiagnosticParams,
) -> lsp.WorkspaceDiagnosticReport:
    """Handles LSP `workspace/diagnostic` request."""

    if pyangls.client_capabilities.text_document is None or \
            pyangls.client_capabilities.text_document.diagnostic is None:
        pyangls.show_message("Unexpected workspace/diagnostic from incapable client.")

    if params.identifier:
        pyangls.log_trace(params.identifier)

    items : List[lsp.WorkspaceDocumentDiagnosticReport] = []
    for text_doc_uri in pyangls.workspace.text_documents.keys():
        text_doc = pyangls.workspace.get_text_document(text_doc_uri)
        doc_items = _build_doc_diagnostics(text_doc.path)
        if doc_items is not None:
            items.append(
                lsp.WorkspaceFullDocumentDiagnosticReport(
                    uri=text_doc.uri,
                    version=text_doc.version,
                    items=doc_items,
                    kind=lsp.DocumentDiagnosticReportKind.Full,
                )
            )

    return lsp.WorkspaceDiagnosticReport(items=items)


################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_FORMATTING)
def text_document_formatting(
    ls: LanguageServer,
    params: lsp.DocumentFormattingParams
):
    """Handles LSP `textDocument/formatting` notification."""

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    source = text_doc.source

    if source is None:
        ls.show_message("No source found")
        return []

    module = _update_ctx_module(text_doc)
    if module is None:
        if _have_parser_errors():
            ls.show_message("Document was syntactically invalid. Did not format.",
                            msg_type=lsp.MessageType.Debug)
        return []

    _validate_ctx_modules()

    fmt_text=_format_yang(source, params.options, module)

    start_pos = lsp.Position(line=0, character=0)
    end_pos = lsp.Position(line=len(text_doc.lines), character=0)
    text_range = lsp.Range(start=start_pos, end=end_pos)

    return [lsp.TextEdit(range=text_range, new_text=fmt_text)]


################################################################################
#-------------------------------------------------------------------------------
# Workspace Features
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.WORKSPACE_SYMBOL)
def workspace_symbol(
    ls: PyangLanguageServer,
    params: lsp.WorkspaceSymbolParams
) -> List[lsp.WorkspaceSymbol]:
    """Handles LSP `workspace/symbol` request."""

    symbols = []
    for doc_uri in pyangls.workspace.text_documents:
        module = ls.modules[doc_uri]
        symbols += _build_ws_stmt_symbols(module, doc_uri, params.query, None)
    return symbols


################################################################################


@pyangls.feature(lsp.WORKSPACE_DID_CHANGE_CONFIGURATION)
def workspace_did_change_configuration(
    ls: LanguageServer,
    params: lsp.DidChangeConfigurationParams
):
    """Handles LSP `workspace/didChangeConfiguration` request."""

    # TODO: Handle config changes including ignoring additional files/subdirs
    _process_workspace_configuration(None, [params.settings])
    _clear_ctx_validation()

    if ls.workspace.folders:
        # TODO: Handle more than one workspace folder
        folder = next(iter(ls.workspace.folders.values()))
        yang_uris = _get_folder_yang_uris(folder.uri)
        for yang_uri in yang_uris:
            if not yang_uri in ls.workspace.text_documents.keys():
                yang_file = to_fs_path(yang_uri)
                assert yang_file
                with open(yang_file, 'r', encoding='utf-8') as file:
                    yang_source = file.read()
                    file.close()
                ls.workspace.put_text_document(
                    lsp.TextDocumentItem(
                        uri=yang_uri,
                        language_id='yang',
                        version=0,
                        text=yang_source,
                    )
                )

    _update_ctx_modules()

    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################


@pyangls.feature(lsp.WORKSPACE_DID_CHANGE_WATCHED_FILES)
def workspace_did_change_watched_files(
    ls: LanguageServer,
    params: lsp.DidChangeWatchedFilesParams
):
    """Handles LSP `workspace/didChangeWatchedFiles` notification."""

    _clear_ctx_validation()

    # Process all the Deleted events first to handle renames gracefully
    for event in params.changes:
        if event.type != lsp.FileChangeType.Deleted:
            continue

        text_doc = ls.workspace.get_text_document(event.uri)
        ls.workspace.remove_text_document(text_doc.uri)
        _delete_from_ctx(text_doc)
        _publish_doc_diagnostics(text_doc, [])

    for event in params.changes:
        if event.type == lsp.FileChangeType.Created:
            yang_file = to_fs_path(event.uri)
            assert yang_file
            with open(yang_file, 'r', encoding='utf-8') as file:
                yang_source = file.read()
                file.close()
            ls.workspace.put_text_document(
                lsp.TextDocumentItem(
                    uri=event.uri,
                    language_id='yang',
                    version=0,
                    text=yang_source,
                )
            )
        elif event.type == lsp.FileChangeType.Changed:
            text_doc = ls.workspace.get_text_document(event.uri)
            text_doc._source = None

    _update_ctx_modules()
    _validate_ctx_modules()
    _publish_workspace_diagnostics()


################################################################################
#-------------------------------------------------------------------------------
# Window Features
#-------------------------------------------------------------------------------
################################################################################


################################################################################
