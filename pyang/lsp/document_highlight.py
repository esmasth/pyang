"""LSP Document Highlight Provider

* `textDocument/documentHighlight`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentHighlight
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from . import common, glue


def text_document_document_highlight(
    ls: LanguageServer,
    params: lsp.DocumentHighlightParams,
) -> Union[List[lsp.DocumentHighlight], None]:
    """Handles LSP `textDocument/documentHighlight` request."""

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None
    position = params.position
    match glue.stmt_from_lsp_position(module, position):
        case (stmt, 'kwd'):
            highlight_range = glue.kwd_lsp_selection_range(stmt.pos)
            highlight_kind = lsp.DocumentHighlightKind.Text
        case (stmt, 'arg'):
            highlight_kind = lsp.DocumentHighlightKind.Text
            highlight_range = glue.arg_lsp_selection_range(stmt.pos)
            match stmt.keyword:
                case 'module' | 'submodule' | 'feature':
                    highlight_kind = lsp.DocumentHighlightKind.Write
                case 'import' | 'include' | 'if-feature':
                    highlight_kind = lsp.DocumentHighlightKind.Read
                case 'key':
                    highlight_kind = lsp.DocumentHighlightKind.Read
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
                            if schar <= position.character < echar:
                                break
                            schar += len(key) + 1
                        if hasattr(stmt.parent, 'i_key') and stmt.parent.i_key:
                            for ref_stmt in stmt.parent.i_key:
                                if key == ref_stmt.arg:
                                    break
                        else:
                            # TODO: check why i_key was not populated in some cases
                            for substmt in stmt.parent.substmts:
                                if substmt.keyword == 'leaf' and key == substmt.arg:
                                    ref_stmt = substmt
                                    break
                        highlight_range = lsp.Range(
                            start=lsp.Position(line=stmt.pos.arg_sline, character=schar),
                            end=lsp.Position(line=stmt.pos.arg_eline, character=echar),
                        )
                case 'unique':
                    highlight_kind = lsp.DocumentHighlightKind.Read
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
                            if schar <= position.character < echar:
                                break
                            schar += len(unique) + 1
                        for i_unique in stmt.parent.i_unique:
                            (_, unique_stmts) = i_unique
                            for unique_stmt in unique_stmts:
                                if unique == unique_stmt.arg:
                                    highlight_range = lsp.Range(
                                        start=lsp.Position(
                                            line=stmt.pos.arg_sline,
                                            character=schar
                                        ),
                                        end=lsp.Position(
                                            line=stmt.pos.arg_eline,
                                            character=echar
                                        ),
                                    )
                                    break
        case _:
            return None
    highlight = lsp.DocumentHighlight(
        range=highlight_range,
        kind=highlight_kind,
    )
    # TODO: Add all other highlights in file
    return [highlight]

def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_HIGHLIGHT)(text_document_document_highlight)
