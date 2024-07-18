from typing import List, Union

from lsprotocol import types as lsp

from pyang.statements import ModSubmodStatement


def build_list(
    module: ModSubmodStatement,
    uri: str,
) -> Union[List[lsp.InlineValueText], None]:
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
