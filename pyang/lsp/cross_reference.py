"""LSP Cross Reference Provider

* `textDocument/definition`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
* `textDocument/typeDefinition`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_typeDefinition

Not Applicable to YANG:
* Go to Declaration `textDocument/declaration`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_declaration
* Go to Implementation `textDocument/implementation`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_implementation
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.uris import from_fs_path

from pyang.lsp import common
from pyang.statements import (
    AugmentStatement,
    DeviationStatement,
    Statement,
)

from . import glue
from .rfc import stmt_map


def _stmts_to_lsp_locations(
    stmts: List[Statement]
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



def text_document_references(
    ls: LanguageServer,
    params: lsp.ReferenceParams,
) -> Union[List[lsp.Location], None]:
    """Handles LSP `textDocument/references` request."""
    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'arg'):
            ref_stmts = common.find_stmt_references(ls.ctx, stmt) # type: ignore
            match stmt.keyword:
                case 'path' | 'augment' | 'deviation':
                    pass
                case _:
                    pass
                    # lookup stmt is a reference as well
                    # ref_stmts.append(stmt)
        case _:
            return None
    return _stmts_to_lsp_locations(ref_stmts)


def text_document_definition(
    ls: LanguageServer,
    params: lsp.ReferenceParams,
) -> Union[lsp.Definition, List[lsp.DefinitionLink], None]:
    """Handles LSP `textDocument/definition` request."""
    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    definition_uri = None
    origin_select_range = None
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'kwd'):
            origin_select_range = glue.kwd_lsp_selection_range(stmt.pos)
            try:
                try:
                    uri = stmt_map[stmt.parent.keyword]['substmt'][stmt.keyword]['uri']
                except (KeyError, AttributeError):
                    uri = stmt_map[stmt.keyword]['uri']
                definition_link = lsp.LocationLink(
                    target_uri=uri,
                    target_range=lsp.Range(lsp.Position(0,0),lsp.Position(0,0)),
                    target_selection_range=lsp.Range(lsp.Position(0,0),lsp.Position(0,0)),
                    origin_selection_range=origin_select_range,
                )
                return [definition_link]
            except (KeyError, AttributeError):
                pass
            ref_stmt = common.ext_stmt_from_stmt_kwd(ls.ctx, stmt) # type: ignore
            if not ref_stmt:
                return None
            for uri, module in ls.modules.items(): # type: ignore
                if ref_stmt.top == module:
                    definition_uri = uri
                    break
        case (stmt, 'arg'):
            ref_stmt = None
            match stmt.keyword:
                case 'augment':
                    aug: AugmentStatement = stmt # type: ignore
                    ref_stmt = common.get_augmented_stmt(aug)
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items(): # type: ignore
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'refine':
                    ref_stmt = common.get_refined_stmt(stmt)
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items(): # type: ignore
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'deviation':
                    dev: DeviationStatement = stmt # type: ignore
                    ref_stmt = common.get_deviated_stmt(dev)
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items(): # type: ignore
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'path':
                    ref_stmt = common.get_leafrefed_stmt(stmt)
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items(): # type: ignore
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'uses' | 'if-feature' | 'type' | 'base':
                    ref_stmt = common.referenced_stmt_from_stmt_arg(ls.ctx, stmt) # type: ignore
                    if not ref_stmt:
                        return None
                    for uri, module in ls.modules.items(): # type: ignore
                        if ref_stmt.top == module:
                            definition_uri = uri
                            break
                case 'import':
                    revision = None
                    r = stmt.search_one('revision-date')
                    if r is not None:
                        revision = r.arg
                    module = ls.ctx.get_module(stmt.arg, revision) # type: ignore
                    if module:
                        for uri, module in ls.modules.items(): # type: ignore
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
                        for uri, module in ls.modules.items(): # type: ignore
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
                        for uri, module in ls.modules.items(): # type: ignore
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


def text_document_type_definition(
    ls: LanguageServer,
    params: lsp.TypeDefinitionParams,
) -> Union[lsp.Definition, List[lsp.DefinitionLink], None]:
    """Handles LSP `textDocument/typeDefinition` request."""
    if not ls.client_capabilities.text_document or \
        not ls.client_capabilities.text_document.type_definition:
        # Incapable client has sent `textDocument/typeDefinition` request
        return None
    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    uri = params.text_document.uri
    position = params.position
    match glue.stmt_from_lsp_position(module, position):
        case (stmt, 'arg'):
            pass
        case _:
            return None
    if stmt and stmt.keyword == 'type' and stmt.arg:
        prefix_parts = str(stmt.arg).rsplit(':')
        if len(prefix_parts) == 1:
            typedef_name = prefix_parts[0]
            typedef_uri = uri
            typedef_mod = module
        elif len(prefix_parts) == 2:
            typedef_name = prefix_parts[1]
            imp_mods: List[Statement] = module.search('import')
            imp_mod: Statement | None = None
            for imp_mod in imp_mods:
                imp_prefix: Statement | None = imp_mod.search_one('prefix')
                if imp_prefix and imp_prefix.arg == prefix_parts[0]:
                    break
            if not imp_mod:
                return None
            typedef_mod = None
            for uri, mod in ls.modules.items(): # type: ignore
                typedef_mod = mod
                if mod.arg == imp_mod.arg:
                    typedef_uri = uri
                    break
        else:
            return None
        if not typedef_mod:
            return None
        typedefs = typedef_mod.search('typedef')
        typedef: Statement
        for typedef in typedefs:
            if typedef.arg == typedef_name:
                typedef_range = glue.stmt_lsp_range(typedef.pos)
                typedef_select_range = glue.arg_lsp_selection_range(typedef.pos)
                if not ls.client_capabilities.text_document.type_definition.link_support:
                    # TODO: Send List[lsp.Location] instead
                    pass
                definition_link = lsp.LocationLink(
                    target_uri=typedef_uri,
                    target_range=typedef_range,
                    target_selection_range=typedef_select_range,
                    origin_selection_range=glue.stmt_lsp_range(stmt.pos)
                )
                # TODO: Send definitions in all modules since implemented one is
                #       not known in the context
                return [definition_link]


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_DEFINITION)(text_document_definition)
    ls.feature(lsp.TEXT_DOCUMENT_TYPE_DEFINITION)(text_document_type_definition)
    ls.feature(lsp.TEXT_DOCUMENT_REFERENCES)(text_document_references)
