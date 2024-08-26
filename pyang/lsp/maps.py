"""YANG Definitions to LSP Type Maps"""

from lsprotocol import types as lsp

arg_type_map = {
    'identifier': {
        'semantic': lsp.SemanticTokenTypes.Class,
    },
    'version': {
        'semantic': lsp.SemanticTokenTypes.Property,
    },
    'uri': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'date': {
        'semantic': lsp.SemanticTokenTypes.Property,
    },
    'string': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'boolean': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    },
    'if-feature-expr': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'identifier-ref': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'fraction-digits-arg': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'range-arg': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'length-arg': {
        'semantic': lsp.SemanticTokenTypes.String,
    },
    'enum-arg': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    },
    'path-arg': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    },
    'non-negative-integer': {
        'semantic': lsp.SemanticTokenTypes.Number,
    },
    'status-arg': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    },
    'ordered-by-arg': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    },
    'max-value': {
        'semantic': lsp.SemanticTokenTypes.Number,
    },
    'integer': {
        'semantic': lsp.SemanticTokenTypes.Number,
    },
    'modifier-arg': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'key-arg': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'unique-arg': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'descendant-schema-nodeid': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'schema-nodeid': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'absolute-schema-nodeid': {
        'semantic': lsp.SemanticTokenTypes.Type,
    },
    'deviate-arg': {
        'semantic': lsp.SemanticTokenTypes.EnumMember,
    }
}
"""pyang `stmt_map` <argument type name> mapping to LSP

Following property keys are present
* `semantic`: LSP `lsp.SemanticTokenTypes` for argument type
"""

status_map = {
    'deprecated': {
        'symbol': lsp.SymbolTag.Deprecated,
        'semantic': lsp.SemanticTokenModifiers.Deprecated,
    },
    'obsolete': {
        'symbol': lsp.SymbolTag.Deprecated,
        'semantic': lsp.SemanticTokenModifiers.Deprecated,
    }
}
"""YANG `status` mapping to LSP

Following property keys are present
* `symbol`  : LSP `SymbolTag` for parent's argument
* `semantic`: LSP `SemanticTokenModifier` for parent's argument
"""

type_map = {
    'uint8': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'uint16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'uint32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'uint64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'int8': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'int16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'int32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'int64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'decimal64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'string': {
        'symbol'    : lsp.SymbolKind.String,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'boolean': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'enumeration': {
        'symbol'    : lsp.SymbolKind.Enum,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'bits': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
    },
    'binary': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
    },
    'union': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Struct,
    },
    'leafref': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
    },
    'identityref': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'instance-identifier': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
    },
    'empty': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
    },
}
"""YANG `type` mapping to LSP

Following property keys are present
* `symbol`    : LSP `SymbolKind` for argument
* `completion`: LSP `CompletionItemKind` for keyword
* `semantic`  : LSP `SemanticTokenType` for argument
* `modifiers` : LSP `SemanticTokenModifiers` for argument
"""

keyword_map = {
    'module': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
    },
    'submodule': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
    },
    'yang-version': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'revision': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'contact': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'organization': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'description': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'reference': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'namespace': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'prefix': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
    },
    'feature': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Constant,
        'semantic'  : lsp.SemanticTokenTypes.Interface,
    },
    'if-feature': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Interface,
    },
    'when': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
    },
    'must': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
    },
    'choice': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
    },
    'case': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
    },
    'grouping': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.Struct,
        'semantic'  : lsp.SemanticTokenTypes.Macro,
    },
    'extension': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Keyword,
    },
    'key': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'pattern': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Regexp,
    },
    'fraction-digits': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'identity': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'base': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'typedef': {
        'symbol'    : lsp.SymbolKind.TypeParameter,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'type': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'container': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
    },
    'leaf': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
    },
    'leaf-list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
    },
    'rpc': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : lsp.SemanticTokenTypes.Function,
    },
    'action': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : lsp.SemanticTokenTypes.Function,
    },
    'input': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
    },
    'output': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
    },
    'notification': {
        'symbol'    : lsp.SymbolKind.Event,
        'completion': lsp.CompletionItemKind.Event,
        'semantic'  : lsp.SemanticTokenTypes.Event,
    },
    'enum': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'error-message': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'presence': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.TypeParameter,
    },
    'value': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'bit': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'position': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'anyxml': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : lsp.SemanticTokenTypes.String,
    },
    'anydata': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
    },
    'augment': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
    },
    'deviation': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
    },
    'deviate': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
    },
    'refine': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : lsp.SemanticTokenTypes.Class,
    },
    'config': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'units': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'path': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'length': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'range': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'modifier': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
    },
    'mandatory': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'max-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'min-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
    },
    'default': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'uses': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Macro,
    },
    'argument': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'status': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'ordered-by': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'import': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
    },
    'include': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
    },
    'revision-date': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'require-instance': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    'yin-element': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
    },
    'unique': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
    },
    '_comment': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : lsp.SemanticTokenTypes.Comment,
    },
}
"""YANG `keyword` mapping to LSP

Following property keys are present
* `symbol`    : LSP `SymbolKind` for argument
* `completion`: LSP `CompletionItemKind` for keyword
* `semantic`  : LSP `SemanticTokenType` for argument
* `modifiers` : LSP `SemanticTokenModifiers` for argument
"""
