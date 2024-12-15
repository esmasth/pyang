"""LSP Call Hierarchy and Type Hierarchy Provider

* `textDocument/prepareCallHierarchy`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_prepareCallHierarchy
* `callHierarchy/incomingCalls`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#callHierarchy_incomingCalls
* `callHierarchy/outgoingCalls`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#callHierarchy_outgoingCalls
* `textDocument/prepareTypeHierarchy`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_prepareTypeHierarchy
* `typeHierarchy/supertypes`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#typeHierarchy_supertypes
* `typeHierarchy/subtypes`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#typeHierarchy_subtypes
"""

from posixpath import basename
from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.uris import from_fs_path

from pyang.statements import ModSubmodStatement
from pyang.types import yang_type_specs

from . import common, glue


def text_document_prepare_call_hierarchy(
    ls: LanguageServer,
    params: lsp.CallHierarchyPrepareParams,
) -> Union[List[lsp.CallHierarchyItem], None]:
    """Handles LSP `textDocument/prepareCallHierarchy` request."""

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'arg'):
            if not stmt or not stmt.arg:
                return None
        case _:
            return None

    call_hierarchy_items = []

    symbol_range = glue.stmt_lsp_range(stmt.pos)
    selection_range = glue.arg_lsp_selection_range(stmt.pos)
    tags = []

    match stmt.keyword:
        case 'module' | 'submodule':
            kind = lsp.SymbolKind.Module
        case _:
            return None

    call_hierarchy_items.append(
        lsp.CallHierarchyItem(
            name=stmt.arg,
            kind=kind,
            uri=params.text_document.uri,
            range=symbol_range,
            selection_range=selection_range,
            tags=tags,
            detail=stmt.keyword,
            data=None,
        )
    )

    return call_hierarchy_items

def call_hierarchy_incoming_calls(
    ls: LanguageServer,
    params: lsp.CallHierarchyIncomingCallsParams,
) -> Union[List[lsp.CallHierarchyIncomingCall], None]:
    """Handles LSP `callHierarchy/incomingCalls` request."""

    wfc = common.get_workspace_folder_context(ls, params.item.uri)
    if not wfc:
        return None

    try:
        module: ModSubmodStatement = ls.modules[params.item.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    call_hierarchy_items = []

    import_stmts = common.find_stmt_references(wfc.ctx, module)

    for stmt in import_stmts:
        if not stmt.arg:
            continue
        tags = []
        symbol_range = glue.stmt_lsp_range(stmt.top.pos)
        selection_range = glue.arg_lsp_selection_range(stmt.top.pos)
        from_range = glue.stmt_lsp_range(stmt.pos)
        kind = lsp.SymbolKind.Module
        uri = from_fs_path(stmt.pos.ref)
        if not uri:
            continue
        call_hierarchy_items.append(
            lsp.CallHierarchyIncomingCall(
                from_=lsp.CallHierarchyItem(
                    name=stmt.top.arg,
                    kind=kind,
                    uri=uri,
                    range=symbol_range,
                    selection_range=selection_range,
                    tags=tags,
                    detail=f"{stmt.top.keyword} ({stmt.keyword})",
                    data=None,
                ),
                from_ranges=[from_range],
            )
        )

    return call_hierarchy_items

def call_hierarchy_outgoing_calls(
    ls: LanguageServer,
    params: lsp.CallHierarchyOutgoingCallsParams,
) -> Union[List[lsp.CallHierarchyOutgoingCall], None]:
    """Handles LSP `callHierarchy/outgoingCalls` request."""

    wfc = common.get_workspace_folder_context(ls, params.item.uri)
    if not wfc:
        return None

    try:
        module: ModSubmodStatement | None = ls.modules[params.item.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    import_stmts = module.search('import')
    if not import_stmts:
        return []

    call_hierarchy_items = []

    for stmt in import_stmts:
        if not stmt.arg:
            continue
        tags = []
        from_range = glue.stmt_lsp_range(stmt.pos)
        revision = None
        r = stmt.search_one('revision-date')
        if r is not None:
            revision = r.arg
        module = wfc.ctx.get_module(stmt.arg, revision)
        ref_stmt = None
        ref_uri = None
        if module:
            for uri, mod in ls.modules.items(): # type: ignore
                ref_stmt = mod
                if not ref_stmt:
                    # TODO: check why this is possible
                    continue
                # TODO: handle multiple module revisions
                if ref_stmt.arg == stmt.arg:
                    ref_uri = uri
                    break
        if not ref_stmt or not ref_uri:
            continue

        to_range = glue.stmt_lsp_range(ref_stmt.pos)
        selection_range = glue.arg_lsp_selection_range(ref_stmt.pos)
        kind = lsp.SymbolKind.Module
        call_hierarchy_items.append(
            lsp.CallHierarchyOutgoingCall(
                to=lsp.CallHierarchyItem(
                    name=stmt.arg,
                    kind=kind,
                    uri=ref_uri,
                    range=to_range,
                    selection_range=selection_range,
                    tags=tags,
                    detail=f"{ref_stmt.keyword} ({stmt.keyword})",
                    data=None,
                ),
                from_ranges=[from_range],
            )
        )

    return call_hierarchy_items


def text_document_prepare_type_hierarchy(
    ls: LanguageServer,
    params: lsp.TypeHierarchyPrepareParams
) -> Union[List[lsp.TypeHierarchyItem], None]:
    """Handles LSP `textDocument/prepareTypeHierarchy` request."""

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    type_hierarchy_items = []

    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'arg'):
            if not stmt or not stmt.arg:
                return None
            match stmt.keyword:
                case 'typedef' | 'type':
                    type_kind = lsp.SymbolKind.Class
                    type_tags = []
                    if stmt.arg in yang_type_specs:
                        type_name = stmt.arg
                        type_detail = 'built-in'
                        type_uri = params.text_document.uri
                        type_pos = stmt.pos
                    else:
                        if stmt.keyword == 'typedef':
                            prefix = stmt.top.i_prefix
                            type_name = prefix + ':' + stmt.arg
                            typedef_stmt = stmt
                            type_uri = params.text_document.uri
                            type_pos = stmt.pos
                        else:
                            type_name = stmt.arg
                            typedef_stmt = common.referenced_stmt_from_stmt_arg(wfc.ctx, stmt)
                            if not typedef_stmt:
                                return None
                            type_uri = from_fs_path(typedef_stmt.top.pos.ref)
                            if not type_uri:
                                return None
                            type_pos = typedef_stmt.pos
                            status_stmt = typedef_stmt.search_one('status')
                            if status_stmt and status_stmt.arg in ['deprecated', 'obsolete']:
                                type_tags.append(lsp.SymbolTag.Deprecated)
                        type_detail = f"typedef ({basename(typedef_stmt.top.pos.ref)})"
                    type_range = glue.stmt_lsp_range(type_pos)
                    type_select_range = glue.arg_lsp_selection_range(type_pos)
                case _:
                    return None
        case _:
            return None

    type_hierarchy_items.append(
        lsp.TypeHierarchyItem(
            name=type_name,
            kind=type_kind,
            uri=type_uri,
            range=type_range,
            selection_range=type_select_range,
            tags=type_tags,
            detail=type_detail,
        )
    )

    return type_hierarchy_items

def type_hierarchy_supertypes(
    ls: LanguageServer,
    params: lsp.TypeHierarchySupertypesParams
) -> Union[List[lsp.TypeHierarchyItem], None]:
    """Handles LSP `typeHierarchy/supertypes` request."""

    wfc = common.get_workspace_folder_context(ls, params.item.uri)
    if not wfc:
        return None

    if params.item.name in yang_type_specs:
        return []

    type_hierarchy_items = []

    try:
        module = ls.modules[params.item.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    match glue.stmt_from_lsp_position(module, params.item.selection_range.start):
        case (stmt, 'arg'):
            if not stmt or not stmt.arg:
                return None
            match stmt.keyword:
                case 'typedef' | 'type':
                    pass
                case _:
                    return None
        case _:
            return None

    refing_stmts = common.get_referencing_stmts(stmt)
    for refing_stmt in refing_stmts:
        if refing_stmt.keyword == 'type':
            if refing_stmt.parent.keyword == 'typedef':
                typedef_stmt = refing_stmt.parent
                prefix = typedef_stmt.top.i_prefix
                type_name = prefix + ':' + typedef_stmt.arg
                type_uri = from_fs_path(typedef_stmt.top.pos.ref)
                if not type_uri:
                    continue
                type_range = glue.stmt_lsp_range(typedef_stmt.pos)
                type_select_range = glue.arg_lsp_selection_range(typedef_stmt.pos)
                type_kind = lsp.SymbolKind.Class
                type_tags = []
                type_detail = f"typedef ({basename(typedef_stmt.top.pos.ref)})"
                type_hierarchy_items.append(
                    lsp.TypeHierarchyItem(
                        name=type_name,
                        kind=type_kind,
                        uri=type_uri,
                        range=type_range,
                        selection_range=type_select_range,
                        tags=type_tags,
                        detail=type_detail,
                    )
                )
            elif refing_stmt.parent.keyword == 'type' and \
                    refing_stmt.parent.arg and \
                    refing_stmt.parent.arg == 'union':
                if not refing_stmt.parent.parent:
                    continue
                typedef_stmt = refing_stmt.parent.parent
                prefix = typedef_stmt.top.i_prefix
                type_name = prefix + ':' + typedef_stmt.arg
                type_uri = from_fs_path(typedef_stmt.top.pos.ref)
                if not type_uri:
                    continue
                type_range = glue.stmt_lsp_range(typedef_stmt.pos)
                type_select_range = glue.arg_lsp_selection_range(typedef_stmt.pos)
                type_kind = lsp.SymbolKind.Class
                type_tags = []
                type_detail = f"type ({basename(typedef_stmt.top.pos.ref)})"
                type_hierarchy_items.append(
                    lsp.TypeHierarchyItem(
                        name=type_name,
                        kind=type_kind,
                        uri=type_uri,
                        range=type_range,
                        selection_range=type_select_range,
                        tags=type_tags,
                        detail=type_detail,
                    )
                )

    return type_hierarchy_items

def type_hierarchy_subtypes(
    ls: LanguageServer,
    params: lsp.TypeHierarchySubtypesParams
) -> Union[List[lsp.TypeHierarchyItem], None]:
    """Handles LSP `typeHierarchy/subtypes` request."""

    wfc = common.get_workspace_folder_context(ls, params.item.uri)
    if not wfc:
        return None

    if params.item.name in yang_type_specs and params.item.name != 'union':
        return []

    try:
        module = ls.modules[params.item.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    type_hierarchy_items = []

    match glue.stmt_from_lsp_position(module, params.item.selection_range.start):
        case (stmt, 'arg'):
            if not stmt or not stmt.arg:
                return None
            match stmt.keyword:
                case 'typedef' | 'type':
                    if stmt.keyword == 'type' and stmt.arg == 'union':
                        type_stmts = stmt.search('type')
                    else:
                        type_stmt = stmt.search_one('type')
                        if not type_stmt or not type_stmt.arg:
                            return None
                        if type_stmt.arg == 'union':
                            type_stmts = type_stmt.search('type')
                        else:
                            type_stmts = [type_stmt]
                    for type_stmt in type_stmts:
                        if not type_stmt.arg:
                            continue
                        type_name = type_stmt.arg
                        type_kind = lsp.SymbolKind.Class
                        type_tags = []
                        if type_stmt.arg in yang_type_specs:
                            type_detail = 'built-in'
                            type_pos = type_stmt.pos
                        else:
                            typedef_stmt = common.referenced_stmt_from_stmt_arg(wfc.ctx, type_stmt)
                            if not typedef_stmt:
                                continue
                            status_stmt = typedef_stmt.search_one('status')
                            if status_stmt and status_stmt.arg in ['deprecated', 'obsolete']:
                                type_tags.append(lsp.SymbolTag.Deprecated)
                            type_detail = f"typedef ({basename(typedef_stmt.top.pos.ref)})"
                            type_pos = typedef_stmt.pos

                        type_uri = from_fs_path(type_pos.ref)
                        if not type_uri:
                            continue
                        type_range = glue.stmt_lsp_range(type_pos)
                        type_select_range = glue.arg_lsp_selection_range(type_pos)

                        type_hierarchy_items.append(
                            lsp.TypeHierarchyItem(
                                name=type_name,
                                kind=type_kind,
                                uri=type_uri,
                                range=type_range,
                                selection_range=type_select_range,
                                tags=type_tags,
                                detail=type_detail,
                            )
                        )
                case _:
                    return None
        case _:
            return None

    return type_hierarchy_items


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_PREPARE_CALL_HIERARCHY)(text_document_prepare_call_hierarchy)
    ls.feature(lsp.CALL_HIERARCHY_INCOMING_CALLS)(call_hierarchy_incoming_calls)
    ls.feature(lsp.CALL_HIERARCHY_OUTGOING_CALLS)(call_hierarchy_outgoing_calls)

    ls.feature(lsp.TEXT_DOCUMENT_PREPARE_TYPE_HIERARCHY)(text_document_prepare_type_hierarchy)
    ls.feature(lsp.TYPE_HIERARCHY_SUPERTYPES)(type_hierarchy_supertypes)
    ls.feature(lsp.TYPE_HIERARCHY_SUBTYPES)(type_hierarchy_subtypes)
