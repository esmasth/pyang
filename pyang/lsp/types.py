"""YANG Definitions to LSP Type Maps"""

import enum
from lsprotocol import types as lsp

# https: //microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokenTypes
@enum.unique
class SemanticTokenType(str, enum.Enum):
    """LSP Semantic Token Types"""
    Namespace = 'namespace'
    Type = 'type'
    """Represents a generic type.
    Acts as a fallback for types which can't be mapped to a specific type like `class` or `enum`."""
    Class = 'class'
    Enum = 'enum'
    Interface = 'interface'
    Struct = 'struct'
    TypeParameter = 'typeParameter'
    Parameter = 'parameter'
    Variable = 'variable'
    Property = 'property'
    EnumMember = 'enumMember'
    Event = 'event'
    Function = 'function'
    Method = 'method'
    Macro = 'macro'
    Keyword = 'keyword'
    Modifier = 'modifier'
    Comment = 'comment'
    String = 'string'
    Number = 'number'
    RegExp = 'regexp'
    Operator = 'operator'
    Decorator = 'decorator'

# https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokenModifiers
@enum.unique
class SemanticTokenModifier(str, enum.Enum):
    """LSP Semantic Token Modifiers"""
    Declaration = 'declaration'
    Definition = 'definition'
    ReadOnly = 'readonly'
    Static = 'static'
    Deprecated = 'deprecated'
    Abstract = 'abstract'
    Async = 'async'
    Modification = 'modification'
    Documentation = 'documentation'
    DefaultLibrary = 'defaultLibrary'

arg_type_map = {
    'identifier': {
        'semantic': SemanticTokenType.Class,
    },
    'version': {
        'semantic': SemanticTokenType.Property,
    },
    'uri': {
        'semantic': SemanticTokenType.String,
    },
    'date': {
        'semantic': SemanticTokenType.Property,
    },
    'string': {
        'semantic': SemanticTokenType.String,
    },
    'boolean': {
        'semantic': SemanticTokenType.EnumMember,
    },
    'if-feature-expr': {
        'semantic': SemanticTokenType.String,
    },
    'identifier-ref': {
        'semantic': SemanticTokenType.String,
    },
    'fraction-digits-arg': {
        'semantic': SemanticTokenType.String,
    },
    'range-arg': {
        'semantic': SemanticTokenType.String,
    },
    'length-arg': {
        'semantic': SemanticTokenType.String,
    },
    'enum-arg': {
        'semantic': SemanticTokenType.EnumMember,
    },
    'path-arg': {
        'semantic': SemanticTokenType.EnumMember,
    },
    'non-negative-integer': {
        'semantic': SemanticTokenType.Number,
    },
    'status-arg': {
        'semantic': SemanticTokenType.EnumMember,
    },
    'ordered-by-arg': {
        'semantic': SemanticTokenType.EnumMember,
    },
    'max-value': {
        'semantic': SemanticTokenType.Number,
    },
    'integer': {
        'semantic': SemanticTokenType.Number,
    },
    'modifier-arg': {
        'semantic': SemanticTokenType.Type,
    },
    'key-arg': {
        'semantic': SemanticTokenType.Type,
    },
    'unique-arg': {
        'semantic': SemanticTokenType.Type,
    },
    'descendant-schema-nodeid': {
        'semantic': SemanticTokenType.Type,
    },
    'schema-nodeid': {
        'semantic': SemanticTokenType.Type,
    },
    'absolute-schema-nodeid': {
        'semantic': SemanticTokenType.Type,
    },
    'deviate-arg': {
        'semantic': SemanticTokenType.EnumMember,
    }
}
"""pyang `stmt_map` <argument type name> mapping to LSP

Following property keys are present
* `semantic`: LSP `SemanticTokenType` for argument type
"""

status_map = {
    'deprecated': {
        'symbol': lsp.SymbolTag.Deprecated,
        'semantic': SemanticTokenModifier.Deprecated,
    },
    'obsolete': {
        'symbol': lsp.SymbolTag.Deprecated,
        'semantic': SemanticTokenModifier.Deprecated,
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
        'semantic'  : SemanticTokenType.Number,
    },
    'uint16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'uint32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'uint64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'int8': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'int16': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'int32': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'int64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'decimal64': {
        'symbol'    : lsp.SymbolKind.Number,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Number,
    },
    'string': {
        'symbol'    : lsp.SymbolKind.String,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.String,
    },
    'boolean': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'enumeration': {
        'symbol'    : lsp.SymbolKind.Enum,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'bits': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Type,
    },
    'binary': {
        'symbol'    : lsp.SymbolKind.Field,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Type,
    },
    'union': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Struct,
    },
    'leafref': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Type,
    },
    'identityref': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Class,
    },
    'instance-identifier': {
        'symbol'    : lsp.SymbolKind.Object,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Type,
    },
    'empty': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Type,
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
        'semantic'  : SemanticTokenType.Namespace,
    },
    'submodule': {
        'symbol'    : lsp.SymbolKind.Module,
        'completion': lsp.CompletionItemKind.Module,
        'semantic'  : SemanticTokenType.Namespace,
    },
    'yang-version': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'revision': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'contact': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.String,
    },
    'organization': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.String,
    },
    'description': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.String,
    },
    'reference': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.String,
    },
    'namespace': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'prefix': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Namespace,
    },
    'feature': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Constant,
        'semantic'  : SemanticTokenType.Interface,
    },
    'if-feature': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Interface,
    },
    'when': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Operator,
    },
    'must': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Operator,
    },
    'choice': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Decorator,
    },
    'case': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Decorator,
    },
    'grouping': {
        'symbol'    : lsp.SymbolKind.Struct,
        'completion': lsp.CompletionItemKind.Struct,
        'semantic'  : SemanticTokenType.Macro,
    },
    'extension': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Keyword,
    },
    'key': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'pattern': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.RegExp,
    },
    'fraction-digits': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Number,
    },
    'identity': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : SemanticTokenType.Class,
    },
    'base': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Class,
    },
    'typedef': {
        'symbol'    : lsp.SymbolKind.TypeParameter,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.Class,
    },
    'type': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Class,
    },
    'container': {
        'symbol'    : lsp.SymbolKind.Class,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : SemanticTokenType.Class,
    },
    'list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Class,
        'semantic'  : SemanticTokenType.Variable,
    },
    'leaf': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : SemanticTokenType.Variable,
    },
    'leaf-list': {
        'symbol'    : lsp.SymbolKind.Array,
        'completion': lsp.CompletionItemKind.Field,
        'semantic'  : SemanticTokenType.Variable,
    },
    'rpc': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : SemanticTokenType.Function,
    },
    'action': {
        'symbol'    : lsp.SymbolKind.Function,
        'completion': lsp.CompletionItemKind.Function,
        'semantic'  : SemanticTokenType.Function,
    },
    'input': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Operator,
    },
    'output': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Operator,
    },
    'notification': {
        'symbol'    : lsp.SymbolKind.Event,
        'completion': lsp.CompletionItemKind.Event,
        'semantic'  : SemanticTokenType.Event,
    },
    'enum': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'error-message': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : SemanticTokenType.String,
    },
    'presence': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.TypeParameter,
        'semantic'  : SemanticTokenType.TypeParameter,
    },
    'value': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Number,
    },
    'bit': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'position': {
        'symbol'    : lsp.SymbolKind.EnumMember,
        'completion': lsp.CompletionItemKind.EnumMember,
        'semantic'  : SemanticTokenType.Number,
    },
    'anyxml': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : SemanticTokenType.String,
    },
    'anydata': {
        'symbol'    : lsp.SymbolKind.Variable,
        'completion': lsp.CompletionItemKind.Variable,
        'semantic'  : SemanticTokenType.Variable,
    },
    'augment': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Modifier,
    },
    'deviation': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Modifier,
    },
    'deviate': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : SemanticTokenType.Modifier,
    },
    'refine': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Snippet,
        'semantic'  : SemanticTokenType.Class,
    },
    'config': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'units': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'path': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'length': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'range': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'modifier': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Modifier,
    },
    'mandatory': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'max-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Number,
    },
    'min-elements': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Number,
    },
    'default': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'uses': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Operator,
        'semantic'  : SemanticTokenType.Macro,
    },
    'argument': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'status': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'ordered-by': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'import': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : SemanticTokenType.Namespace,
    },
    'include': {
        'symbol'    : lsp.SymbolKind.Operator,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : SemanticTokenType.Namespace,
    },
    'revision-date': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Reference,
        'semantic'  : SemanticTokenType.Property,
    },
    'require-instance': {
        'symbol'    : lsp.SymbolKind.Property,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    'yin-element': {
        'symbol'    : lsp.SymbolKind.Boolean,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : SemanticTokenType.EnumMember,
    },
    'unique': {
        'symbol'    : lsp.SymbolKind.Key,
        'completion': lsp.CompletionItemKind.Property,
        'semantic'  : SemanticTokenType.Property,
    },
    '_comment': {
        'symbol'    : lsp.SymbolKind.Null,
        'completion': lsp.CompletionItemKind.Text,
        'semantic'  : SemanticTokenType.Comment,
    },
}
"""YANG `keyword` mapping to LSP

Following property keys are present
* `symbol`    : LSP `SymbolKind` for argument
* `completion`: LSP `CompletionItemKind` for keyword
* `semantic`  : LSP `SemanticTokenType` for argument
* `modifiers` : LSP `SemanticTokenModifiers` for argument
"""
