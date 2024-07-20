"""Workspace Folder Context"""

from threading import Lock
from typing import List

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang.context import Context

class WorkspaceFolderContext:
    uri: str
    """Folder URI, same as lsprotocol.types.WorkspaceFolder.uri"""
    ls: LanguageServer | None = None
    """LSP Server Context"""
    ctx: Context | None = None
    """pyang Context"""
    _config = {
        'format': {
        },
        'lint': {
        },
    }
    # LSP Server Cache
    _diagnostics: dict[str, List[lsp.Diagnostic]]
    _doc_symbols: dict[str, List[lsp.DocumentSymbol]]
    _wsf_symbols: List[lsp.WorkspaceSymbol]

    def __init__(
        self,
        uri: str,
        ls: LanguageServer,
        ctx: Context,
        _ctx_lock: Lock,
    ):
        self.uri = uri
        self.ls = ls
        self.ctx = ctx
        self._diagnostics = {}
        self._doc_symbols = {}
        self._wsf_symbols = []
        self._ctx_lock = Lock()

    def cache_diagnostics(self, uri: str, diagnostics: List[lsp.Diagnostic]):
        self._diagnostics[uri] = diagnostics

    def diagnostics_cache(self, uri: str) -> List[lsp.Diagnostic]:
        return self._diagnostics[uri]

    def cache_doc_symbols(self, uri: str, symbols: List[lsp.DocumentSymbol]):
        self._doc_symbols[uri] = symbols

    def doc_symbols_cache(self, uri: str) -> List[lsp.DocumentSymbol]:
        return self._doc_symbols[uri]

    def cache_wsf_symbols(self, symbols: List[lsp.WorkspaceSymbol]):
        self._wsf_symbols = symbols

    def wsf_symbols_cache(self) -> List[lsp.WorkspaceSymbol]:
        return self._wsf_symbols
