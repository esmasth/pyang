"""LSP Formatting Provider

* `textDocument/formatting`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_formatting

TODO:
* `textDocument/rangeFormatting`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_rangeFormatting
* `textDocument/onTypeFormatting`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_onTypeFormatting
"""

from typing import List, Union
import tempfile

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.workspace import TextDocument

from pyang.context import Context
from pyang.lsp import server
from pyang.translators import yang
from pyang.workspace import WorkspaceFolderContext
from . import common

yangfmt = yang.YANGPlugin()

# Default Formatting parameters
default_line_length = 80
default_canonical_order = False
default_remove_unused_imports = False
default_remove_comments = False


def _update_ctx_module(ctx: Context, text_doc: TextDocument):
    server._delete_from_ctx(ctx, text_doc)
    return server._add_to_ctx(ctx, text_doc)

def _format_yang(wfc: WorkspaceFolderContext, source: str, opts, module) -> str:
    ls: LanguageServer = wfc.ls # type: ignore
    if opts.insert_spaces is False:
        ls.log_trace("insert_spaces is currently restricted to True")
    if opts.tab_size:
        wfc.ctx.opts.yang_indent_size = opts.tab_size # type: ignore
    if opts.trim_trailing_whitespace is False:
        ls.log_trace("trim_trailing_whitespace is currently restricted to True")
    if opts.trim_final_newlines is False:
        ls.log_trace("trim_final_newlines is currently restricted to True")
    wfc.ctx.opts.yang_canonical = default_canonical_order # type: ignore
    wfc.ctx.opts.yang_line_length = default_line_length # type: ignore
    wfc.ctx.opts.yang_remove_unused_imports = default_remove_unused_imports # type: ignore
    wfc.ctx.opts.yang_remove_comments = default_remove_comments # type: ignore

    yangfmt.setup_fmt(wfc.ctx) # type: ignore
    tmpfd = tempfile.TemporaryFile(mode="w+", encoding="utf-8")

    yangfmt.emit(wfc.ctx, [module], tmpfd) # type: ignore

    tmpfd.seek(0)
    fmt_text = tmpfd.read()
    tmpfd.close()

    # pyang only supports unix file endings and inserts a final one if missing
    if not opts.insert_final_newline and not source.endswith('\n'):
        fmt_text.rstrip('\n')

    return fmt_text


def text_document_formatting(
    ls: LanguageServer,
    params: lsp.DocumentFormattingParams,
) -> Union[List[lsp.TextEdit], None]:
    """Handles LSP `textDocument/formatting` request."""
    if not ls.client_capabilities.text_document or \
        not ls.client_capabilities.text_document.formatting:
        return None

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    source = text_doc.source

    if source is None:
        ls.show_message("No source found")
        return []

    module = _update_ctx_module(wfc.ctx, text_doc)
    if module is None:
        if common.have_parser_errors(wfc.ctx): # type: ignore
            ls.show_message("Document was syntactically invalid. Did not format.",
                            msg_type=lsp.MessageType.Debug)
        return []

    server._validate_ctx_modules(wfc.ctx)

    fmt_text=_format_yang(wfc, source, params.options, module)

    start_pos = lsp.Position(line=0, character=0)
    end_pos = lsp.Position(line=len(text_doc.lines), character=0)
    text_range = lsp.Range(start=start_pos, end=end_pos)

    return [lsp.TextEdit(range=text_range, new_text=fmt_text)]


def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_FORMATTING)(text_document_formatting)
