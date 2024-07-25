"""Common functions to traverse pyang structures"""

from typing import List

from pyang import error, types, util, yang_parser
from pyang.context import Context
from pyang.statements import (
    AugmentStatement,
    DeviationStatement,
    GroupingStatement,
    ImportStatement,
    ModSubmodStatement,
    Statement,
    TypeStatement,
    UsesStatement,
)


def have_parser_errors(ctx: Context) -> bool:
    for _, etag, _ in ctx.errors:
        if etag in yang_parser.errors:
            return True
    return False

def is_top_level_stmt(stmt: Statement) -> bool:
    return stmt.parent == stmt.top

def stmt_from_epos_line(
    line: int,
    stmt: Statement,
    substmts=True,
    i_children=True,
) -> Statement | None:
    """Gets first statement found on 1 indexed line number"""
    pos : error.Position = stmt.pos
    if pos.line == line:
        return stmt
    if substmts and stmt.substmts:
        for s in stmt.substmts:
            line_stmt = stmt_from_epos_line(line, s, substmts, i_children)
            if line_stmt:
                return line_stmt
    if i_children and hasattr(stmt, 'i_children'):
        for s in stmt.i_children:
            line_stmt = stmt_from_epos_line(line, s, substmts, i_children)
            if line_stmt:
                return line_stmt
    return None

ref_map = {
    'uses': 'grouping',
    'key': 'leaf',
    'path': 'leaf',
    'base': 'identity',
    'type': 'typedef',
    'if-feature': 'feature',
}

def referenced_stmt_from_stmt_arg(
    ctx: Context,
    ref: Statement,
) -> Statement | None:
    if not ref.arg:
        return None
    ref_type = ref.keyword
    ref_parts = str(ref.arg).split(':')
    ref_module: ModSubmodStatement | None = None
    if len(ref_parts) == 1:
        ref_name = ref_parts[0]
        ref_module = ref.top
    elif len(ref_parts) == 2:
        ref_prefix = ref_parts[0]
        ref_name = ref_parts[1]
        imp_mods = ref.top.search('import')
        for imp_mod in imp_mods:
            imp_prefix = imp_mod.search_one('prefix')
            if ref_prefix != imp_prefix.arg:
                continue
            revision = None
            imp_revdate = imp_mod.search_one('revision-date')
            if imp_revdate is not None:
                revision = imp_revdate.arg
            ref_module = ctx.get_module(imp_mod.arg, revision)
            if ref_module:
                break
        if not ref_module:
            if ref_prefix == ref.top.i_prefix:
                ref_module = ref.top
    else:
        return None

    def _stmt_from_arg(
        stmt: Statement | None
    ) -> Statement | None:
        if not stmt:
            return None
        if ref_map[ref_type] == stmt.keyword and ref_name == stmt.arg:
            return stmt
        for substmt in stmt.substmts:
            s = _stmt_from_arg(substmt)
            if s:
                return s
        return None

    return _stmt_from_arg(ref_module)

def get_referencing_stmts(
    stmt: Statement,
) -> List[Statement]:
    return stmt.i_referencing_nodes

def get_augmented_stmt(
    augment: AugmentStatement,
) -> Statement | None:
    if hasattr(augment, 'i_target_node'):
        return augment.i_target_node
    return None

def get_refined_stmt(
    refine: Statement,
) -> Statement | None:
    if hasattr(refine, 'i_target_node'):
        return refine.i_target_node  # type: ignore
    return None

def get_deviated_stmt(
    deviation: DeviationStatement,
) -> Statement | None:
    if hasattr(deviation, 'i_target_node'):
        return deviation.i_target_node
    return None

def get_leafrefed_stmt(
    path: Statement,
) -> Statement | None:
    lrt_stmt: TypeStatement = path.parent
    if not lrt_stmt.i_type_spec or not hasattr(lrt_stmt.i_type_spec, 'i_target_node'):
        return None
    return lrt_stmt.i_type_spec.i_target_node

def ext_stmt_from_stmt_kwd(
    ctx: Context,
    ref: Statement,
) -> Statement | None:
    ref_module: ModSubmodStatement | None = None
    match ref.keyword:
        case str():
            ref_name = ref.keyword
            ref_module = ref.top
        case (ref_modulename, ref_name):
            if ref_modulename != ref.top.arg:
                (ref_prefix, _) = ref.raw_keyword
                imp_mods = ref.top.search('import')
                for imp_mod in imp_mods:
                    imp_prefix = imp_mod.search_one('prefix')
                    if ref_prefix != imp_prefix.arg:
                        continue
                    revision = None
                    imp_revdate = imp_mod.search_one('revision-date')
                    if imp_revdate is not None:
                        revision = imp_revdate.arg
                    ref_module = ctx.get_module(imp_mod.arg, revision)
                    if ref_module:
                        break
            else:
                ref_module = ref.top
        case _:
            return None

    def _stmt_from_arg(
        stmt: Statement | None
    ) -> Statement | None:
        if not stmt:
            return None
        if ref_name == stmt.arg:
            return stmt
        for substmt in stmt.substmts:
            s = _stmt_from_arg(substmt)
            if s:
                return s
        return None

    return _stmt_from_arg(ref_module)

def get_reference(stmt: Statement):
    if not stmt.keyword in ['module', 'submodule']:
        refstmt = stmt.search_one('reference')
        if refstmt:
            return refstmt.arg
        return None
    latest_rev = util.get_latest_revision(stmt)
    for revstmt in stmt.search('revision'):
        if revstmt.arg == latest_rev:
            return get_reference(revstmt)
    return None


def find_grouping_uses(
    grouping: GroupingStatement,
    stmt: Statement,
) -> List[UsesStatement]:
    uses: List[UsesStatement] = []
    if hasattr(stmt, 'i_grouping') and stmt.i_grouping == grouping: # type: ignore
        uses.append(stmt) # type: ignore
    for substmt in stmt.substmts:
        uses.extend(find_grouping_uses(grouping, substmt))
    return uses


def find_module_import(
    mod_stmt: ModSubmodStatement,
    module: ModSubmodStatement,
) -> ImportStatement | None:
    substmt: Statement
    for substmt in module.substmts:
        if substmt.keyword == 'import' and substmt.arg == mod_stmt.arg:
            revdate = substmt.search_one('revision-date')
            if revdate and revdate != mod_stmt.i_version:
                continue
            return substmt  # type: ignore
    return None


def find_feature_deps(
    feature: Statement,
    stmt: Statement,
) -> List[Statement]:
    deps = []
    stmts = stmt.search('if-feature', arg=feature.arg)
    if stmts:
        deps.extend(stmts)
    for substmt in stmt.substmts:
        deps.extend(find_feature_deps(feature, substmt))
    return deps


def get_ctx_modules(ctx: Context):
    modules = []
    for k in ctx.modules:
        m = ctx.modules[k]
        if m is not None:
            modules.append(m)
    return modules


def find_stmt_references(
    ctx: Context,
    stmt: Statement
) -> List[Statement]:
    stmt_refs: List[Statement] = []
    for module in get_ctx_modules(ctx):
        match stmt.keyword:
            case 'grouping':
                stmt_refs.extend(find_grouping_uses(stmt, module))  # type: ignore
            case 'module':
                imp = find_module_import(stmt, module)  # type: ignore
                if imp:
                    stmt_refs.append(imp)
            case 'feature':
                stmt_refs.extend(find_feature_deps(stmt, module))  # type: ignore
            case _:
                stmt_refs.extend(get_referencing_stmts(stmt))
                break
        # stmt_refs.extend(find_deviations(stmt, module))  # type: ignore
    # TODO: Add all references in workspace
    return stmt_refs

def get_base_type(ctx: Context, stmt: Statement):
    stmt_type = stmt.search_one('type')
    if stmt_type:
        if stmt_type.arg in types.yang_type_specs:
            return stmt_type.arg
        typedef = referenced_stmt_from_stmt_arg(ctx, stmt_type)
        if typedef:
            return get_base_type(ctx, typedef)
    return None
