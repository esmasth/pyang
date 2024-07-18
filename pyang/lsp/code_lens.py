from typing import List

from lsprotocol import types as lsp

from pyang.context import Context
from pyang.lsp import glue, helper
from pyang.statements import Statement, ModSubmodStatement

def build_list(
    ctx: Context,
    module: ModSubmodStatement,
    uri: str,
) -> List[lsp.CodeLens]:
    def stmt_ref_lenses(stmt: Statement):
        code_lenses: List[lsp.CodeLens] = []
        stmt_ref_count = 0
        stmt_refs = helper.find_stmt_references(ctx, stmt)
        if stmt_refs:
            stmt_ref_count = len(stmt_refs)
        if stmt_ref_count > 0:
            s = ''
            if stmt_ref_count > 1:
                s = 's'
            stmt_range = glue.stmt_lsp_range(stmt.pos)
            stmt_lens = lsp.CodeLens(
                range=stmt_range,
                command=lsp.Command(
                    title=f'{stmt_ref_count} reference{s}',
                    command='editor.action.showReferences',
                    arguments=[
                        uri,
                        stmt_range.start,
                        [],
                    ]
                ),
            )
            code_lenses.append(stmt_lens)
        for substmt in stmt.substmts:
            code_lenses.extend(stmt_ref_lenses(substmt))
        return code_lenses
    return stmt_ref_lenses(module)
