"""LSP Hover Provider

* `textDocument/hover`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover

"""

from typing import Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang import statements
from pyang.statements import Statement

from . import common, glue, rfc


def text_document_hover(
    ls: LanguageServer,
    params: lsp.HoverParams,
) -> Union[lsp.Hover, None]:
    """Handles LSP `textDocument/hover` request."""

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None

    hover_value = ''

    def append_hover(current: str, value: str) -> str:
        if current != '':
            current += '\n___\n'
        return current + value

    def append_ref_info(current: str, stmt: Statement) -> str:
        ref_stmt = common.referenced_stmt_from_stmt_arg(wfc.ctx, stmt)
        if ref_stmt:
            desc = statements.get_description(ref_stmt)
            if desc and desc.strip() != '':
                value = '**' + common.ref_map[stmt.keyword] + '**: ' + desc
                return append_hover(current, value)
        return current

    def rfcref_value(rfcref: dict[str, str]) -> str:
        return rfcref['title'] + '\n\n' + rfcref['brief'] + '\n\n' + rfcref['uri']

    hover_range = None
    match glue.stmt_from_lsp_position(module, params.position):
        case (stmt, 'kwd'):
            target: Statement
            try:
                target = stmt.parent
                try:
                    parent_map = rfc.stmt_map[target.keyword]['substmt']
                    kwd_rfcref = parent_map[stmt.keyword]
                except (KeyError, AttributeError):
                    # No parent specific reference map exists, use generic map
                    kwd_rfcref = rfc.stmt_map[stmt.keyword]
                hover_value = append_hover(hover_value, rfcref_value(kwd_rfcref))
            except KeyError:
                match stmt.keyword:
                    case 'config' | 'mandatory' | 'default' | 'min-elements' | 'max-elements':
                        # deviation
                        target = stmt.parent.parent.i_target_node
                        try:
                            parent_map = rfc.stmt_map[target.keyword]['substmt']
                            kwd_rfcref = parent_map[stmt.keyword]
                        except (KeyError, AttributeError):
                            # No parent specific reference map exists, use generic map
                            kwd_rfcref = rfc.stmt_map[stmt.keyword]
                        hover_value = append_hover(hover_value, rfcref_value(kwd_rfcref))
                    case _:
                        # not an inbuilt keyword
                        ext_stmt = common.ext_stmt_from_stmt_kwd(wfc.ctx, stmt)
                        if ext_stmt:
                            # extension
                            desc = statements.get_description(ext_stmt)
                            if desc and desc.strip() != '':
                                value = '**extension**: ' + desc
                                hover_value = append_hover(hover_value, value)
            hover_range = glue.kwd_lsp_selection_range(stmt.pos)
        case (stmt, 'arg'):
            stmt_status: Statement | None = stmt.search_one('status')
            if stmt_status and stmt_status.arg in ['deprecated', 'obsolete']:
                hover_value = append_hover(hover_value,
                                           f'This schema node is **{stmt_status.arg}**.')
            desc = statements.get_description(stmt)
            if desc and desc.strip() != '':
                if stmt.keyword == 'refine':
                    value = '**refined**: ' + desc
                else:
                    value = desc
                hover_value = append_hover(hover_value, value)
            ref = common.get_reference(stmt)
            if ref and ref.strip() != '':
                hover_value += '\n\n*See*: ' + ref
            match stmt.keyword:
                case 'augment':
                    aug: statements.AugmentStatement = stmt # type: ignore
                    aug_stmt = common.get_augmented_stmt(aug)
                    if aug_stmt:
                        desc = statements.get_description(aug_stmt)
                        if desc and desc.strip() != '':
                            value = '**' + aug_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'refine':
                    ref_stmt = common.get_refined_stmt(stmt)
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
                    dev_stmt = common.get_deviated_stmt(dev)
                    if dev_stmt:
                        desc = statements.get_description(dev_stmt)
                        if desc and desc.strip() != '':
                            value = '**' + dev_stmt.keyword + '**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'path':
                    ref_stmt = common.get_leafrefed_stmt(stmt)
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
                    module = wfc.ctx.get_module(stmt.arg, revision)
                    if module:
                        desc = statements.get_description(module)
                        if desc:
                            value = '**module**: ' + desc
                            hover_value = append_hover(hover_value, value)
                case 'type':
                    try:
                        type_rfcref = rfc.type_map[stmt.arg] # type: ignore
                        hover_value = append_hover(hover_value, rfcref_value(type_rfcref))
                    except KeyError:
                        # not an inbuilt type
                        hover_value = append_ref_info(hover_value, stmt)
                case 'default':
                    type_ = stmt.parent.search_one('type')
                    if not type_:
                        return None
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


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_HOVER)(text_document_hover)
