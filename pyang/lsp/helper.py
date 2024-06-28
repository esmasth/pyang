"""Helper functions to traverse pyang structures"""

from pyang import context, error, util
from pyang import statements

def is_top_level_stmt(stmt: statements.Statement) -> bool:
    return stmt.parent == stmt.top

def stmt_from_epos_line(
    line: int,
    stmt: statements.Statement,
    substmts=True,
    i_children=True,
) -> statements.Statement | None:
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

ref_map = {
    'uses': 'grouping',
    'key': 'leaf',
    'path': 'leaf',
    'base': 'identity',
    'type': 'typedef',
    'if-feature': 'feature',
}

def ref_stmt_from_stmt_arg(
    ctx: context.Context,
    ref: statements.Statement,
) -> statements.Statement | None:
    if not ref.arg:
        return
    ref_type = ref.keyword
    ref_parts = str(ref.arg).split(':')
    ref_module: statements.ModSubmodStatement | None = None
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
        return

    def _stmt_from_arg(stmt: statements.Statement | None) -> statements.Statement | None:
        if not stmt:
            return
        if ref_map[ref_type] == stmt.keyword and ref_name == stmt.arg:
            return stmt
        for substmt in stmt.substmts:
            s = _stmt_from_arg(substmt)
            if s:
                return s
        return

    return _stmt_from_arg(ref_module)

def get_augmented_stmt(
    augment: statements.AugmentStatement,
) -> statements.Statement | None:
    return augment.i_target_node

def get_deviated_stmt(
    deviation: statements.DeviationStatement,
) -> statements.Statement | None:
    return deviation.i_target_node

def get_leafrefed_stmt(
    path: statements.Statement,
) -> statements.Statement | None:
    return path.parent.i_type_spec.i_target_node

def ext_stmt_from_stmt_kwd(
    ctx: context.Context,
    ref: statements.Statement,
) -> statements.Statement | None:
    ref_module: statements.ModSubmodStatement | None = None
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
            return

    def _stmt_from_arg(stmt: statements.Statement | None) -> statements.Statement | None:
        if not stmt:
            return
        if ref_name == stmt.arg:
            return stmt
        for substmt in stmt.substmts:
            s = _stmt_from_arg(substmt)
            if s:
                return s
        return

    return _stmt_from_arg(ref_module)

def get_reference(stmt: statements.Statement):
    if not stmt.keyword in ['module', 'submodule']:
        refstmt = stmt.search_one('reference')
        if refstmt:
            return refstmt.arg
        else:
            return None
    else:
        latest_rev = util.get_latest_revision(stmt)
        for revstmt in stmt.search('revision'):
            if revstmt.arg == latest_rev:
                return get_reference(revstmt)
        return None
