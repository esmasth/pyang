"""LSP Diagnostics Provider

* `textDocument/publishDiagnostics`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_publishDiagnostics
* `textDocument/diagnostic`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_diagnostic
* `workspace/diagnostic`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_diagnostic
"""

from typing import List

from lsprotocol import types as lsp
from pygls.server import LanguageServer
from pygls.uris import from_fs_path
from pygls.workspace import TextDocument

from pyang import error
from pyang.plugins import lint

pyangls = None

def _build_doc_diagnostics(ls: LanguageServer, ref: str) -> List[lsp.Diagnostic]:
    """Builds lsp diagnostics from pyang context"""
    diagnostics = []
    # TODO: revisit sorting. VS code seems to prefer ordering on line numbers
    ls.ctx.errors.sort(key=lambda e: (e[0].ref, e[0].line), reverse=True) # type: ignore
    for epos, etag, eargs in ls.ctx.errors: # type: ignore
        if epos.ref != ref:
            continue
        msg = error.err_to_str(etag, eargs)

        def epos_to_lsp_range(etag: str, epos: error.Position) -> lsp.Range:
            start_line = epos.arg_sline
            start_col = epos.arg_schar
            end_line = epos.arg_eline
            end_col = epos.arg_echar
            if etag == 'LONG_LINE' and ls.ctx.max_line_len is not None: # type: ignore
                start_line = epos.line - 1
                start_col = ls.ctx.max_line_len # type: ignore
                end_line = epos.line
                end_col = 0
            elif etag == 'LONG_IDENTIFIER' and ls.ctx.max_identifier_len is not None: # type: ignore
                start_col = epos.arg_schar + ls.ctx.max_identifier_len # type: ignore
            elif 'KEYWORD' in etag:
                start_line = epos.kwd_sline
                start_col = epos.kwd_schar
                end_line = epos.kwd_eline
                end_col = epos.kwd_echar
            return lsp.Range(
                start=lsp.Position(line=start_line, character=start_col),
                end=lsp.Position(line=end_line, character=end_col),
            )

        def line_to_lsp_range(etag: str, line: int) -> lsp.Range:
            # pyang just stores line context, not keyword/argument context
            start_line = line - 1
            if etag == 'LONG_LINE' and ls.ctx.max_line_len is not None: # type: ignore
                start_col = ls.ctx.max_line_len # type: ignore
            else:
                start_col = 0
            end_line = line
            end_col = 0
            return lsp.Range(
                start=lsp.Position(line=start_line, character=start_col),
                end=lsp.Position(line=end_line, character=end_col),
            )

        def level_to_lsp_severity(level) -> lsp.DiagnosticSeverity:
            if level == 1 or level == 2:
                return lsp.DiagnosticSeverity.Error
            elif level == 3:
                return lsp.DiagnosticSeverity.Warning
            elif level == 4:
                return lsp.DiagnosticSeverity.Information
            else:
                return lsp.DiagnosticSeverity.Hint

        diag_tags=[]
        rel_info=[]
        unused_etags = [
            'UNUSED_IMPORT',
            'UNUSED_TYPEDEF',
            'UNUSED_GROUPING',
        ]
        duplicate_1_etags = [
            'DUPLICATE_ENUM_NAME',
            'DUPLICATE_ENUM_VALUE',
            'DUPLICATE_BIT_POSITION',
            'DUPLICATE_CHILD_NAME',
        ]
        if etag in unused_etags:
            diag_tags.append(lsp.DiagnosticTag.Unnecessary)
        elif etag in duplicate_1_etags:
            if etag == 'DUPLICATE_ENUM_NAME':
                dup_arg = 1
                dup_msg = 'Original Enumeration'
            elif etag == 'DUPLICATE_ENUM_VALUE':
                dup_arg = 1
                dup_msg = 'Original Enumeration with Value'
            elif etag == 'DUPLICATE_BIT_POSITION':
                dup_arg = 1
                dup_msg = 'Original Bit Position'
            elif etag == 'DUPLICATE_CHILD_NAME':
                dup_arg = 3
                dup_msg = 'Original Child'
            dup_uri = from_fs_path(eargs[dup_arg].ref)
            dup_range = line_to_lsp_range(etag, eargs[dup_arg].line)
            if dup_uri:
                dup_loc = lsp.Location(uri=dup_uri, range=dup_range)
                rel_info.append(lsp.DiagnosticRelatedInformation(location=dup_loc,
                                                             message=dup_msg))
        elif etag == 'DUPLICATE_NAMESPACE':
            # TODO: handle
            pass

        code_desc = None
        (_severity, _fmt, uri) = error.error_codes[etag]
        if uri:
            code_desc = lsp.CodeDescription(href=uri)
        else:
            if etag == 'LINT_MISSING_REQUIRED_SUBSTMT':
                kwd = eargs[1]
                (_stmts, _rfc_sec, uri) = lint._required_substatements[kwd]  #pylint: disable=protected-access
                code_desc = lsp.CodeDescription(href=uri)
            elif etag == 'LINT_MISSING_RECOMMENDED_SUBSTMT':
                kwd = eargs[1]
                (_stmts, _rfc_sec, uri) = lint._recommended_substatements[kwd]  #pylint: disable=protected-access
                code_desc = lsp.CodeDescription(href=uri)

        d = lsp.Diagnostic(
            range=epos_to_lsp_range(etag, epos),
            message=msg,
            severity=level_to_lsp_severity(error.err_level(etag)),
            tags=diag_tags,
            related_information=rel_info,
            code=etag,
            code_description=code_desc,
            source=ls.name,
        )

        diagnostics.append(d)

    return diagnostics

def publish_document_diagnostics(
    ls: LanguageServer,
    text_doc: TextDocument,
    diagnostics: List[lsp.Diagnostic] | None = None
):
    if not ls.client_capabilities.text_document:
        return
    if not ls.client_capabilities.text_document.publish_diagnostics:
        return
    if not diagnostics:
        diagnostics = _build_doc_diagnostics(ls, text_doc.path)
    ls.publish_diagnostics(text_doc.uri, diagnostics)
    ls.diagnostics[text_doc.uri] = diagnostics # type: ignore

def publish_workspace_diagnostics(
    ls: LanguageServer,
):
    for text_doc in ls.workspace.text_documents.values():
        publish_document_diagnostics(ls, text_doc)


# def text_document_diagnostic(
#     params: lsp.DocumentDiagnosticParams,
# ) -> lsp.DocumentDiagnosticReport:
#     """Handles LSP `textDocument/diagnostic` request."""

#     if not (items := pyangls.diagnostics[params.text_document.uri]): # type: ignore
#         text_doc = pyangls.workspace.get_text_document(params.text_document.uri)
#         doc_items = _build_doc_diagnostics(pyangls, text_doc.path)
#         if doc_items is None:
#             items = []
#         else:
#             items = doc_items

#     # TODO: check if there are any errors which provide related diagnostics
#     return lsp.RelatedFullDocumentDiagnosticReport(
#         items=items,
#     )


# def workspace_diagnostic(
#     params: lsp.WorkspaceDiagnosticParams,
# ) -> lsp.WorkspaceDiagnosticReport:
#     """Handles LSP `workspace/diagnostic` request."""
#     if pyangls.client_capabilities.workspace is None or \
#             pyangls.client_capabilities.workspace.diagnostics is None:
#         pyangls.show_message("Unexpected workspace/diagnostic from incapable client.")

#     if params.identifier:
#         pyangls.log_trace(params.identifier)

#     items : List[lsp.WorkspaceDocumentDiagnosticReport] = []
#     for text_doc_uri in pyangls.workspace.text_documents.keys():
#         text_doc = pyangls.workspace.get_text_document(text_doc_uri)
#         doc_items = _build_doc_diagnostics(pyangls, text_doc.path)
#         if doc_items is not None:
#             items.append(
#                 lsp.WorkspaceFullDocumentDiagnosticReport(
#                     uri=text_doc.uri,
#                     version=text_doc.version,
#                     items=doc_items,
#                     kind=lsp.DocumentDiagnosticReportKind.Full,
#                 )
#             )

#     return lsp.WorkspaceDiagnosticReport(items=items)


def register_callbacks(ls: LanguageServer):
    # ls.feature(
    #     lsp.TEXT_DOCUMENT_DIAGNOSTIC,
    #     lsp.DiagnosticOptions(
    #         identifier=ls.name,
    #         inter_file_dependencies=True,
    #         workspace_diagnostics=True,
    #     ),
    # )(text_document_diagnostic)
    # ls.feature(lsp.WORKSPACE_DIAGNOSTIC)(workspace_diagnostic)
    pass
