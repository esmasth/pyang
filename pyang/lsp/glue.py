"""Glue between lsprotocol and pyang"""

from typing import Tuple

from lsprotocol import types as lsp

from pyang import error, statements


def _match_part_position(
    pos: lsp.Position,
    sline: int,
    schar: int,
    eline: int,
    echar: int,
) -> bool:
    if sline <= pos.line <= eline:
        if sline != eline:
            if (pos.line == sline and schar > pos.character) or \
                    (pos.line == eline and echar <= pos.character):
                return False
            return True
        if schar < pos.character < echar:
            return True
    return False

def stmt_from_lsp_position(
    stmt: statements.Statement,
    position: lsp.Position
) -> Tuple[statements.Statement, str] | None:
    stmt_pos : error.Position = stmt.pos

    # check if cursor was within keyword
    match = _match_part_position(position,
                                 stmt_pos.kwd_sline, stmt_pos.kwd_schar,
                                 stmt_pos.kwd_eline, stmt_pos.kwd_echar)
    if match:
        return (stmt, 'kwd')

    # check if cursor was within argument
    match = _match_part_position(position,
                                 stmt_pos.arg_sline, stmt_pos.arg_schar,
                                 stmt_pos.arg_eline, stmt_pos.arg_echar)
    if match:
        return (stmt, 'arg')

    # check if cursor was within a substatement
    if stmt.substmts:
        for s in stmt.substmts:
            line_stmt = stmt_from_lsp_position(s, position)
            if line_stmt:
                return line_stmt

    # check if statement has substatement space i.e., {...}
    if hasattr(stmt_pos, 'sub_sline') and \
            hasattr(stmt_pos, 'sub_eline') and \
            hasattr(stmt_pos, 'sub_schar') and \
            hasattr(stmt_pos, 'sub_echar'):
        # check if cursor was within substatement space
        match = _match_part_position(position,
                                     stmt_pos.sub_sline, stmt_pos.sub_schar,
                                     stmt_pos.sub_eline, stmt_pos.sub_echar)
        if match:
            return (stmt, 'sub')

    # check if cursor was within i.e., {...}
    match = _match_part_position(position,
                                 stmt_pos.stmt_sline, stmt_pos.stmt_schar,
                                 stmt_pos.stmt_eline, stmt_pos.stmt_echar)
    if match:
        return (stmt, 'stmt')

    return None

def stmt_lsp_range(epos: error.Position) -> lsp.Range:
    return lsp.Range(
        start=lsp.Position(line=epos.stmt_sline, character=epos.stmt_schar),
        end=lsp.Position(line=epos.stmt_eline, character=epos.stmt_echar),
    )

def kwd_lsp_selection_range(epos: error.Position) -> lsp.Range:
    return lsp.Range(
        start=lsp.Position(line=epos.kwd_sline, character=epos.kwd_schar),
        end=lsp.Position(line=epos.kwd_eline, character=epos.kwd_echar),
    )

def arg_lsp_selection_range(epos: error.Position) -> lsp.Range:
    return lsp.Range(
        start=lsp.Position(line=epos.arg_sline, character=epos.arg_schar),
        end=lsp.Position(line=epos.arg_eline, character=epos.arg_echar),
    )

def epos_to_lsp_range(epos: error.Position) -> lsp.Range:
    return lsp.Range(
        start=lsp.Position(line=epos.line - 1, character=0),
        end=lsp.Position(line=epos.line, character=0),
    )
