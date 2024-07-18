from typing import List

from lsprotocol import types as lsp

from pyang.error import Position
from pyang.statements import Statement, ModSubmodStatement


def build_list(
    module: ModSubmodStatement,
) -> List[lsp.FoldingRange]:
    def stmt_ranges(stmt: Statement) -> List[lsp.FoldingRange]:
        ranges = []
        pos: Position = stmt.pos
        if stmt.substmts:
            start_line = pos.sub_sline
            end_line = pos.sub_eline
            start_character = pos.sub_schar + 1
            end_character = pos.sub_echar
            ranges.append(
                lsp.FoldingRange(
                    start_line=start_line,
                    start_character=start_character,
                    end_line=end_line,
                    end_character=end_character,
                    kind=lsp.FoldingRangeKind.Region,
                    collapsed_text=None,
                )
            )
            for substmt in stmt.substmts:
                ranges.extend(stmt_ranges(substmt))
        return ranges
    return stmt_ranges(module)
