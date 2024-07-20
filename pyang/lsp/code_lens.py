"""LSP Code Lens Provider

* `textDocument/codeLens`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_codeLens

TODO:
* `workspace/codeLens/refresh`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#codeLens_refresh
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang.context import Context
from pyang.statements import Statement

from . import common, glue


def text_document_code_lens(
    ls: LanguageServer,
    params: lsp.CodeLensParams,
) -> Union[List[lsp.CodeLens], None]:
    """Handles LSP `textDocument/codeLens` request."""

    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    ctx: Context = ls.ctx # type: ignore
    def stmt_ref_lenses(stmt: Statement):
        lenses: List[lsp.CodeLens] = []
        stmt_ref_count = 0
        stmt_refs = common.find_stmt_references(ctx, stmt)
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
                        params.text_document.uri,
                        stmt_range.start,
                        [],
                    ]
                ),
            )
            lenses.append(stmt_lens)
        for substmt in stmt.substmts:
            lenses.extend(stmt_ref_lenses(substmt))
        return lenses
    return stmt_ref_lenses(module)


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_CODE_LENS)(text_document_code_lens)
