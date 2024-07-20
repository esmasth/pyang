"""LSP Inlay Hint Provider

* `textDocument/inlayHint`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_inlayHint

TODO:
* `inlayHint/resolve`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#inlayHint_resolve
"""

from typing import List, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang.error import Position
from pyang.statements import LeafLeaflistStatement, Statement


def create_item(
    line: int,
    character: int,
    label_value: str,
    label_tooltip_value: str,
    tooltip_value: str,
):
    return lsp.InlayHint(
        position=lsp.Position(
            line=line,
            character=character,
        ),
        label=[
            lsp.InlayHintLabelPart(
                value=label_value,
                tooltip=lsp.MarkupContent(
                    kind=lsp.MarkupKind.Markdown,
                    value=label_tooltip_value,
                ),
                location=None,
                command=None,
            )
        ],
        kind=lsp.InlayHintKind.Parameter,
        text_edits=None,
        tooltip=lsp.MarkupContent(
            kind=lsp.MarkupKind.Markdown,
            value=tooltip_value,
        ),
        padding_left=True,
        padding_right=True,
    )


def stmt_hints(
    stmt: Statement,
) -> List[lsp.InlayHint]:
    hints = []
    position: Position = stmt.pos

    if stmt.substmts:
        line = position.sub_sline
        character = position.sub_schar
    else:
        line = position.stmt_eline
        character = position.stmt_echar

    if hasattr(stmt, 'i_is_key') and isinstance(stmt, LeafLeaflistStatement) and stmt.i_is_key:
        hints.append(
            create_item(
                line=line,
                character=character,
                label_value='key',
                label_tooltip_value='`list` key',
                tooltip_value='`list` key',
            )
        )

    if hasattr(stmt, 'i_config') and stmt.i_config is not None and not stmt.search_one('config'):
        hints.append(
            create_item(
                line=line,
                character=character,
                label_value=f'config {str(stmt.i_config).lower()};',
                label_tooltip_value='implicit `config` property',
                tooltip_value='implicit `config` property',
            )
        )

    match stmt.keyword:
        case 'list':
            if not stmt.search_one('min-elements'):
                min_elements = 0
                hints.append(
                    create_item(
                        line=line,
                        character=character,
                        label_value=f'min-elements {min_elements};',
                        label_tooltip_value='implicit `min-elements` property',
                        tooltip_value='implicit `min-elements` property',
                    )
                )
            if not stmt.search_one('max-elements'):
                max_elements = 'unbounded'
                hints.append(
                    create_item(
                        line=line,
                        character=character,
                        label_value=f'max-elements {max_elements};',
                        label_tooltip_value='implicit `max-elements` property',
                        tooltip_value='implicit `max-elements` property',
                    )
                )

    for substmt in stmt.substmts:
        hints.extend(stmt_hints(substmt))

    return hints


def text_document_inlay_hint(
    ls: LanguageServer,
    params: lsp.InlayHintParams,
) -> Union[List[lsp.InlayHint], None]:
    """Handles LSP `textDocument/inlayHint` request."""
    module = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None
    return stmt_hints(module)


def register_callbacks(ls: LanguageServer):
    ls.feature(
        lsp.TEXT_DOCUMENT_INLAY_HINT,
        lsp.InlayHintOptions(
            resolve_provider=False,
        ),
    )(text_document_inlay_hint)
