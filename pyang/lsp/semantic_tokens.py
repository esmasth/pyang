"""LSP Semantic Tokens Provider

* `textDocument/semanticTokens/full`

TODO:
* `textDocument/semanticTokens/full/delta`
* `textDocument/semanticTokens/range`

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens
"""

import re
from typing import List, Tuple, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer

from pyang import util
from pyang.context import Context
from pyang.grammar import data_def_stmts, flatten_spec, stmt_map
from pyang.statements import AugmentStatement, DeviationStatement, ModSubmodStatement, Statement
from pyang.types import yang_type_specs

from . import common, glue, maps

TOKEN_TYPES: List[str] = [
    lsp.SemanticTokenTypes.Namespace,
    lsp.SemanticTokenTypes.Type,
    lsp.SemanticTokenTypes.Class,
    lsp.SemanticTokenTypes.Enum,
    lsp.SemanticTokenTypes.Interface,
    lsp.SemanticTokenTypes.Struct,
    lsp.SemanticTokenTypes.TypeParameter,
    lsp.SemanticTokenTypes.Parameter,
    lsp.SemanticTokenTypes.Variable,
    lsp.SemanticTokenTypes.Property,
    lsp.SemanticTokenTypes.EnumMember,
    lsp.SemanticTokenTypes.Event,
    lsp.SemanticTokenTypes.Function,
    lsp.SemanticTokenTypes.Method,
    lsp.SemanticTokenTypes.Macro,
    lsp.SemanticTokenTypes.Keyword,
    lsp.SemanticTokenTypes.Modifier,
    lsp.SemanticTokenTypes.Comment,
    lsp.SemanticTokenTypes.String,
    lsp.SemanticTokenTypes.Number,
    lsp.SemanticTokenTypes.Regexp,
    lsp.SemanticTokenTypes.Operator,
    lsp.SemanticTokenTypes.Decorator,
]
"""`SemanticTokensLegend.tokenTypes`

https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#semanticTokensLegend"""

TOKEN_MODIFIERS: List[str] = [
    lsp.SemanticTokenModifiers.Declaration,
    lsp.SemanticTokenModifiers.Definition,
    lsp.SemanticTokenModifiers.Readonly,
    lsp.SemanticTokenModifiers.Static,
    lsp.SemanticTokenModifiers.Deprecated,
    lsp.SemanticTokenModifiers.Abstract,
    lsp.SemanticTokenModifiers.Async,
    lsp.SemanticTokenModifiers.Modification,
    lsp.SemanticTokenModifiers.Documentation,
    lsp.SemanticTokenModifiers.DefaultLibrary,
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
        return TOKEN_TYPES.index(maps.type_map[base_type]['semantic'])
    return TOKEN_TYPES.index(lsp.SemanticTokenTypes.Type)

def arg_token_idx(ctx: Context, stmt: Statement) -> int:
    match stmt.keyword:
        case 'default':
            return stmt_type_token_idx(ctx, stmt.parent)
        case _:
            try:
                token_type = maps.keyword_map[stmt.keyword]['semantic']
            except KeyError:
                try:
                    arg_type = stmt_map[stmt.keyword][0]
                    token_type = maps.arg_type_map[arg_type]['semantic']
                except KeyError:
                    token_type = lsp.SemanticTokenTypes.Type
            return TOKEN_TYPES.index(token_type)

def _is_deprecated(stmt: Statement) -> bool:
    status = stmt.search_one('status')
    if status:
        return status.arg in ['deprecated', 'obsolete']
    return False

def _update_tok_mods(tok_mods: int, mod: str) -> int:
    tok_mods |= 1 << TOKEN_MODIFIERS.index(mod)
    return tok_mods

def arg_tok_mods(ctx: Context, stmt: Statement, deprecated: bool = False) -> int:
    tok_mods = 0
    def _set_tok_mod(mod: str) -> None:
        nonlocal tok_mods
        tok_mods = _update_tok_mods(tok_mods, mod)
    def _is_child_of_augment_deviation_refine(stmt: Statement) -> bool:
        parent = stmt.parent
        while parent is not None:
            if parent.keyword in ['augment', 'deviate', 'refine']:
                return True
            parent = parent.parent
        return False
    match stmt.keyword:
        case 'module':
            _set_tok_mod(lsp.SemanticTokenModifiers.Definition)
        case 'submodule':
            _set_tok_mod(lsp.SemanticTokenModifiers.Definition)
        case 'prefix':
            _set_tok_mod(lsp.SemanticTokenModifiers.Declaration)
        case 'description':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'reference':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'organization':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'contact':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'presence':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'error-message':
            _set_tok_mod(lsp.SemanticTokenModifiers.Documentation)
        case 'typedef':
            _set_tok_mod(lsp.SemanticTokenModifiers.Definition)
        case 'identity':
            _set_tok_mod(lsp.SemanticTokenModifiers.Definition)
            if not stmt.search_one('base'):
                _set_tok_mod(lsp.SemanticTokenModifiers.Abstract)
        case 'type':
            if stmt.arg in yang_type_specs:
                _set_tok_mod(lsp.SemanticTokenModifiers.DefaultLibrary)
        case 'extension':
            _set_tok_mod(lsp.SemanticTokenModifiers.Definition)
        case _:
            pass
    if _is_child_of_augment_deviation_refine(stmt):
        _set_tok_mod(lsp.SemanticTokenModifiers.Modification)
    if hasattr(stmt, 'i_config') and not stmt.i_config:
        _set_tok_mod(lsp.SemanticTokenModifiers.Readonly)
    if deprecated:
        _set_tok_mod(lsp.SemanticTokenModifiers.Deprecated)
    elif stmt.keyword in common.ref_map:
        ref_stmt = common.referenced_stmt_from_stmt_arg(ctx, stmt)
        if ref_stmt and _is_deprecated(ref_stmt):
            _set_tok_mod(lsp.SemanticTokenModifiers.Deprecated)
    elif stmt.keyword == 'augment':
        aug_stmt = common.get_augmented_stmt(stmt) # type: ignore
        if aug_stmt and _is_deprecated(aug_stmt):
            _set_tok_mod(lsp.SemanticTokenModifiers.Deprecated)

    return tok_mods

def arg_tokens(
    ctx: Context,
    stmt: Statement,
) -> Tuple[List[SemanticToken], Tuple[int, int]]:
    return ([], (0, 0))

def kwd_tok_mods(
    ctx: Context,
    stmt: Statement,
) -> int:
    ext_stmt = common.ext_stmt_from_stmt_kwd(ctx, stmt)
    if ext_stmt:
        if _is_deprecated(ext_stmt):
            return _update_tok_mods(0, lsp.SemanticTokenModifiers.Deprecated)
    return 0

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
    parent_deprecated: bool = False,
) -> Tuple[List[SemanticToken], Tuple[int, int]]:
    tokens: List[SemanticToken] = []
    # kwd token
    sel_range = glue.kwd_lsp_selection_range(stmt.pos)
    sline = sel_range.start.line
    schar = sel_range.start.character
    echar = sel_range.end.character
    delta_line, delta_char = delta_linechar(sline, schar, last_line, last_char)
    length = echar - schar
    if not util.is_prefixed(stmt.keyword):
        tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Keyword)
        tok_mods = _update_tok_mods(0, lsp.SemanticTokenModifiers.DefaultLibrary)
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
            tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Namespace)
            tok_mods = 0
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            # :
            delta_line = 0
            delta_char = length
            schar += length
            length = 1
            tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Operator)
            tok_mods = 0
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            # keyword
            delta_line = 0
            delta_char = length
            schar += length
            length = len(keyword)
            tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Keyword)
            tok_mods = kwd_tok_mods(ctx, stmt)
            tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
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
        tok_mods = 0
        if not parent_deprecated:
            if _is_deprecated(stmt):
                deprecated = True
                parent_deprecated = True
            else:
                deprecated = False
        else:
            data_def_kwds = [x[0] for x in flatten_spec(data_def_stmts)]
            deprecated = stmt.keyword in data_def_kwds + ['grouping']
        if eline == sline:
            # single line argument
            length = echar - schar
            # XXX: presuming strings split by + are never on single line
            substring = stmt.arg_substrings[0] # type: ignore
            if substring[1] != '':
                length = length - 2
                delta_char += 1
            prefixed_arg_re = re.compile(r'(^[a-zA-Z0-9-_]+):([a-zA-Z0-9-_]+)$')
            m = prefixed_arg_re.match(stmt.arg)
            if stmt.keyword in ['augment', 'deviation']:
                ref_stmt = None
                if stmt.keyword == 'augment':
                    aug: AugmentStatement = stmt # type: ignore
                    ref_stmt = common.get_augmented_stmt(aug)
                elif stmt.keyword == 'deviation':
                    dev: DeviationStatement = stmt # type: ignore
                    ref_stmt = common.get_deviated_stmt(dev)
                stmts : List[Statement] = []
                if ref_stmt:
                    stmts.insert(0, ref_stmt)
                    while ref_stmt.parent != ref_stmt.top:
                        ref_stmt = ref_stmt.parent
                        stmts.insert(0, ref_stmt)
                # slice the stmt.arg across '/'
                target : str = stmt.arg
                nodes = target.split('/')
                nodes = nodes[1:] if nodes[0] == '' else nodes
                parent_stmt : Statement | ModSubmodStatement | None = None
                mod_stmt = None
                i = 0
                for node in nodes:
                    maybe_prefixed_arg_re = re.compile(r'^(([a-zA-Z0-9-_]+):)?([a-zA-Z0-9-_]+)$')
                    m = maybe_prefixed_arg_re.match(node)
                    # /
                    length = 1
                    tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Operator)
                    tok_mods = 0
                    tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                    delta_line = 0
                    delta_char = length
                    schar += length
                    if not m:
                        continue
                    prefix = m.group(2) if m.group(1) else None
                    element = m.group(3)
                    if prefix:
                        # prefix
                        length = len(prefix)
                        tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Namespace)
                        mod_prefix = stmt.top.search_one('prefix')
                        if mod_prefix and mod_prefix.arg == prefix:
                            mod_stmt = stmt.top
                        else:
                            imp_mods = stmt.top.search('import')
                            for imp_mod in imp_mods:
                                imp_prefix = imp_mod.search_one('prefix')
                                if prefix != imp_prefix.arg:
                                    continue
                                revision = None
                                imp_revdate = imp_mod.search_one('revision-date')
                                if imp_revdate is not None:
                                    revision = imp_revdate.arg
                                mod_stmt = ctx.get_module(imp_mod.arg, revision)
                                if mod_stmt:
                                    break
                        if not mod_stmt:
                            break
                        parent_stmt = parent_stmt if parent_stmt else mod_stmt
                        tok_mods = arg_tok_mods(ctx, mod_stmt)
                        tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                        delta_line = 0
                        delta_char = length
                        schar += length
                        # :
                        length = 1
                        tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Operator)
                        tok_mods = 0
                        tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                        delta_line = 0
                        delta_char = length
                        schar += length
                    # element
                    length = len(element)
                    elem_stmt = stmts[i]
                    tok_type = arg_token_idx(ctx, elem_stmt)
                    tok_mods = arg_tok_mods(ctx, elem_stmt)
                    tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                    delta_line = 0
                    delta_char = length
                    schar += length
                    i += 1
            elif not m:
                tok_type = arg_token_idx(ctx, stmt)
                tok_mods = arg_tok_mods(ctx, stmt, deprecated)
                tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
            elif stmt.keyword in ['type', 'if-feature', 'uses', 'base']:
                prefix = m.group(1)
                element = m.group(2)
                # prefix
                length = len(prefix)
                tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Namespace)
                tok_mods = 0
                tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                delta_line = 0
                delta_char = length
                schar += length
                # :
                length = 1
                tok_type = TOKEN_TYPES.index(lsp.SemanticTokenTypes.Operator)
                tok_mods = 0
                tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
                delta_line = 0
                delta_char = length
                schar += length
                # element
                length = len(element)
                tok_type = arg_token_idx(ctx, stmt)
                tok_mods = arg_tok_mods(ctx, stmt)
                tokens.append((delta_line, delta_char, length, tok_type, tok_mods))
        else:
            # multi line argument
            tok_type = arg_token_idx(ctx, stmt)
            if stmt.keyword in ['augment', 'deviation']:
                tok_mods = arg_tok_mods(ctx, stmt)
            else:
                tok_mods = arg_tok_mods(ctx, stmt)
            # XXX: presuming strings split by + or \n are always aligned
            delta_char += 1
            for arg_substr in stmt.arg_substrings: # type: ignore
                arg_toks = arg_substr[0].split('\n')
                for arg_tok in arg_toks:
                    tokens.append((delta_line, delta_char, len(arg_tok), tok_type, tok_mods))
                    delta_line = 1
                    sline += 1
                    delta_char = schar + 1
            delta_line = 0
            sline -= 1
        prev_line = sline
        prev_char = schar

    # sub tokens
    for substmt in stmt.substmts:
        substmt_tokens, (prev_line, prev_char) = stmt_tokens(
            ctx,
            substmt,
            prev_line,
            prev_char,
            parent_deprecated,
        )
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

    wfc = common.get_workspace_folder_context(ls, params.text_document.uri)
    if not wfc:
        return None

    try:
        module = ls.modules[params.text_document.uri] # type: ignore
        if not module:
            return None
    except KeyError:
        return None

    tokens = stmt_tokens(wfc.ctx, module)[0] # type: ignore

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
