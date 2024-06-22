"""Utilities to traverse pyang structures"""

from pyang import error
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
