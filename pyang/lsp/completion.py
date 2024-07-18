from typing import List, Tuple

from lsprotocol import types as lsp

from pyang import grammar, types
from pyang.context import Context
from pyang.lsp import glue, helper, maps, rfcref
from pyang.plugins import lint
from pyang.statements import Statement, ImportStatement, ModSubmodStatement
from pyang.translators import yang

INDENT_STEP = 2

trigger_characters = ['/']

keyword_arg_detail = {
    'description' : 'description',
    'reference'   : 'reference',
    'presence'    : 'implication',
    'grouping'    : 'name',
    'container'   : 'name',
    'list'        : 'name',
    'leaf'        : 'name',
    'leaf-list'   : 'name',
    'extension'   : 'name',
    'if-feature'  : 'feature-expr',
    'choice'      : 'name',
    'feature'     : 'name',  # FIXME: without detail all if-feature instances referenced the feature in codelens
    'min-elements': 'count',
    'max-elements': 'count',
}

keyword_no_substmt_arg = {
    'deviate': [
        'not-supported',
    ],
    'type': [
        'empty',
        'boolean'
    ],
}

def min_zero(cardinality: str) -> bool:
    return cardinality in ['?', '*']

def min_one(cardinality: str) -> bool:
    return cardinality in ['1', '+']

def max_one(cardinality: str) -> bool:
    return cardinality in ['?', '1']

def maybe_substatements(
    keyword: str,
) -> bool:
    match keyword:
        case 'deviate':
            return True
        # case 'type':
        #     return True
        case _:
            return False

def mandatory_substmt_keywords(
    yangver: str,
    keyword: str,
) -> List[str]:
    mandatory_substmts = []
    (_, substmt_props) = grammar.stmt_map[keyword]
    def append_mandatory_substmts(substmt_kwd, cardinality):
        if min_one(cardinality):
            mandatory_substmts.append(substmt_kwd)
    def handle_prop(prop):
        match prop:
            case ('$choice', _) | ((_, _), _):
                return
            case ('$interleave', interleave_list):
                for interleave_prop in interleave_list:
                    handle_prop(interleave_prop)
                return
            case ('$1.1', (substmt_kwd, cardinality)):
                if yangver == '1':
                    return
            case (substmt_kwd, cardinality):
                if substmt_kwd == '$cut':
                    return
            case _:
                return
        append_mandatory_substmts(substmt_kwd, cardinality)
    for substmt_prop in substmt_props:
        handle_prop(substmt_prop)
    return mandatory_substmts

def get_base_type(ctx: Context, stmt: Statement):
    stmt_type = stmt.search_one('type')
    if stmt_type:
        if stmt_type.arg in maps.type_lsp_kind:
            return stmt_type.arg
        typedef = helper.referenced_stmt_from_stmt_arg(ctx, stmt_type)
        if typedef:
            return get_base_type(ctx, typedef)
    return None

def stmt_typedefs(
    ctx: Context,
    stmt: Statement,
) -> List[str]:
    typedefs = []
    if hasattr(stmt, 'i_typedefs'):
        typedefs += stmt.i_typedefs
    if not stmt.top:
        module: ModSubmodStatement = stmt  # type: ignore
        import_stmt: ImportStatement
        for import_stmt in module.search('import'):
            import_pre: Statement | None = import_stmt.search_one('prefix')
            if not import_pre:
                continue
            revision = None
            import_rev: Statement | None = import_stmt.search_one('revision-date')
            if import_rev:
                revision = import_rev.arg
            imported_stmt = ctx.get_module(import_stmt.arg, revision)
            if imported_stmt:
                if hasattr(imported_stmt, 'i_typedefs'):
                    for typedef in imported_stmt.i_typedefs:
                        typedefs.append(import_pre.arg + ':' + typedef)
    else:
        typedefs += stmt_typedefs(ctx, stmt.parent)
    return typedefs

def generate_substmt_snippet(
    idx: int,
) -> Tuple[str, int]:
    idx += 1
    snippet = '${%d}' % (idx)
    return (snippet, idx)

def generate_stmt_snippet(
    ctx: Context,
    stmt: Statement,
    yangver: str,
    keyword: str,
    idx: int,
    indent: int,

) -> Tuple[str, int]:
    idx += 1

    (argtype, _) = grammar.stmt_map[keyword]

    # statement argument placeholder fragment
    if argtype in yang._non_quote_arg_type:  #pylint: disable=protected-access
        quote = ''
    elif argtype in yang._keyword_prefer_single_quote_arg:  #pylint: disable=protected-access
        quote = "'"
    else:
        quote = '"'
    try:
        placeholder = ':' + keyword_arg_detail[keyword]
    except KeyError:
        match keyword:
            case 'type':
                placeholder = '|'
                for type_spec in types.yang_type_specs:
                    placeholder += type_spec + ','
                for typedef in stmt_typedefs(ctx, stmt):
                    placeholder += typedef + ','
                placeholder = placeholder.rstrip(',')
                placeholder += '|'
            case _:
                placeholder = ''
    abs_pre = ''
    (argtype, _) = grammar.stmt_map[keyword]
    if argtype == 'absolute-schema-nodeid':
        abs_pre = '/'
    argument = '%s%s${%d%s}%s' % (quote, abs_pre, idx, placeholder, quote)
    substmts = ''

    # statement substatements placeholder fragment
    def substmt_snippet(snippet: str) -> str:
        return INDENT_STEP * ' ' + snippet + '\n'

    for substmt in mandatory_substmt_keywords(yangver, keyword):
        if not maybe_substatements(substmt):
            (snippet, idx) = generate_stmt_snippet(ctx, stmt, yangver, substmt, idx, indent + INDENT_STEP)
        else:
            (snippet, idx) = generate_substmt_snippet(idx)
        substmts += substmt_snippet(snippet)
    if keyword in lint._required_substatements:  #pylint: disable=protected-access
        (req_substmts, _rfc, _uri) = lint._required_substatements[keyword]  #pylint: disable=protected-access
        for substmt in req_substmts:
            (snippet, idx) = generate_stmt_snippet(ctx, stmt, yangver, substmt, idx, indent + INDENT_STEP)
            substmts += substmt_snippet(snippet)
    elif keyword in lint._recommended_substatements:  #pylint: disable=protected-access
        (rec_substmts, _rfc, _uri) = lint._recommended_substatements[keyword]  #pylint: disable=protected-access
        for substmt in rec_substmts:
            (snippet, idx) = generate_stmt_snippet(ctx, stmt, yangver, substmt, idx, indent + INDENT_STEP)
            substmts += substmt_snippet(snippet)

    match keyword:
        case 'deviate':
            substmts = (indent + INDENT_STEP) * ' ' + '%s${%d%s}%s\n' % ('', idx + 1, '', '')

    if substmts:
        sub = ' {\n' + substmts + '}'
    else:
        sub = ';'

    argsep = ' '
    if keyword in yang._force_newline_arg:  #pylint: disable=protected-access
        argsep = '\n' + (INDENT_STEP * 2) * ' '

    return (keyword + argsep + argument + sub, idx)

def create_item(
    label,
    label_detail,
    label_description,
    edit_range,
    edit_new_text,
    preselect: bool = False,
    sort_idx: int | None = None,
    kind: lsp.CompletionItemKind = lsp.CompletionItemKind.Snippet,
    text_format: lsp.InsertTextFormat = lsp.InsertTextFormat.Snippet,
    add_text_edits: List[lsp.TextEdit] | None = None,
) -> lsp.CompletionItem:
    sort_text=None
    if sort_idx:
        sort_text=f'{sort_idx:03d}'
    return lsp.CompletionItem(
        label=label,
        label_details=lsp.CompletionItemLabelDetails(
            detail=label_detail,
            description=label_description,
        ),
        kind=kind,
        tags=[],
        detail=label_detail,
        documentation=lsp.MarkupContent(
            kind=lsp.MarkupKind.Markdown,
            value=label_description,
        ),
        preselect=preselect,
        sort_text=sort_text,
        filter_text=None,
        insert_text=None,
        insert_text_format=text_format,
        insert_text_mode=lsp.InsertTextMode.AdjustIndentation,
        text_edit=lsp.TextEdit(
            range=edit_range,
            new_text=edit_new_text,
        ),
        text_edit_text=None,
        additional_text_edits=add_text_edits,
        commit_characters=None,
        command=None,
        data=None,
    )

def create_keyword_item(
    ctx: Context,
    stmt: Statement,
    yangver: str,
    position: lsp.Position,
    keyword: str,
    indent: int,
) -> lsp.CompletionItem:
    try:
        kind = lsp.CompletionItemKind.Snippet
        label_detail = rfcref.rfcref_stmt_map[keyword]['title']
        label_description = rfcref.rfcref_stmt_map[keyword]['uri']
    except KeyError:
        kind = lsp.CompletionItemKind.Keyword
        label_detail = keyword + ' label detail TBD'
        label_description = keyword + ' label description TBD'
    if not maybe_substatements(keyword):
        (snippet, _idx) = generate_stmt_snippet(ctx, stmt, yangver, keyword, 0, indent)
    else:
        (snippet, _idx) = generate_substmt_snippet(0)
    edit_new_text = snippet
    label = keyword
    edit_range = lsp.Range(
        start=position,
        end=position,
    )
    return create_item(
        label=label,
        label_detail=label_detail,
        label_description=label_description,
        kind=kind,
        edit_range=edit_range,
        edit_new_text=edit_new_text,
    )

implicit_props = [
    'config',
    'mandatory',
    'min-elements',
    'max-elements',
]
"""Implicit node properties wherever applicable"""

def build_list(
    ctx: Context,
    module: ModSubmodStatement,
    position: lsp.Position,
) -> List[lsp.CompletionItem] | None:
    comp_items = []
    stmt_match = glue.stmt_from_lsp_position(module, position)
    if not stmt_match:
        return None
    (stmt, match) = stmt_match
    stmt_depth = 0
    stmt_ptr = stmt
    while stmt_ptr.top:
        stmt_ptr = stmt_ptr.parent
        stmt_depth += 1
    indent = stmt_depth * INDENT_STEP
    match match:
        case 'sub':
            (_, substmt_props) = grammar.stmt_map[stmt.keyword]
            yangver = module.i_version
            def append_comp_keyword_item(keyword: str, cardinality: str) -> None:
                substmts = stmt.search(keyword)
                if not max_one(cardinality) or not substmts:
                    comp_items.append(
                        create_keyword_item(
                            ctx, stmt, yangver, position, keyword, indent))
            for substmt_prop in substmt_props:
                match substmt_prop:
                    case ('$choice', choice_lists):
                        choice_filtered = False
                        for choice_list in choice_lists:
                            for keyword, cardinality in choice_list:
                                if stmt.search_one('keyword'):
                                    choice_filtered = True
                                else:
                                    append_comp_keyword_item(keyword, cardinality)
                            if choice_filtered:
                                break
                        continue
                    case ('$interleave', interleave_list):
                        for interleave_prop in interleave_list:
                            match interleave_prop:
                                case ('$1.1', (keyword, cardinality)):
                                    if yangver == '1':
                                        continue
                                case (keyword, cardinality):
                                    pass
                                case _:
                                    continue
                            append_comp_keyword_item(keyword, cardinality)
                        continue
                    case ((mod, keyword), cardinality):
                        if not module.search('import', arg=mod):
                            continue
                    case ('$1.1', (keyword, cardinality)):
                        if yangver == '1':
                            continue
                    case (keyword, cardinality):
                        if stmt.keyword == 'deviate':
                            if keyword in implicit_props and not stmt.arg == 'replace':
                                continue
                        if stmt.keyword == 'deviation' and keyword == 'deviate':
                            comp_items.append(
                                create_item(
                                    label='deviate not-supported;',
                                    label_detail='label_detail',
                                    label_description='label_description',
                                    edit_range=lsp.Range(start=position, end=position),
                                    edit_new_text='deviate not-supported;',
                                    text_format=lsp.InsertTextFormat.PlainText,
                                    kind=maps.keyword_lsp_kind[stmt.keyword]['completion']
                                )
                            )
                            continue
                        if keyword == '$cut':
                            continue
                    case _:
                        continue
                append_comp_keyword_item(keyword, cardinality)
        case 'stmt' | 'arg':
            if match == 'stmt' and stmt.keyword in yang._need_quote:  #pylint: disable=protected-access
                return None
            if not match == 'stmt' or not stmt.arg:
                edit_range = lsp.Range(start=position, end=position)
            else:
                edit_range = glue.arg_lsp_selection_range(stmt.pos)
            match stmt.keyword:
                case 'yang-version':
                    for version in ['1.1', '1']:
                        comp_items.append(
                            create_item(
                                label=version,
                                label_detail='',
                                label_description='',
                                preselect=version == '1.1',
                                kind=lsp.CompletionItemKind.Constant,
                                text_format=lsp.InsertTextFormat.PlainText,
                                edit_range=edit_range,
                                edit_new_text=version,
                            )
                        )
                case 'prefix':
                    if stmt.parent.keyword == 'import':
                        for mod in ctx.modules.values():
                            if mod.arg == stmt.parent.arg:
                                label: str = mod.i_prefix  # type: ignore
                                label_detail = 'prefix'
                                label_description = 'test_label_description'
                                edit_new_text = label
                                comp_items = [
                                    create_item(
                                        label=label,
                                        label_detail=label_detail,
                                        label_description=label_description,
                                        edit_range=edit_range,
                                        edit_new_text=edit_new_text,
                                        kind=lsp.CompletionItemKind.Reference,
                                        text_format=lsp.InsertTextFormat.PlainText,
                                    )
                                ]
                                break
                case 'import' | 'include':
                    for mod in ctx.modules.values():
                        label: str = mod.arg  # type: ignore
                        label_detail = 'module'
                        label_description = 'test_label_description'
                        edit_new_text = label
                        comp_items.append(
                            create_item(
                                label=label,
                                label_detail=label_detail,
                                label_description=label_description,
                                edit_range=edit_range,
                                edit_new_text=edit_new_text,
                                kind=lsp.CompletionItemKind.Module,
                                text_format=lsp.InsertTextFormat.PlainText
                            )
                        )
                case 'if-feature':
                    def append_feature_item(feature):
                        label = feature
                        label_detail = 'feature'
                        label_description = 'test_label_description'
                        edit_new_text = label
                        comp_items.append(
                            create_item(
                                label=label,
                                label_detail=label_detail,
                                label_description=label_description,
                                kind=lsp.CompletionItemKind.Constant,
                                text_format=lsp.InsertTextFormat.PlainText,
                                edit_range=edit_range,
                                edit_new_text=edit_new_text,
                            )
                        )
                    for feature in module.i_features:
                        if feature == stmt.parent.arg:
                            # circular dependency
                            continue
                        append_feature_item(feature)
                    import_stmt: ImportStatement
                    for import_stmt in module.search('import'):
                        import_pre: Statement | None = import_stmt.search_one('prefix')
                        if not import_pre:
                            continue
                        revision = None
                        import_rev: Statement | None = import_stmt.search_one('revision-date')
                        if import_rev:
                            revision = import_rev.arg
                        imported_stmt = ctx.get_module(import_stmt.arg, revision)
                        if imported_stmt:
                            for feature in imported_stmt.i_features:
                                append_feature_item(import_pre.arg + ':' + feature)
                case 'type':
                    sort_idx = 0
                    for type_spec in types.yang_type_specs:
                        sort_idx += 1
                        comp_items.append(
                            create_item(
                                label=type_spec,
                                label_detail='',
                                label_description='',
                                edit_range=edit_range,
                                edit_new_text=type_spec,
                                sort_idx=sort_idx,
                                kind=maps.type_lsp_kind[type_spec]['completion'],
                                text_format=lsp.InsertTextFormat.PlainText,
                            )
                        )
                    for typedef in stmt_typedefs(ctx, stmt):
                        if stmt.parent.keyword == 'typedef' and stmt.parent.arg == typedef:
                            continue
                        sort_idx += 1
                        comp_items.append(
                            create_item(
                                label=typedef,
                                label_detail='',
                                label_description='',
                                edit_range=edit_range,
                                edit_new_text=typedef,
                                sort_idx=sort_idx,
                                kind=lsp.CompletionItemKind.TypeParameter,
                                text_format=lsp.InsertTextFormat.PlainText,
                            )
                        )
        case _:
            return None
    return comp_items
