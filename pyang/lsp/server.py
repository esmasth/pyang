"""pyang LSP Server"""

from __future__ import absolute_import
import optparse  #pylint: disable=deprecated-module
import os
from types import ModuleType
from typing import Any, List
import importlib
import logging

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.workspace import TextDocument
from pygls.uris import from_fs_path, to_fs_path

from pyang import context, plugin, syntax
from pyang.statements import ModSubmodStatement, Statement

from . import (
    common,
    code_lens,
    completion,
    cross_reference,
    diagnostics,
    document_highlight,
    document_link,
    folding_range,
    formatting,
    hover,
    inlay_hint,
    inline_value,
    semantic_tokens,
    symbols,
)

ext_deps = ['pygls']
def try_import_deps():
    """Raises `ModuleNotFoundError` if external module dependencies are missing"""
    for dep in ext_deps:
        importlib.import_module(dep)

SERVER_NAME = "pyang"
SERVER_VERSION = "v0.1"

SERVER_MODE_IO = "io"
SERVER_MODE_TCP = "tcp"
SERVER_MODE_WS = "ws"
supported_modes = [
    SERVER_MODE_IO,
    SERVER_MODE_TCP,
    SERVER_MODE_WS,
]
default_mode = SERVER_MODE_IO
default_host = "127.0.0.1"
default_port = 2087

class PyangLanguageServer(LanguageServer):
    def __init__(self):
        self.ctx : context.Context
        self.modules : dict[str, ModSubmodStatement] = {}
        self.doc_symbols : dict[str, List[lsp.DocumentSymbol] | None] = {}
        self.diagnostics : dict[str, List[lsp.Diagnostic] | None] = {}
        self.handlers: List[ModuleType] = []

        super().__init__(
            name=SERVER_NAME,
            version=SERVER_VERSION,
            text_document_sync_kind=lsp.TextDocumentSyncKind.Full
        )

logging.basicConfig(filename='pyang-ls.log', filemode='w', level=logging.DEBUG)

pyangls = PyangLanguageServer()

code_lens.register_callbacks(pyangls)
completion.register_callbacks(pyangls)
cross_reference.register_callbacks(pyangls)
diagnostics.register_callbacks(pyangls)
document_highlight.register_callbacks(pyangls)
document_link.register_callbacks(pyangls)
folding_range.register_callbacks(pyangls)
formatting.register_callbacks(pyangls)
hover.register_callbacks(pyangls)
inlay_hint.register_callbacks(pyangls)
inline_value.register_callbacks(pyangls)
symbols.register_callbacks(pyangls)
semantic_tokens.register_callbacks(pyangls)

def add_opts(optparser: optparse.OptionParser):
    optlist = [
        # use capitalized versions of std options help and version
        optparse.make_option("--lsp-config-schema",
                             dest="lsp_config_schema",
                             action="store_true",
                             help="Generate JSON schema for supported errors " \
                                 "and warnings as per the plugins and option " \
                                 "codes and exit."),
        optparse.make_option("--lsp-mode",
                             dest="pyangls_mode",
                             default=default_mode,
                             metavar="LSP_MODE",
                             help="Provide LSP Service in this mode" \
                             "Supported LSP server modes are: " +
                             ', '.join(supported_modes)),
        optparse.make_option("--lsp-host",
                             dest="pyangls_host",
                             default=default_host,
                             metavar="LSP_HOST",
                             help="Bind LSP Server to this address"),
        optparse.make_option("--lsp-port",
                             dest="pyangls_port",
                             type="int",
                             default=default_port,
                             metavar="LSP_PORT",
                             help="Bind LSP Server to this port"),
        ]
    g = optparser.add_option_group("LSP Server specific options")
    g.add_options(optlist)

def gen_config_schema():
    return

def start_server(optargs, ctx: context.Context):
    pyangls.ctx = ctx
    if optargs.pyangls_mode == SERVER_MODE_TCP:
        pyangls.start_tcp(optargs.pyangls_host, optargs.pyangls_port)
    elif optargs.pyangls_mode == SERVER_MODE_WS:
        pyangls.start_ws(optargs.pyangls_host, optargs.pyangls_port)
    else:
        pyangls.start_io()

def _delete_from_ctx(text_doc: TextDocument):
    if not pyangls.modules:
        return
    try:
        module = pyangls.modules[text_doc.uri]
    except KeyError:
        return
    pyangls.ctx.del_module(module)
    del pyangls.modules[text_doc.uri]

def _add_to_ctx(text_doc: TextDocument):
    assert text_doc.filename
    m = syntax.re_filename.search(text_doc.filename)
    if m is not None:
        name, rev, in_format = m.groups()
        assert in_format == 'yang'
        module = pyangls.ctx.add_module(text_doc.path, text_doc.source,
                                        in_format, name, rev,
                                        expect_failure_error=False,
                                        primary_module=True)
    else:
        module = pyangls.ctx.add_module(text_doc.path, text_doc.source,
                                        primary_module=True)
    if module:
        pyangls.modules[text_doc.uri] = module
    return module

def _update_ctx_modules():
    for text_doc in pyangls.workspace.documents.values():
        _delete_from_ctx(text_doc)
    for text_doc in pyangls.workspace.documents.values():
        _add_to_ctx(text_doc)

def _clear_stmt_validation(stmt: Statement):
    stmt.i_is_validated = False
    substmt : Statement
    for substmt in stmt.substmts:
        _clear_stmt_validation(substmt)

def _clear_ctx_validation():
    pyangls.doc_symbols = {}
    pyangls.diagnostics = {}
    # pyangls.ctx.internal_reset()
    pyangls.ctx.errors = []
    module : Statement
    for module in pyangls.ctx.modules.values():
        module.internal_reset()
        # _clear_stmt_validation(module)

def _validate_ctx_modules():
    # ls.show_message_log("Validating YANG...")
    modules = common.get_ctx_modules(pyangls.ctx)

    p : plugin.PyangPlugin

    for p in plugin.plugins:
        p.pre_validate_ctx(pyangls.ctx, modules)

    pyangls.ctx.validate()

    for _m in modules:
        _m.prune()

    for p in plugin.plugins:
        p.post_validate_ctx(pyangls.ctx, modules)

def _get_folder_yang_uris(folder_uri) -> List[str]:
    """Recursively find all .yang files in the given folder."""
    folder = to_fs_path(folder_uri)
    assert folder
    yang_files = []
    for root, _, files in os.walk(folder):
        file : str
        for file in files:
            if file.endswith(".yang") and not file.startswith('.#'):
                yang_files.append(from_fs_path(os.path.join(root, file)))
    return yang_files

def _process_workspace_configuration(_scope: str | None, _config: List[Any]):
    pass


################################################################################
#-------------------------------------------------------------------------------
# LSP Lifecycle Messages
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.INITIALIZED)
def initialized(
    ls: LanguageServer,
    _params: lsp.InitializedParams,
):
    """Handles LSP `initialized` notification."""

    def add_workspace_folder(uri: str):
        _clear_ctx_validation()
        yang_uris = _get_folder_yang_uris(uri)
        for yang_uri in yang_uris:
            if not yang_uri in ls.workspace.text_documents.keys():
                yang_file = to_fs_path(yang_uri)
                assert yang_file
                with open(yang_file, 'r', encoding='utf-8') as file:
                    yang_source = file.read()
                    file.close()
                ls.workspace.put_text_document(
                    lsp.TextDocumentItem(
                        uri=yang_uri,
                        language_id='yang',
                        version=0,
                        text=yang_source,
                    )
                )
        _update_ctx_modules()
        _validate_ctx_modules()
        diagnostics.publish_workspace_diagnostics(ls)

    if ls.workspace.folders:
        # TODO: Handle more than one workspace folder
        folder = next(iter(ls.workspace.folders.values()))
        add_workspace_folder(folder.uri)
    # fallback to pre 3.6.0
    elif ls.workspace.root_uri:
        add_workspace_folder(ls.workspace.root_uri)
    # fallback to pre 3.0
    elif ls.workspace.root_path:
        uri = from_fs_path(ls.workspace.root_path)
        if uri:
            add_workspace_folder(uri)


################################################################################
#-------------------------------------------------------------------------------
# Document Synchronization
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def text_document_did_open(
    ls: LanguageServer,
    params: lsp.DidOpenTextDocumentParams,
):
    """Handles LSP `textDocument/didOpen` notification."""

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    orig_source = text_doc._source

    # Prevent direct file read on next TextDocument.source access
    text_doc._source = params.text_document.text

    if params.text_document.text == orig_source:
        # Some LSP clients like Emacs/eglot do not consume an earlier diagnostic
        # publishing for the
        diagnostics.publish_document_diagnostics(ls, text_doc)
        return

    # File content of opened file is not matching ex
    _clear_ctx_validation()
    _update_ctx_modules()
    _validate_ctx_modules()
    diagnostics.publish_workspace_diagnostics(ls)


# pyang supports LSP `TextDocumentSyncKind` `Full` but not `Incremental`
# The mapping is provided via initialization parameters of pygls LanguageServer
@pyangls.feature(lsp.TEXT_DOCUMENT_DID_CHANGE)
def text_document_did_change(
    ls: LanguageServer,
    params: lsp.DidChangeTextDocumentParams,
):
    """Handles LSP `textDocument/didChange` notification."""

    _clear_ctx_validation()

    for content_change in params.content_changes:
        ls.workspace.update_text_document(params.text_document, content_change)

    _update_ctx_modules()
    _validate_ctx_modules()
    diagnostics.publish_workspace_diagnostics(ls)


@pyangls.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
def text_document_did_close(
    ls: LanguageServer,
    params: lsp.DidCloseTextDocumentParams,
):
    """Handles LSP `textDocument/didClose` notification."""

    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    orig_source = text_doc._source
    # Force text document read from file system on next get_text_document()
    text_doc._source = None
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    # Text document source is now corresponding to the file system

    # If last cached source is not different from file system then return
    if text_doc._source == orig_source:
        return

    # Validation is rerun and textDocument/PublishDiagnostics is resent for all
    # workspace files due to LSP clients such as Emacs/eglot which do not send a
    # textDocument/didChange notification before textDocument/didClose for the
    # case when an edited buffer window is killed without saving so that the
    # project diagnostics are still consistent
    _clear_ctx_validation()
    _update_ctx_modules()
    _validate_ctx_modules()
    diagnostics.publish_workspace_diagnostics(ls)


################################################################################
#-------------------------------------------------------------------------------
# LSP Language Features
#-------------------------------------------------------------------------------
################################################################################


################################################################################
#-------------------------------------------------------------------------------
# Workspace Features
#-------------------------------------------------------------------------------
################################################################################


@pyangls.feature(lsp.WORKSPACE_DID_CHANGE_CONFIGURATION)
def workspace_did_change_configuration(
    ls: PyangLanguageServer,
    params: lsp.DidChangeConfigurationParams,
):
    """Handles LSP `workspace/didChangeConfiguration` request."""

    # TODO: Handle config changes including ignoring additional files/subdirs
    _process_workspace_configuration(None, [params.settings])
    _clear_ctx_validation()

    if ls.workspace.folders:
        # TODO: Handle more than one workspace folder
        folder = next(iter(ls.workspace.folders.values()))
        yang_uris = _get_folder_yang_uris(folder.uri)
        for yang_uri in yang_uris:
            if not yang_uri in ls.workspace.text_documents.keys():
                yang_file = to_fs_path(yang_uri)
                assert yang_file
                with open(yang_file, 'r', encoding='utf-8') as file:
                    yang_source = file.read()
                    file.close()
                ls.workspace.put_text_document(
                    lsp.TextDocumentItem(
                        uri=yang_uri,
                        language_id='yang',
                        version=0,
                        text=yang_source,
                    )
                )

    _update_ctx_modules()

    _validate_ctx_modules()
    diagnostics.publish_workspace_diagnostics(ls)


@pyangls.feature(lsp.WORKSPACE_DID_CHANGE_WATCHED_FILES)
def workspace_did_change_watched_files(
    ls: LanguageServer,
    params: lsp.DidChangeWatchedFilesParams,
):
    """Handles LSP `workspace/didChangeWatchedFiles` notification."""

    _clear_ctx_validation()

    # Process all the Deleted events first to handle renames gracefully
    for event in params.changes:
        if event.type != lsp.FileChangeType.Deleted:
            continue

        text_doc = ls.workspace.get_text_document(event.uri)
        ls.workspace.remove_text_document(text_doc.uri)
        _delete_from_ctx(text_doc)
        diagnostics.publish_document_diagnostics(ls, text_doc, [])

    for event in params.changes:
        if event.type == lsp.FileChangeType.Created:
            yang_file = to_fs_path(event.uri)
            assert yang_file
            with open(yang_file, 'r', encoding='utf-8') as file:
                yang_source = file.read()
                file.close()
            ls.workspace.put_text_document(
                lsp.TextDocumentItem(
                    uri=event.uri,
                    language_id='yang',
                    version=0,
                    text=yang_source,
                )
            )
        elif event.type == lsp.FileChangeType.Changed:
            text_doc = ls.workspace.get_text_document(event.uri)
            text_doc._source = None

    _update_ctx_modules()
    _validate_ctx_modules()
    diagnostics.publish_workspace_diagnostics(ls)


################################################################################
#-------------------------------------------------------------------------------
# Window Features
#-------------------------------------------------------------------------------
################################################################################


################################################################################
