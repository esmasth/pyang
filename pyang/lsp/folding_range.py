"""LSP Folding Range Provider

* `textDocument/foldingRange`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_foldingRange
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang import grammar
from pyang.error import Position
from pyang.lsp import common
from pyang.statements import ModSubmodStatement, Statement

def _stmt_ranges(stmt: Statement) -> List[lsp.FoldingRange]:
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
                kind=None,
                collapsed_text=None,
            )
        )
        for substmt in stmt.substmts:
            ranges.extend(_stmt_ranges(substmt))
    else:
        if stmt.keyword in [s for s, _ in grammar.meta_stmts] + ['_comment'] \
                and pos.stmt_sline != pos.stmt_eline:
            ranges.append(
                lsp.FoldingRange(
                    start_line=pos.stmt_sline,
                    start_character=pos.stmt_schar + 1,
                    end_line=pos.stmt_eline,
                    end_character=pos.stmt_echar,
                    kind=lsp.FoldingRangeKind.Comment,
                    collapsed_text=None,
                )
            )
    return ranges

def _imports_ranges(module: ModSubmodStatement) -> List[lsp.FoldingRange]:
    ranges = []
    stmt: Statement
    in_range = False
    for stmt in module.substmts:
        pos: Position = stmt.pos
        if stmt.keyword in \
                [s for s, _ in \
                    grammar.module_header_stmts + \
                    grammar.submodule_header_stmts + \
                    grammar.linkage_stmts + \
                    grammar.revision_stmts + \
                    grammar.meta_stmts]:
            if not in_range:
                start_line = pos.stmt_sline
                start_character = None
                in_range = True
            end_line = pos.stmt_eline
            end_character = None
        else:
            if in_range:
                if isinstance(stmt.keyword, tuple):
                    end_line = pos.stmt_eline
                    end_character = None
                    continue
                in_range = False
                ranges.append(
                    lsp.FoldingRange(
                        start_line=start_line,
                        start_character=start_character,
                        end_line=end_line,
                        end_character=end_character,
                        kind=lsp.FoldingRangeKind.Imports,
                        collapsed_text=None,
                    )
                )
    return ranges


def text_document_folding_range(
    ls: LanguageServer,
    params: lsp.FoldingRangeParams,
) -> Union[List[lsp.FoldingRange], None]:
    """Handles LSP `textDocument/foldingRange` request."""
    if not ls.client_capabilities.text_document or \
        not ls.client_capabilities.text_document.folding_range:
        return None

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None
    ranges = []
    ranges.extend(_stmt_ranges(module))
    ranges.extend(_imports_ranges(module))
    return ranges


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_FOLDING_RANGE)(text_document_folding_range)
