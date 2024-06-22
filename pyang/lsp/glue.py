"""Glue between lsprotocol and pyang"""

from lsprotocol import types as lsp
from pyang import error


def epos_to_lsp_range(epos: error.Position):
    return lsp.Range(
        start=lsp.Position(line=epos.line - 1, character=0),
        end=lsp.Position(line=epos.line, character=0),
    )
