"""LSP Semantic Tokens Provider

* `textDocument/semanticTokens/full`

TODO:
* `textDocument/semanticTokens/full/delta`
* `textDocument/semanticTokens/range`

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens
"""

from typing import List, Tuple, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang import util
from pyang.context import Context
from pyang.lsp import common
from pyang.statements import ModSubmodStatement, Statement

from . import glue, types

TOKEN_TYPES: List[str] = [
    types.SemanticTokenType.Namespace,
    types.SemanticTokenType.Type,
    types.SemanticTokenType.Class,
    types.SemanticTokenType.Enum,
    types.SemanticTokenType.Interface,
    types.SemanticTokenType.Struct,
    types.SemanticTokenType.TypeParameter,
    types.SemanticTokenType.Parameter,
    types.SemanticTokenType.Variable,
    types.SemanticTokenType.Property,
    types.SemanticTokenType.EnumMember,
    types.SemanticTokenType.Event,
    types.SemanticTokenType.Function,
    types.SemanticTokenType.Method,
    types.SemanticTokenType.Macro,
    types.SemanticTokenType.Keyword,
    types.SemanticTokenType.Modifier,
    types.SemanticTokenType.Comment,
    types.SemanticTokenType.String,
    types.SemanticTokenType.Number,
    types.SemanticTokenType.RegExp,
    types.SemanticTokenType.Operator,
    types.SemanticTokenType.Decorator,
]
"""`SemanticTokensLegend.tokenTypes`

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokensLegend"""

TOKEN_MODIFIERS: List[str] = [
    types.SemanticTokenModifier.Declaration,
    types.SemanticTokenModifier.Definition,
    types.SemanticTokenModifier.ReadOnly,
    types.SemanticTokenModifier.Static,
    types.SemanticTokenModifier.Deprecated,
    types.SemanticTokenModifier.Abstract,
    types.SemanticTokenModifier.Async,
    types.SemanticTokenModifier.Modification,
    types.SemanticTokenModifier.Documentation,
    types.SemanticTokenModifier.DefaultLibrary,
]
"""`SemanticTokensLegend.tokenModifiers`

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokensLegend"""

DeltaLine = int
DeltaChar = int
TokenLength = int
TokenTypeIndex = int
TokenModifierFlags = int
SemanticToken = Tuple[DeltaLine, DeltaChar, TokenLength, TokenTypeIndex, TokenModifierFlags]
"""`SemanticTokens.data` fragment instance

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokens
https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens"""

def delta_linechar(
    curr_line: int,
    curr_char: int,
    prev_line: int = 0,
    prev_char: int = 0,
) -> Tuple[int, int]:
    delta_line = curr_line - prev_line
    if delta_line == 0:
        delta_char = curr_char - prev_char
    else:
        delta_char = curr_char
    return (delta_line, delta_char)

def stmt_type_token_idx(ctx: Context, stmt: Statement) -> int:
    base_type = common.get_base_type(ctx, stmt)
    if base_type:
        return TOKEN_TYPES.index(types.type_map[base_type]['semantic'])
    return TOKEN_TYPES.index(types.SemanticTokenType.Type)

def arg_token_idx(ctx: Context, stmt: Statement) -> int:
    match stmt.keyword:
        case 'default':
            return stmt_type_token_idx(ctx, stmt.parent)
        case _:
            if not util.is_prefixed(stmt.keyword):
                return TOKEN_TYPES.index(types.keyword_map[stmt.keyword]['semantic'])
            # TODO: add a plugin hook to allow specification of extension arg type
            keyword = stmt.keyword[0] + ':' + stmt.keyword[1]
            try:
                return TOKEN_TYPES.index(types.keyword_map[keyword]['semantic'])
            except KeyError:
                return TOKEN_TYPES.index(types.SemanticTokenType.Type)

def arg_tok_mods(stmt: Statement) -> int:
    tok_mods = 0
    match stmt.keyword:
        case 'description':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Documentation)
        case 'reference':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Documentation)
        case 'presence':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Documentation)
        case 'typedef':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Definition)
        case 'identity':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Definition)
        case 'extension':
            tok_mods |= TOKEN_MODIFIERS.index(types.SemanticTokenModifier.Definition)
        case _:
            pass
    if hasattr(stmt, 'i_config') and not stmt.i_config:
        tok_mods |= TOKEN_MODIFIERS.index('readonly')
    if (status := stmt.search_one('status')) and \
            status.arg in ['deprecated', 'obsolete']:
        tok_mods |= TOKEN_MODIFIERS.index('deprecated')
    return tok_mods

def arg_tokens(
    ctx: Context,
    stmt: Statement,
) -> Tuple[List[SemanticToken], Tuple[int, int]]:
    return ([], (0, 0))

def kwd_tokens(
    ctx: Context,
    stmt: Statement,
) -> Tuple[List[SemanticToken], Tuple[int, int]]:
    return ([], (0, 0))

def stmt_tokens(
    ctx: Context,
    stmt: Statement,
    last_line: int = 0,
    last_char: int = 0,
) -> Tuple[List[SemanticToken], Tuple[int, int]]:
    tokens: List[SemanticToken] = []
    # kwd token
    sel_range = glue.kwd_lsp_selection_range(stmt.pos)
    sline = sel_range.start.line
    schar = sel_range.start.character
    echar = sel_range.end.character
    delta_line, delta_char = delta_linechar(sline, schar, last_line, last_char)
    length = echar - schar
    tok_mods = 0
    if not util.is_prefixed(stmt.keyword):
        tok_type = TOKEN_TYPES.index(types.SemanticTokenType.Keyword)
        tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
    else:
        module, keyword = stmt.keyword
        prefix = None
        for prefix, mod_tuple in stmt.top.i_prefixes.items():
            if module == mod_tuple[0]:
                break
        if prefix:
            # prefix
            length = len(prefix)
            tok_type = TOKEN_TYPES.index(types.SemanticTokenType.Namespace)
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            schar += delta_char
            # :
            delta_line = 0
            delta_char = length
            length = 1
            tok_type = TOKEN_TYPES.index(types.SemanticTokenType.Operator)
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            schar += delta_char
            # keyword
            delta_line = 0
            delta_char = length
            length = len(keyword)
            tok_type = TOKEN_TYPES.index(types.SemanticTokenType.Keyword)
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            schar -= 1 # FIXME: bandaid to fix arg token delta
    prev_line = sline
    prev_char = schar

    if stmt.arg:
        # arg token
        sel_range = glue.arg_lsp_selection_range(stmt.pos)
        sline = sel_range.start.line
        schar = sel_range.start.character
        eline = sel_range.end.line
        echar = sel_range.end.character
        delta_line, delta_char = delta_linechar(sline, schar, prev_line, prev_char)
        if eline == sline:
            # single line argument
            length = echar - schar
        else:
            # FIXME: Set length for first line add more tokens for multiline
            length = 666
        tok_type = arg_token_idx(ctx, stmt)
        tok_mods = arg_tok_mods(stmt)
        tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
        prev_line = sline
        prev_char = schar

    # sub tokens
    for substmt in stmt.substmts:
        substmt_tokens, (prev_line, prev_char) = stmt_tokens(ctx, substmt, prev_line, prev_char)
        tokens.extend(substmt_tokens)

    return (tokens, (prev_line, prev_char))

def text_document_semantic_tokens_full(
    ls: LanguageServer,
    params: lsp.SemanticTokensParams,
) -> Union[lsp.SemanticTokens, None]:
    """Handles LSP `textDocument/semanticTokens/full` request."""
    if not ls.client_capabilities.text_document or \
            not ls.client_capabilities.text_document.semantic_tokens:
        return None

    module: ModSubmodStatement = ls.modules[params.text_document.uri] # type: ignore
    if not module:
        return None

    tokens = stmt_tokens(ls.ctx, module)[0] # type: ignore

    data = []
    for token in tokens:
        data.extend(token)

    return lsp.SemanticTokens(
        data=data,
    )

def text_document_semantic_tokens_full_delta(
    ls: LanguageServer,
    _params: lsp.SemanticTokensDeltaParams,
) -> Union[lsp.SemanticTokens, lsp.SemanticTokensDelta, None]:
    """Handles LSP `textDocument/semanticTokens/full/delta` request."""
    if not ls.client_capabilities.text_document or \
            not ls.client_capabilities.text_document.semantic_tokens:
        return None
    return None

def text_document_semantic_tokens_range(
    ls: LanguageServer,
    _params: lsp.SemanticTokensRangeParams,
) -> Union[lsp.SemanticTokens, None]:
    """Handles LSP `textDocument/semanticTokens/range` request."""
    if not ls.client_capabilities.text_document or \
            not ls.client_capabilities.text_document.semantic_tokens:
        return None
    return None

def register_callbacks(ls: LanguageServer):
    ls.feature(
        lsp.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
        lsp.SemanticTokensRegistrationOptions(
            legend=lsp.SemanticTokensLegend(
                token_types=TOKEN_TYPES,
                token_modifiers=TOKEN_MODIFIERS,
            ),
            range=False,
            full=lsp.SemanticTokensRegistrationOptionsFullType1(
                delta=False,
            ),
        ),
    )(text_document_semantic_tokens_full)

    # ls.feature(
    #     lsp.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL_DELTA,
    # )(text_document_semantic_tokens_full_delta)

    # ls.feature(
    #     lsp.TEXT_DOCUMENT_SEMANTIC_TOKENS_RANGE,
    # )(text_document_semantic_tokens_range)
