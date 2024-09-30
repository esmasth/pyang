"""LSP Execute Command Provider

* `workspace/executeCommand`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_executeCommand
"""

import tempfile
from typing import List

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang.error import EmitError
from pyang.lsp import common
from pyang.plugins import tree, uml
from pyang.statements import ModSubmodStatement
from pyang.workspace import WorkspaceFolderContext

treefmt = tree.TreePlugin()
pumlfmt = uml.UMLPlugin()

def _generate_puml(
    wfc: WorkspaceFolderContext,
    module: ModSubmodStatement,
) -> str:
    """Generates YANG PlantUML diagram text."""
    pumlfmt.setup_fmt(wfc.ctx) # type: ignore
    pumlfmt.pre_validate(wfc.ctx, [module]) # type: ignore
    tmpfd = tempfile.TemporaryFile(mode="w+", encoding="utf-8")

    pumlfmt.emit(wfc.ctx, [module], tmpfd) # type: ignore

    tmpfd.seek(0)
    puml_text = tmpfd.read()
    tmpfd.close()

    return puml_text

def generate_puml_diagram(
    ls: LanguageServer,
    args: List[lsp.LSPAny],
):
    """Handles LSP `workspace/executeCommand` request
    for `pyang.generate.puml.diagram` command."""

    if len(args) != 1:
        return
    active_doc_uri = args[0]
    if not active_doc_uri or not active_doc_uri.endswith('.yang'):
        return
    try:
        module = ls.modules[active_doc_uri] # type: ignore
    except KeyError:
        return

    wfc = common.get_workspace_folder_context(ls, active_doc_uri)
    if not wfc:
        return
    text_doc_uri = active_doc_uri + '.puml'
    if not text_doc_uri:
        return

    try:
        text_doc_content = _generate_puml(wfc, module)
    except EmitError:
        ls.show_message(
            message=f"Did not generate PlantUML diagram for \"{active_doc_uri}\"." +
                    "\n\nPlease resolve YANG errors and warnings and try again.",
            msg_type=lsp.MessageType.Warning,
        )
        return

    text_doc_create = lsp.CreateFile(
        uri=text_doc_uri,
        options=lsp.CreateFileOptions(
            overwrite=True,
        ),
    )
    text_doc_id =lsp.OptionalVersionedTextDocumentIdentifier(
        uri=text_doc_uri,
    )
    text_edit = lsp.AnnotatedTextEdit(
        annotation_id='pyang.generate.puml.diagram',
        range=lsp.Range(
            start=lsp.Position(line=0, character=0),
            end=lsp.Position(line=0, character=0),
        ),
        new_text=text_doc_content,
    )
    text_doc_edit = lsp.TextDocumentEdit(
        text_document=text_doc_id,
        edits=[
            text_edit,
        ]
    )
    ls.apply_edit(
        edit=lsp.WorkspaceEdit(
            document_changes=[
                text_doc_create,
                text_doc_edit,
            ]
        )
    )
    ls.show_document(
        params=lsp.ShowDocumentParams(
            uri=text_doc_uri,
            take_focus=True,
        )
    )

def _generate_tree(
    wfc: WorkspaceFolderContext,
    module: ModSubmodStatement,
) -> str:
    """Generates YANG tree diagram text."""
    treefmt.setup_fmt(wfc.ctx) # type: ignore
    tmpfd = tempfile.TemporaryFile(mode="w+", encoding="utf-8")

    treefmt.emit(wfc.ctx, [module], tmpfd) # type: ignore

    tmpfd.seek(0)
    tree_text = tmpfd.read()
    tmpfd.close()

    return tree_text

def generate_tree_diagram(
    ls: LanguageServer,
    args: List[lsp.LSPAny],
):
    """Handles LSP `workspace/executeCommand` request
    for `pyang.generate.tree.diagram` command."""

    if len(args) != 1:
        return
    active_doc_uri = args[0]
    if not active_doc_uri or not active_doc_uri.endswith('.yang'):
        return
    try:
        module = ls.modules[active_doc_uri] # type: ignore
    except KeyError:
        return

    wfc = common.get_workspace_folder_context(ls, active_doc_uri)
    if not wfc:
        return
    text_doc_uri = active_doc_uri + '.ytd'
    if not text_doc_uri:
        return

    try:
        text_doc_content = _generate_tree(wfc, module)
    except EmitError:
        ls.show_message(
            message=f"Did not generate YANG Tree diagram for \"{active_doc_uri}\"." +
                    "\n\nPlease resolve YANG errors and warnings and try again.",
            msg_type=lsp.MessageType.Warning,
        )
        return

    text_doc_create = lsp.CreateFile(
        uri=text_doc_uri,
        options=lsp.CreateFileOptions(
            overwrite=True,
        ),
    )
    text_doc_id =lsp.OptionalVersionedTextDocumentIdentifier(
        uri=text_doc_uri,
    )
    text_edit = lsp.AnnotatedTextEdit(
        annotation_id='pyang.generate.tree.diagram',
        range=lsp.Range(
            start=lsp.Position(line=0, character=0),
            end=lsp.Position(line=0, character=0),
        ),
        new_text=text_doc_content,
    )
    text_doc_edit = lsp.TextDocumentEdit(
        text_document=text_doc_id,
        edits=[
            text_edit,
        ]
    )
    ls.apply_edit(
        edit=lsp.WorkspaceEdit(
            document_changes=[
                text_doc_create,
                text_doc_edit,
            ]
        )
    )
    ls.show_document(
        params=lsp.ShowDocumentParams(
            uri=text_doc_uri,
            take_focus=True,
        )
    )


def register_callbacks(ls: LanguageServer):
    ls.command('pyang.generate.tree.diagram')(generate_tree_diagram)
    ls.command('pyang.generate.puml.diagram')(generate_puml_diagram)
