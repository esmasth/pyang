"""YANG Definitions to LSP Kind Maps"""

from lsprotocol import types as lsp

type_map = {
    'uint8': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'uint16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'uint32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'uint64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'int8': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'int16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'int32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'int64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'decimal64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'string': {
        'symbol'    : lsp.SymbolKind.String,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'boolean': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'enumeration': {
        'symbol'    : lsp.SymbolKind.Enum,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'bits': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'binary': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'union': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'leafref': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'identityref': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'instance-identifier': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'empty': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
}
"""YANG `type` mapping to LSP

Following property keys are present
* `symbol`: LSP `SymbolKind`
* `completion`: LSP `CompletionItemKind`
"""

keyword_map = {
    'module': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
    },
    'submodule': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
    },
    'yang-version': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'revision': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'contact': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'organization': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'description': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'reference': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'base': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'namespace': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'prefix': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'feature': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Constant,
    },
    'if-feature': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'when': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'must': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'choice': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'case': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'grouping': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.Struct,
    },
    'extension': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'key': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
    },
    'identity': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
    },
    'typedef': {
        'symbol'    : lsp.SymbolKind.TypeParameter,
        'completion': lsp.CompletionItemKind.TypeParameter,
    },
    'container': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
    },
    'list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Field,
    },
    'leaf-list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Field,
    },
    'rpc': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
    },
    'action': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
    },
    'input': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'output': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'notification': {
        'symbol'    : lsp.SymbolKind.Event,
        'completion': lsp.CompletionItemKind.Event,
    },
    'enum': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
    },
    'value': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
    },
    'anyxml': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
    },
    'anydata': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
    },
    'augment': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'deviation': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'deviate': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
    },
    'config': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'mandatory': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'max-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'min-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'default': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'uses': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
    },
    'argument': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'status': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'ordered-by': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
    },
    'import': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Reference,
    },
    'include': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Reference,
    },
    'revision-date': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
    },
}
"""YANG `keyword` mapping to LSP

Following property keys are present
* `symbol`: LSP `SymbolKind`
* `completion`: LSP `CompletionItemKind`
"""
