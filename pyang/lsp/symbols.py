"""LSP Symbols Provider

* `textDocument/documentSymbol`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol
* `workspace/symbol`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbol

TODO:
* `workspaceSymbol/resolve`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_symbolResolve

Not Applicable to YANG:
* Go to Declaration `textDocument/declaration`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_declaration
* Go to Implementation `textDocument/implementation`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_implementation
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang import error, grammar
from pyang.context import Context
from pyang.lsp import common, maps
from pyang.statements import LeafLeaflistStatement, Statement

from . import glue


def _stmt_to_lsp_symbol_kind(ctx: Context, stmt: Statement) -> lsp.SymbolKind:
    if stmt.arg is None:
        return lsp.SymbolKind.Property
    match stmt.keyword:
        case str():
            match stmt.keyword:
                case 'leaf':
                    def leaf_symbol_kind(
                        leaf: LeafLeaflistStatement
                    ) -> lsp.SymbolKind:
                        stmt_type = common.get_base_type(ctx, leaf)
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
                            return maps.type_map[stmt_type]['symbol']
                        except KeyError:
                            return lsp.SymbolKind.Field

                    return leaf_symbol_kind(stmt) # type: ignore

                case _:
                    try:
                        return maps.keyword_map[stmt.keyword]['symbol']
                    except KeyError:
                        return lsp.SymbolKind.Null
        case (str(), str()):
            return lsp.SymbolKind.Null
        case _:
            raise TypeError

def _build_doc_stmt_symbols(
    ctx: Context,
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
    symbol_kind = _stmt_to_lsp_symbol_kind(ctx, stmt)


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
        if isinstance(stmt.keyword, str):
            symbol_name = stmt.keyword
        else:
            # Likely extension statement
            return None
        if stmt.parent and stmt.parent.keyword in ['rpc', 'action']:
            symbol_detail = ''
            symbol_name = stmt.keyword
            if not symbol_select_range:
                symbol_select_range = glue.kwd_lsp_selection_range(stmt.pos)
        else:
            extra_detail = '  '
            extra_detail += '['
            if feature_cond or stmt.search('if-feature'):
                extra_detail += 'f'
                feature_cond = True
            if when_cond or stmt.search('when'):
                extra_detail += 'w'
                when_cond = True
            extra_detail += ']'
            extra_detail += '  '
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
            symbol_detail = stmt.keyword
            symbol_detail += extra_detail
            symbol_name = stmt.arg
            if not symbol_select_range:
                symbol_select_range = glue.arg_lsp_selection_range(stmt.pos)
    else:
        # Likely extension statement
        return None

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

            symbols = _build_doc_stmt_symbols(ctx, s, deprecated,
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

            symbols = _build_doc_stmt_symbols(ctx, s, deprecated,
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
    ctx: Context,
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
            symbols = _build_ws_stmt_symbols(ctx, s, doc_uri, query, container_name)
            if symbols:
                ctx_symbols += symbols
    if hasattr(stmt, 'i_children'):
        for s in stmt.i_children:
            symbols = _build_ws_stmt_symbols(ctx, s, doc_uri, query, container_name)
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
    symbol_kind = _stmt_to_lsp_symbol_kind(ctx, stmt)

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

async def text_document_document_symbol(
    ls: LanguageServer,
    params: lsp.DocumentSymbolParams,
) -> Union[List[lsp.SymbolInformation], List[lsp.DocumentSymbol], None]:
    """Handles LSP `textDocument/documentSymbol` request."""
    if not ls.client_capabilities.text_document or \
            not ls.client_capabilities.text_document.document_symbol:
        return None

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if module is None:
            if common.have_parser_errors(wfc.ctx):
                ls.show_message_log("Syntactically invalid document is not outlined.",
                                    msg_type=lsp.MessageType.Debug)
            return None
    except KeyError:
        return None

    try:
        if ls.doc_symbols[params.text_document.uri]: # type: ignore
            return ls.doc_symbols[params.text_document.uri] # type: ignore
    except KeyError:
        pass

    symbols = []
    for substmt in module.substmts:
        module_symbols = _build_doc_stmt_symbols(wfc.ctx, substmt)
        if module_symbols:
            symbols.append(module_symbols)
    ls.doc_symbols[params.text_document.uri] = symbols # type: ignore
    return symbols


def workspace_symbol(
    ls: LanguageServer,
    params: lsp.WorkspaceSymbolParams,
) -> Union[List[lsp.SymbolInformation], List[lsp.WorkspaceSymbol], None]:
    """Handles LSP `workspace/symbol` request."""
    if not ls.client_capabilities.workspace or \
            not ls.client_capabilities.workspace.symbol:
        return None

    symbols = []
    for wfc in ls.wfc.values(): # type: ignore
        for doc_uri in ls.workspace.text_documents:
            module = ls.modules[doc_uri] # type: ignore
            if not module:
                continue
            symbols += _build_ws_stmt_symbols(wfc.ctx, module, doc_uri, params.query, None)
    return symbols


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.WORKSPACE_SYMBOL)(workspace_symbol)
    ls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_SYMBOL)(text_document_document_symbol)
