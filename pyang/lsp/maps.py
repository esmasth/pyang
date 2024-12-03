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
        'modifiers' : [
            lsp.SemanticTokenModifiers.Definition,
        ],
    },
    'submodule': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Definition,
        ],
    },
    'yang-version': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Declaration,
        ],
    },
    'revision': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'contact': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'organization': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'description': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'reference': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'namespace': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'prefix': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Declaration,
        ],
    },
    'feature': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Constant,
        'semantic'  : lsp.SemanticTokenTypes.Interface,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Definition,
        ],
    },
    'if-feature': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Interface,
        'modifiers' : [
        ],
    },
    'when': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
        'modifiers' : [
        ],
    },
    'must': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
        'modifiers' : [
        ],
    },
    'choice': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
        'modifiers' : [
        ],
    },
    'case': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Decorator,
        'modifiers' : [
        ],
    },
    'grouping': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.Struct,
        'semantic'  : lsp.SemanticTokenTypes.Macro,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Declaration,
        ],
    },
    'extension': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Keyword,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Definition,
        ],
    },
    'key': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'pattern': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Regexp,
        'modifiers' : [
        ],
    },
    'fraction-digits': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
        'modifiers' : [
        ],
    },
    'identity': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'base': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'typedef': {
        'symbol'    : lsp.SymbolKind.TypeParameter,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.Type,
        'modifiers' : [
        ],
    },
    'type': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Type,
        'modifiers' : [
        ],
    },
    'container': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'leaf': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
        'modifiers' : [
        ],
    },
    'leaf-list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
        'modifiers' : [
        ],
    },
    'rpc': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : lsp.SemanticTokenTypes.Function,
        'modifiers' : [
        ],
    },
    'action': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : lsp.SemanticTokenTypes.Function,
        'modifiers' : [
        ],
    },
    'input': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
        'modifiers' : [
        ],
    },
    'output': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Operator,
        'modifiers' : [
        ],
    },
    'notification': {
        'symbol'    : lsp.SymbolKind.Event,
        'completion': lsp.CompletionItemKind.Event,
        'semantic'  : lsp.SemanticTokenTypes.Event,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Async,
        ],
    },
    'enum': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'error-message': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'presence': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : lsp.SemanticTokenTypes.String,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation,
        ],
    },
    'value': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
        'modifiers' : [
        ],
    },
    'bit': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'position': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : lsp.SemanticTokenTypes.Number,
        'modifiers' : [
        ],
    },
    'anyxml': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
        'modifiers' : [
        ],
    },
    'anydata': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : lsp.SemanticTokenTypes.Variable,
        'modifiers' : [
        ],
    },
    'augment': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'deviation': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
        'modifiers' : [
        ],
    },
    'deviate': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
        'modifiers' : [
        ],
    },
    'refine': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : lsp.SemanticTokenTypes.Class,
        'modifiers' : [
        ],
    },
    'config': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'units': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'path': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'length': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'range': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'modifier': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Modifier,
        'modifiers' : [
        ],
    },
    'mandatory': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'max-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
        'modifiers' : [
        ],
    },
    'min-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Number,
        'modifiers' : [
        ],
    },
    'default': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'uses': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : lsp.SemanticTokenTypes.Macro,
        'modifiers' : [
        ],
    },
    'argument': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'status': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'ordered-by': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'import': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
        'modifiers' : [
        ],
    },
    'include': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Namespace,
        'modifiers' : [
        ],
    },
    'revision-date': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'require-instance': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    'yin-element': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : lsp.SemanticTokenTypes.EnumMember,
        'modifiers' : [
        ],
    },
    'unique': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : lsp.SemanticTokenTypes.Property,
        'modifiers' : [
        ],
    },
    '_comment': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : lsp.SemanticTokenTypes.Comment,
        'modifiers' : [
            lsp.SemanticTokenModifiers.Documentation
        ],
    },
}
"""YANG `keyword` mapping to LSP

Following property keys are present
* `symbol`    : LSP `SymbolKind` for argument
* `completion`: LSP `CompletionItemKind` for keyword
* `semantic`  : LSP `SemanticTokenType` for argument
* `modifiers` : LSP `SemanticTokenModifiers` for argument

https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide#standard-token-types-and-modifiers
"""

xpath_token_type_map = {
    'function_name': lsp.SemanticTokenTypes.Function,
    'name': lsp.SemanticTokenTypes.Class,
    'number': lsp.SemanticTokenTypes.Number,
    'literal': lsp.SemanticTokenTypes.String,
    'LPAREN': lsp.SemanticTokenTypes.Operator,
    'RPAREN': lsp.SemanticTokenTypes.Operator,
    'LBRACKET': lsp.SemanticTokenTypes.Operator,
    'RBRACKET': lsp.SemanticTokenTypes.Operator,
    'DOTDOT': lsp.SemanticTokenTypes.Operator,
    'DOT': lsp.SemanticTokenTypes.Operator,
    'COMMA': lsp.SemanticTokenTypes.Operator,
    'AT': lsp.SemanticTokenTypes.Operator,
    'DOLLAR': lsp.SemanticTokenTypes.Operator,
    'DOUBLECOLON': lsp.SemanticTokenTypes.Operator,
    'DOUBLESLASH': lsp.SemanticTokenTypes.Operator,
    'SLASH': lsp.SemanticTokenTypes.Operator,
    'BAR': lsp.SemanticTokenTypes.Operator,
    'PLUS': lsp.SemanticTokenTypes.Operator,
    'MINUS': lsp.SemanticTokenTypes.Operator,
    'EQ': lsp.SemanticTokenTypes.Operator,
    'NEQ': lsp.SemanticTokenTypes.Operator,
    'LTE': lsp.SemanticTokenTypes.Operator,
    'GTE': lsp.SemanticTokenTypes.Operator,
    'GT': lsp.SemanticTokenTypes.Operator,
    'LT': lsp.SemanticTokenTypes.Operator,
    'STAR': lsp.SemanticTokenTypes.Operator,
}
