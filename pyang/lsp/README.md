# LSP TODO

## Server Capabilities

### Document Synchronization

#### Text Document

- [x] [Did Open Text Document][textDocument_didOpen]
- [x] [Did Change Text Document][textDocument_didChange]
- [ ] [Will Save Text Document][textDocument_willSave]
- [ ] [Will Save Document Wait Until][textDocument_willSaveWaitUntil]
- [ ] [Did Save Text Document][textDocument_didSave]
- [x] [Did Close Text Document][textDocument_didClose]
- [x] [Rename a Text Document][textDocument_didClose]

#### Notebook Document

> *Not Applicable to YANG*

### Language Features

#### Go to Declaration

- [ ] ~~[declarationProvider][textDocument_declaration]~~ <-- *Not Applicable to YANG*

#### Go to Definition

- [ ] [definitionProvider][textDocument_definition]
  - [x] `import`
  - [x] `uses`
  - [x] `if-feature`
  - [x] `type`
  - [ ] `key`
  - [ ] `path` <-- *xpath traversal*
  - [ ] `augment` <-- *xpath traversal*
  - [ ] `deviation` <-- *xpath traversal*
  - [ ] `when` <-- *xpath traversal*
  - [ ] `must` <-- *xpath traversal*

#### Go to Type Definition

- [x] [typeDefinitionProvider][textDocument_typeDefinition]
  - [x] `type`

#### Go to Implementation

- [ ] ~~[implementationProvider][textDocument_implementation]~~ <-- *Not Applicable to YANG*

#### Find References

- [ ] [referencesProvider][textDocument_references]
  - [x] `grouping`
    - [x] `uses`
  - [x] `module`
    - [x] `import`
  - [ ] `submodule`
    - [ ] `include`
  - [x] `feature`
    - [x] `if-feature`
  - [ ] `container` <-- *xpath traversal*
    - [ ] `augment`
    - [ ] `deviation`
  - [ ] `list` <-- *xpath traversal*
    - [ ] `augment`
    - [ ] `deviation`
  - [ ] `leaf` <-- *xpath traversal*
    - [ ] `path`
    - [ ] `when`
    - [ ] `must`
    - [ ] `deviation`
  - [ ] `leaf-list` <-- *xpath traversal*
    - [ ] `deviation`

#### Call Hierarchy

- [ ] [callHierarchyProvider][textDocument_prepareCallHierarchy]
  - [ ] `import`
    - [ ] `module`
  - [ ] `include`
    - [ ] `submodule`
  - [ ] `augment` <-- *xpath traversal*
    - [ ] `container`
    - [ ] `list`
  - [ ] `deviation` <-- *xpath traversal*
    - [ ] `container`
    - [ ] `list`
    - [ ] `leaf`
    - [ ] `leaf-list`

#### Type Hierarchy

- [ ] [typeHierarchyProvider][textDocument_prepareTypeHierarchy]
  - [ ] `typedef`
  - [ ] `identity`

#### Document Highlight

- [ ] [documentHighlightProvider][textDocument_documentHighlight]
  - [x] keywords
  - [ ] arguments
    - [ ] Selected symbol
      - [x] Non-xpath traversal
      - [ ] xpath traversal
    - [ ] Other symbols

#### Document Link

- [ ] [documentLinkProvider][textDocument_documentLink]

#### Hover

- [ ] [hoverProvider][textDocument_hover]
  - [ ] keywords
    - [x] YANG RFC
      - [x] RFC URIs
    - [ ] YANG Extensions
      - [ ] `argument`
      - [ ] `description`
  - [ ] arguments
    - [x] Own
      - [x] `description`
      - [x] `reference`
    - [x] Reference
      - [x] `description`
      - [x] `reference`

#### Code Lens

- [ ] [codeLensProvider][textDocument_codeLens]
  - [ ] [resolveProvider][codeLensOptions]
  - [ ] [workspace.codeLens][codeLens_refresh] <-- *Config Change Use Case*

#### Folding Range

- [ ] [foldingRangeProvider][textDocument_foldingRange]

#### Selection Range

- [ ] [selectionRangeProvider][textDocument_selectionRange]

#### Document Symbols

- [ ] [documentSymbolProvider][textDocument_documentSymbol]
  - [ ] Debug undigested model outlines
  - [ ] Fix `config` marker in detail
  - [ ] Fix `default` marker in detail

#### Semantic Tokens

- [ ] [semanticTokensProvider][textDocument_semanticTokens]

#### Inline Value

- [ ] [inlineValueProvider][textDocument_inlineValue]

#### Inlay Hint

- [ ] [inlayHintProvider][textDocument_inlayHint]

#### Monikers

- [ ] [monikerProvider][textDocument_moniker]

#### Completion

- [ ] [completionProvider][textDocument_completion]

#### Diagnostics

##### Publish Diagnostics

- [x] [textDocument.publishDiagnostics][textDocument_publishDiagnostics]

##### Pull Diagnostics

- [x] [diagnosticProvider][textDocument_pullDiagnostics]

#### Signature Help

- [ ] [signatureHelpProvider][textDocument_signatureHelp]

#### Code Action

- [ ] [codeActionProvider][textDocument_codeAction]

#### Document Color

- [ ] [codeActionProvider][textDocument_documentColor]

#### Formatting

##### Full Document Formatting

- [x] [documentFormattingProvider][textDocument_formatting]

##### Range Formatting

- [ ] [documentRangeFormattingProvider][textDocument_rangeFormatting]

##### On Type Formatting

- [ ] [documentOnTypeFormattingProvider][textDocument_onTypeFormatting]

#### Rename

- [ ] [renameProvider][textDocument_rename]

#### Linked Editing Range

- [ ] [linkedEditingRangeProvider][textDocument_linkedEditingRange]

### Workspace

#### Workspace Symbols

- [ ] [workspaceSymbolProvider][textDocument_linkedEditingRange]
  - [x] Without resolve
  - [ ] With resolve

#### Configuration

#### Workspace Folders

#### Execute Command

#### Apply Edit

---

[textDocument_declaration]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_declaration
[textDocument_definition]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_definition
[textDocument_typeDefinition]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_typeDefinition
[textDocument_implementation]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_implementation
[textDocument_references]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_references
[textDocument_prepareCallHierarchy]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_prepareCallHierarchy
[textDocument_prepareTypeHierarchy]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_prepareTypeHierarchy
[textDocument_documentHighlight]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentHighlight
[textDocument_documentLink]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentLink
[textDocument_hover]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover
[textDocument_codeLens]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_codeLens
[codeLensOptions]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#codeLensOptions
[codeLens_refresh]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#codeLens_refresh
[textDocument_foldingRange]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_foldingRange
[textDocument_selectionRange]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_selectionRange
[textDocument_documentSymbol]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentSymbol
[textDocument_semanticTokens]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens
[textDocument_inlineValue]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_inlineValue
[textDocument_inlayHint]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_inlayHint
[textDocument_moniker]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_moniker
[textDocument_completion]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_completion
[textDocument_publishDiagnostics]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_publishDiagnostics
[textDocument_pullDiagnostics]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_pullDiagnostics
[textDocument_signatureHelp]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_signatureHelp
[textDocument_codeAction]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_codeAction
[textDocument_documentColor]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentColor
[textDocument_formatting]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_formatting
[textDocument_rangeFormatting]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_rangeFormatting
[textDocument_onTypeFormatting]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_onTypeFormatting
[textDocument_rename]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_rename
[textDocument_linkedEditingRange]: https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_linkedEditingRange

<!-- markdownlint-disable-file MD052 -->
