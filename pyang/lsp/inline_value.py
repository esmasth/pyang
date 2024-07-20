"""LSP Inline Value Provider

* `textDocument/inlineValue`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_inlineValue

TODO:
* `workspace/inlineValue/refresh`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_inlineValue_refresh
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer


def text_document_inline_value(
    ls: LanguageServer,
    params: lsp.InlineValueParams,
) -> Union[List[lsp.InlineValueText], None]:
    """Handles LSP `textDocument/inlineValue` request."""
    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    return [
        lsp.InlineValueText(
            range=lsp.Range(
                start=lsp.Position(
                    line=0,
                    character=0,
                ),
                end=lsp.Position(
                    line=0,
                    character=0,
                ),
            ),
            text='Test Inline Value',
        )
    ]


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_INLINE_VALUE)(text_document_inline_value)
