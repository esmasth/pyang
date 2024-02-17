"""3GPP usage guidelines plugin

For 3GPP General Modeling Rules, see 3GPP TS 32.160 clause 6.2

For 3GPP Common YANG Extension Usage, see descriptions in link below
https://forge.3gpp.org/rep/sa5/MnS/-/blob/Integration_Rel18_SA5_153_YANG/yang-models/_3gpp-common-yang-extensions.yang

Copyright Ericsson 2020-2024
Author balazs.lengyel@ericsson.com
Author siddharth.sharma@ericsson.com

* Revision 2020-11-25

    * Checks implemented
        6.2.1.2     Module name starts with _3gpp-
        6.2.1.3     namespace pattern urn:3gpp:sa5:<module-name>
        6.2.1.4-a   prefix ends with 3gpp
        6.2.1.4-b   prefix.length <= 10 char
        6.2.1.5     yang 1.1 missing
        6.2.1.5     yang 1.1 incorrect
        6.2.1.6-a   anydata
        6.2.1.6-b   anyxml
        6.2.1.6-c   rpc
        6.2.1.6-d   deviation
        6.2.1.9     description not needed for enum, bit, choice, container, 
                    leaf-list, leaf, typedef, grouping, augment, uses
        6.2.1.b-a   module-description-missing
        6.2.1.b-b   module-organization-missing
        6.2.1.b-c   module-organization includes 3gpp
        6.2.1.b-d   module-contact-missing
        6.2.1.b-d   module-contact-incorrect
        6.2.1.c     module-reference-missing
        6.2.1.c     module-reference-incorrect
        6.2.1.d-a   module-revision-missing
        6.2.1.d-a   module-revision-reference-missing
        6.2.1.e     default meaning
        6.2.1.f-a   linelength > 80
        6.2.1.f-b   no-tabs
        6.2.1.f-c   no-strange-chars
        6.2.1.f-d   no-CR-chars
        6.2-a       no-containers

* Revision 2024-02-24

    * Checks removed
        6.2.1.6-a   anydata

    * Checks implemented
        _3gpp-common-yang-extensions@2023-09-18.yang extensions
            nonNotifyable
                YEXT3GPP_NON_NOTIFYABLE_NOT_WITHIN_ATTRIBUTES
            inVariant
                YEXT3GPP_INVARIANT_WITH_KEY_LEAF
                YEXT3GPP_INVARIANT_WITH_CONFIG_FALSE
            initial-value
                YEXT3GPP_INITIAL_VALUE_PARENT_DESCRIPTION
                YEXT3GPP_INITIAL_VALUE_WITH_DEFAULT
                YEXT3GPP_INITIAL_VALUE_LEAF_MULTI_STATEMENTS
                YEXT3GPP_INITIAL_VALUE_WITH_CONFIG_FALSE
                YEXT3GPP_INITIAL_VALUE_ACTION_RPC_NOTIFICATION

"""

from typing import List
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Any

from enum import Enum

import optparse
import re
import io
import sys

from pyang import plugin
from pyang import context
from pyang import grammar
from pyang import syntax
from pyang import statements
from pyang import error
from pyang.error import err_add
from pyang.plugins import lint

_3gpp_mod_name = '_3gpp-common-yang-extensions'

def pyang_plugin_init():
    plugin.register_plugin(THREEGPPlugin())

    _register_ext_stmt_grammar_validation(_3gpp_mod_name, _3gpp_stmts)

class THREEGPPlugin(lint.LintPlugin):
    def __init__(self):
        lint.LintPlugin.__init__(self)
        self.namespace_prefixes = ['urn:3gpp:sa5:']
        self.modulename_prefixes = ['_3gpp']

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option("--3gpp",
                                 dest="threegpp",
                                 action="store_true",
                                 help="Validate the module(s) according to " \
                                 "3GPP rules."),
            optparse.make_option("--3gpp-help",
                                 dest="threegpp_help",
                                 action="store_true",
                                 help="Print help on the 3GPP checks and exit."),
            ]
        optparser.add_options(optlist)

    def setup_ctx(self, ctx):
        if ctx.opts.threegpp_help:
            print_3gpp_help()
            sys.exit(0)
        if not ctx.opts.threegpp:
            return
        self._setup_ctx(ctx)

        error.add_error_code(
           '3GPP_BAD_NAMESPACE_VALUE', ErrorLevel.MinorError,
           '3GPP: the namespace should be urn:3gpp:sa5:%s')

        statements.add_validation_fun(
            'grammar', ['namespace'],
            lambda ctx, s: self.v_chk_namespace(ctx, s))

        error.add_error_code(
           '3GPP_BAD_PREFIX_VALUE', ErrorLevel.MinorError,
           '3GPP: the prefix should end with 3gpp')

        error.add_error_code(
           '3GPP_TOO_LONG_PREFIX', ErrorLevel.MinorError,
           '3GPP: the prefix should not be longer than 13 characters')

        statements.add_validation_fun(
            'grammar', ['prefix'],
            lambda ctx, s: self.v_chk_prefix(ctx, s))

        error.add_error_code(
           '3GPP_BAD_YANG_VERSION', ErrorLevel.MinorError,
           '3GPP: the yang-version should be 1.1')

        statements.add_validation_fun(
            'grammar', ['yang-version'],
            lambda ctx, s: self.v_chk_yang_version(ctx, s))

        # check that yang-version is present. If not,
        #  it defaults to 1. which is bad for 3GPP
        statements.add_validation_fun(
            'grammar', ['module'],
            lambda ctx, s: self.v_chk_yang_version_present(ctx, s))

        error.add_error_code(
           '3GPP_STATEMENT_NOT_ALLOWED', ErrorLevel.MinorError,
           ('3GPP: YANG statements anyxml, deviation, rpc should not be used'))

        statements.add_validation_fun(
            'grammar', ['anyxml' , 'deviation' , 'rpc'],
            lambda ctx, s: self.v_chk_not_allowed_statements(ctx, s))

        error.add_error_code(
           '3GPP_BAD_ORGANIZATION', ErrorLevel.MinorError,
           '3GPP: organization statement must include 3GPP')

        statements.add_validation_fun(
            'grammar', ['organization'],
            lambda ctx, s: self.v_chk_organization(ctx, s))

        error.add_error_code(
           '3GPP_BAD_CONTACT', ErrorLevel.MinorError,
           '3GPP: incorrect contact statement')

        statements.add_validation_fun(
            'grammar', ['contact'],
            lambda ctx, s: self.v_chk_contact(ctx, s))

        error.add_error_code(
           '3GPP_MISSING_MODULE_REFERENCE', ErrorLevel.MinorError,
           '3GPP: the module should have a reference substatement')

        statements.add_validation_fun(
            'grammar', ['module'],
            lambda ctx, s: self.v_chk_module_reference_present(ctx, s))

        error.add_error_code(
           '3GPP_BAD_MODULE_REFERENCE', ErrorLevel.MinorError,
           '3GPP: the module\'s reference substatement is incorrect')

        statements.add_validation_fun(
            'grammar', ['reference'],
            lambda ctx, s: self.v_chk_module_reference(ctx, s))

        error.add_error_code(
           '3GPP_TAB_IN_FILE', ErrorLevel.MinorError,
           '3GPP: tab characters should not be used in YANG modules')

        error.add_error_code(
           '3GPP_WHITESPACE_AT_END_OF_LINE', ErrorLevel.MinorError,
           '3GPP: extra whitespace should not be added at the end of the line')

        error.add_error_code(
           '3GPP_LONG_LINE', ErrorLevel.MinorError,
           '3GPP: line longer than 80 characters')

        error.add_error_code(
           '3GPP_CR_IN_FILE', ErrorLevel.MinorError,
           ('3GPP: Carriage-return characters should not be used. '
            'End-of-line should be just one LF character'))

        error.add_error_code(
           '3GPP_NON_ASCII', ErrorLevel.MinorError,
           '3GPP: the module should only use ASCII characters')

        statements.add_validation_fun(
            'grammar', ['module'],
            lambda ctx, s: self.v_chk_3gpp_format(ctx, s))

        error.add_error_code(
           '3GPP_LIMITED_CONTAINER_USE', ErrorLevel.Warning,
           ('3GPP: containers should only be used to contain the attributes '
            'of a class'))

        statements.add_validation_fun(
            'grammar', ['container'],
            lambda ctx, s: self.v_chk_limited_container_use(ctx, s))


    def pre_validate_ctx(self, ctx, modules):
        if ctx.opts.threegpp:
            ctx.canonical = False
        return

    # This check may be skipped with '-E LINT_BAD_NAMESPACE_VALUE' now
    def v_chk_namespace(self, ctx, stmt):
        r = 'urn:3gpp:sa5:' + stmt.i_module.arg +'$'
        if re.match(r, stmt.arg) is None:
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_NAMESPACE_VALUE',
                    stmt.i_module.arg)

    def v_chk_prefix(self, ctx, stmt):
        if stmt.parent.keyword != 'module' :
            return
        r = '.+3gpp$'
        if re.match(r, stmt.arg) is None:
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_PREFIX_VALUE',())
        if len(stmt.arg) > 13   :
            err_add(ctx.errors, stmt.pos, '3GPP_TOO_LONG_PREFIX',())

    def v_chk_yang_version_present(self, ctx, stmt):
        yang_version_present = False
        for stmt in stmt.substmts:
            if stmt.keyword == 'yang-version' :
                yang_version_present = True
        if not(yang_version_present) :
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_YANG_VERSION',())

    def v_chk_yang_version(self, ctx, stmt):
        r = '1.1'
        if re.match(r, stmt.arg) is None:
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_YANG_VERSION',())
    
    def v_chk_not_allowed_statements(self, ctx, stmt):
        err_add(ctx.errors, stmt.pos, '3GPP_STATEMENT_NOT_ALLOWED',())

    def v_chk_organization(self, ctx, stmt):
        r = '3GPP'
        if re.search(r, stmt.arg, re.IGNORECASE) is None:
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_ORGANIZATION',())

    def v_chk_contact(self, ctx, stmt):
        if stmt.arg != ('https://www.3gpp.org/DynaReport/TSG-WG--S5--officials.htm?Itemid=464'):
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_CONTACT',())

    def v_chk_module_reference_present(self, ctx, stmt):
        module_reference_present = False
        for stmt in stmt.substmts:
            if stmt.keyword == 'reference' :
                module_reference_present = True
        if not(module_reference_present) :
            err_add(ctx.errors, stmt.pos, '3GPP_MISSING_MODULE_REFERENCE',())

    def v_chk_module_reference(self, ctx, stmt):
        if stmt.parent.keyword != 'module' :
            return
        if not(stmt.arg.startswith('3GPP TS ')) :
            err_add(ctx.errors, stmt.pos, '3GPP_BAD_MODULE_REFERENCE',())

    def v_chk_3gpp_format(self, ctx, stmt):
        if (not(stmt.arg.startswith("_3gpp"))):
            return
        filename = stmt.pos.ref
        try:
            fd = io.open(filename, "r", encoding="utf-8", newline='')
            pos = error.Position(stmt.pos.ref)
            pos.top = stmt
            lineno = 0
            for line in fd:
                lineno += 1
                pos.line = lineno
                #  no tabs
                if (line.find('\t') != -1 ):
                    err_add(ctx.errors, pos, '3GPP_TAB_IN_FILE',())
                #  no whitespace after the line
                #  removed for now as there are just too many of these
                #    errors
                # if (re.search('.*\s+\n',line) != None ):
                #    err_add(ctx.errors, self.pos,
                #        '3GPP_WHITESPACE_AT_END_OF_LINE',())
                #  lines shorter then 80 char
                if (len(line) > 82 ):
                    err_add(ctx.errors, pos, '3GPP_LONG_LINE',())
                #  EOL should be just NL no CR
                if (line.find('\r') != -1 ):
                    err_add(ctx.errors, pos, '3GPP_CR_IN_FILE',())
                #  only us-ascii chars
                try:
                    line.encode('ascii')
                except UnicodeEncodeError:
                    err_add(ctx.errors, pos, '3GPP_NON_ASCII',())

        except IOError as ex:
            sys.stderr.write("error %s: %s\n" % (filename, ex))
            sys.exit(1)
        except UnicodeDecodeError as ex:
            s = str(ex).replace('utf-8', 'utf8')
            sys.stderr.write("%s: unicode error: %s\n" % (filename, s))
            sys.exit(1)

    def v_chk_limited_container_use(self, ctx, stmt):
        if stmt.arg  != 'attributes' or stmt.parent.keyword != 'list' :
            err_add(ctx.errors, stmt.pos, '3GPP_LIMITED_CONTAINER_USE',())


    def post_validate_ctx(
            self,
            ctx: context.Context,
            modules: List[statements.Statement]
            ) -> None:
        if not ctx.opts.threegpp: # type: ignore [reportAttributeAccessIssue]
            return
        """Remove some lint errors that 3GPP considers acceptable"""
        for ctx_error in ctx.errors[:]:
            pos: error.Position = ctx_error[0]
            tag = ctx_error[1]
            fmtvars = ctx_error[2]
            if (tag == "LINT_MISSING_REQUIRED_SUBSTMT" or
                tag == "LINT_MISSING_RECOMMENDED_SUBSTMT"):
                # Following is a fragile approach which will break whenever the
                # format variables corresponding to the error tags may change
                # without notice, since they are not a part of plugin interface.
                rfcref = fmtvars[0]
                stmt = fmtvars[1]
                substmt = fmtvars[2]
                if (substmt == 'description' and
                    stmt in ['enum', 'bit', 'choice', 'container', 'leaf-list',
                             'leaf', 'typedef', 'grouping', 'augment', 'uses']):
                    # remove error from ctx
                    ctx.errors.remove(ctx_error)

        return

def print_3gpp_help():
    print("""
Validates the module or submodule according to the 3GPP General Modeling rules
found in 3GPP TS 32.160 clause 6.2
""")

def _is_descendent_of(
        stmt: statements.Statement,
        keyword: str,
        arg: Union[str, None],
        ) -> Tuple[bool, Union[statements.Statement, None]]:
    """Checks if stmt is descendent of a statement

    The ancestor statement is identified by a statement keyword and optionally
    an argument if a specific keyword instance is target.

    Args:
        stmt (statements.Statement): YANG statement
        keyword (str): Ancestor statement type/instance keyword
        arg (Union[str, None]): Ancestor statement instance argument

    Returns:
        Tuple[bool, statements.Statement]:
            (True, ancestor) statement if stmt is descendent, else (False, None)
    """
    if stmt.keyword == keyword and (arg is None or stmt.arg == arg):
        return (True, stmt)
    if stmt.parent == stmt.top:
        return (False, None)
    is_descendent, ancestor_stmt = _is_descendent_of(stmt.parent, keyword, arg)
    if is_descendent:
        return (True, ancestor_stmt)
    else:
        return (False, None)

def _is_descendent_of_ioc_attributes(
        stmt: statements.Statement,
        ) -> bool:
    """TODO: check if there are deterministic markers for an IOC"""
    is_descendent, ancestor_stmt = _is_descendent_of(stmt, 'container', 'attributes')
    return is_descendent

def v_chk_yext3gpp_non_notifyable(
        ctx: context.Context,
        stmt: statements.Statement,
        ) -> None:
    """Validates a _3gpp-common-yang-extensions:nonNotifyable statement instance

    This validation presumes that grammar checks have already been performed.

    Args:
        ctx (context.Context): Context for parse session
        stmt (statements.Statement): Statement for validation callback

    Returns:
        None: Validation recursion continues
    """
    if not _is_descendent_of_ioc_attributes(stmt):
        err_add(ctx.errors, stmt.pos,
                'YEXT3GPP_NON_NOTIFYABLE_NOT_WITHIN_ATTRIBUTES', ())

def v_chk_yext3gpp_invariant(
        ctx: context.Context,
        stmt: statements.Statement,
        ) -> None:
    """Validates a _3gpp-common-yang-extensions:inVariant statement instance

    This validation presumes that grammar checks have already been performed.

    Args:
        ctx (context.Context): Context for parse session
        stmt (statements.Statement): Statement for validation callback

    Returns:
        None: Validation recursion continues
    """
    if not stmt.parent.i_config:
        err_add(ctx.errors, stmt.pos,
                'YEXT3GPP_INVARIANT_WITH_CONFIG_FALSE', ())
    parent: statements.Statement = stmt.parent
    for sibling in parent.parent.substmts:
        if sibling.keyword == 'key' and sibling.arg == parent.arg:
            err_add(ctx.errors, stmt.pos,
                    'YEXT3GPP_INVARIANT_WITH_KEY_LEAF', ())

def _description_contains(
        stmt: statements.Statement,
        text: str
        ) -> bool:
    """Checks if the description of stmt contains text

    Args:
        stmt (statements.Statement): YANG statement
        text (str): Text to search within statement description

    Returns:
        bool: True if description of stmt contains text, else False
    """
    desc = stmt.search_one('description')
    if desc is None or desc.arg == "":
        return False
    return text in desc.arg

initial_value_desc = "Initial-value: "
def v_chk_yext3gpp_initial_value(
        ctx: context.Context,
        stmt: statements.Statement,
        ) -> None:
    """Validates a _3gpp-common-yang-extensions:initial-value statement instance

    This validation presumes that grammar checks have already been performed.

    Args:
        ctx (context.Context): Context for parse session
        stmt (statements.Statement): Statement for validation callback

    Returns:
        None: Validation recursion continues
    """
    for disallowed in ['rpc', 'action', 'notification']:
        is_descendent, ancestor = _is_descendent_of(stmt, disallowed, None)
        if is_descendent:
            err_add(ctx.errors, stmt.pos,
                    'YEXT3GPP_INITIAL_VALUE_ACTION_RPC_NOTIFICATION',
                    (disallowed))
            return
    parent: statements.Statement = stmt.parent
    if not parent.i_config:
        err_add(ctx.errors, stmt.pos,
                'YEXT3GPP_INITIAL_VALUE_WITH_CONFIG_FALSE', ())
    if parent.search_one('default') is not None:
        err_add(ctx.errors, stmt.pos,
                'YEXT3GPP_INITIAL_VALUE_WITH_DEFAULT', ())
    if parent.keyword == 'leaf':
        siblings: List[statements.Statement] = parent.substmts
        first_initial_value_instance: Union[statements.Statement, None] = None
        for sibling in siblings:
            if sibling.keyword == stmt.keyword:
                if not first_initial_value_instance:
                    first_initial_value_instance = sibling
                elif first_initial_value_instance.pos != stmt.pos:
                    err_add(ctx.errors, stmt.pos,
                            'YEXT3GPP_INITIAL_VALUE_LEAF_MULTI_STATEMENTS',
                            (first_initial_value_instance.pos))
    if not _description_contains(stmt.parent, initial_value_desc):
        err_add(ctx.errors, stmt.pos,
                'YEXT3GPP_INITIAL_VALUE_PARENT_DESCRIPTION', ())

StmtKwd = str
class StmtMultiplicity(str, Enum):
    ExactlyOne  = '1',
    NoneOrOne   = '?',
    OneOrMore   = '+',
    NoneOrMore  = '*',
StmtDefault = Any
StmtArgType = str
StmtArgValidFn = Callable[[str], bool]
SubStmtMeta = Tuple[StmtKwd, StmtMultiplicity]
SuperStmts = List[StmtKwd]
StmtValidFn = Callable[[context.Context, statements.Statement], Union[str, None]]
ErrorTag = str
class ErrorLevel(int, Enum):
    CriticalError   = 1,
    MajorError      = 2,
    MinorError      = 3,
    Warning         = 4,
ErrorFmt = str
StmtError = Tuple[ErrorTag, ErrorLevel, ErrorFmt]
StmtMeta = Tuple[StmtKwd, StmtMultiplicity, Union[StmtDefault, None],
                 Tuple[Union[StmtArgType, None], Union[StmtArgValidFn, None], List[SubStmtMeta]],
                 SuperStmts,
                 Tuple[Union[StmtValidFn, None], List[StmtError]]]

# In order of definitions in _3gpp-common-yang-extensions@2023-09-18
# TODO: Check whether the ErrorLevel settings are appropriate
# TODO: Check whether the Errors are in practice as strict as the descriptions
_3gpp_stmts: List[StmtMeta] = [

    ('notNotifyable', StmtMultiplicity.NoneOrOne, None,
     (None, None, []),
     ['leaf', 'leaf-list', 'list', 'container'],
     (v_chk_yext3gpp_non_notifyable,
      [('YEXT3GPP_NON_NOTIFYABLE_NOT_WITHIN_ATTRIBUTES', ErrorLevel.CriticalError,
        "'yext3gpp:notNotifyable' extension must not be used " +
        "as substatement of a node outside IOC attributes")])),

    ('inVariant', StmtMultiplicity.NoneOrOne, None,
     (None, None, []),
     ['leaf', 'leaf-list', 'list'], # description conflicted on 'container'
     (v_chk_yext3gpp_invariant,
      [('YEXT3GPP_INVARIANT_WITH_KEY_LEAF', ErrorLevel.CriticalError,
        "'yext3gpp:inVariant' extension must not be used " +
        "as substatement of a key leaf"),
       ('YEXT3GPP_INVARIANT_WITH_CONFIG_FALSE', ErrorLevel.CriticalError,
        "'yext3gpp:inVariant' extension must not be used " +
        "as substatement of a config false node")])),

    ('initial-value', StmtMultiplicity.NoneOrMore, None,
     ('string', None, []),
     ['leaf', 'leaf-list'],
     (v_chk_yext3gpp_initial_value,
      [('YEXT3GPP_INITIAL_VALUE_PARENT_DESCRIPTION', ErrorLevel.Warning,
        "'yext3gpp:initial-value' statement parent should contain " +
        "'" + initial_value_desc + "' in the description"),
       ('YEXT3GPP_INITIAL_VALUE_WITH_DEFAULT', ErrorLevel.CriticalError,
        "'yext3gpp:initial-value' extension must not be used " +
        "as substatement of a node with default statement"), # TODO: Check what types have default value
       ('YEXT3GPP_INITIAL_VALUE_LEAF_MULTI_STATEMENTS', ErrorLevel.CriticalError,
        "'yext3gpp:initial-value' statement is already present " +
        "as substatement of the leaf node at %s"),
       ('YEXT3GPP_INITIAL_VALUE_WITH_CONFIG_FALSE', ErrorLevel.CriticalError,
        "'yext3gpp:initial-value' extension must not be used " +
        "as substatement of a config false node"),
       ('YEXT3GPP_INITIAL_VALUE_ACTION_RPC_NOTIFICATION', ErrorLevel.CriticalError,
        "'yext3gpp:initial-value' extension must not be used " +
        "as substatement within %s subtree")])),
]

def _register_ext_stmt_grammar_validation(
        module: str,
        stmt_meta: List[StmtMeta]
        ) -> None:
    """Registers YANG extension statement grammar and syntax callback functions

    Args:
        module (str): Name of the YANG module containing extension statements
        stmt_meta (List[StmtMeta]): YANG extension statement metadata

    Returns:
        None:
    """
    # Register that we handle extensions from the YANG module
    # 'ericsson-yang-extensions'
    grammar.register_extension_module(module)

    for stmt, occurence, default, \
        (arg, v_arg, rules), \
            super_stmts, \
                (v_fun, err_codes) in stmt_meta:
        mod_stmt = (module, stmt)
        # Register the special grammar
        grammar.add_stmt(mod_stmt, (arg, rules))
        grammar.add_to_stmts_rules(super_stmts, [(mod_stmt, occurence)])

        if v_arg:
            if arg != 'string' and not arg in syntax.arg_type_map:
                syntax.add_arg_type(arg, v_arg)

        v_phase = 'expand_2'
        if v_fun:
            # Need to explicitly add keywords which are ancestors of ericsson
            # extensions possibly and are skipped for 'expand_2' phase which
            # only traverses the sub-statements of type i_children by default
            for super_stmt in super_stmts:
                if (not statements.is_keyword_with_children(super_stmt) and
                    not super_stmt in statements._v_i_children_keywords):
                    statements.add_keyword_phase_i_children(v_phase, super_stmt)
            # Register the keywords for which we validate statements
            statements.add_keyword_phase_i_children(v_phase, mod_stmt)
            statements.add_validation_fun(v_phase, [mod_stmt], v_fun)
            for err_tag, err_level, err_fmt in err_codes:
                # Register special error codes
                error.add_error_code(err_tag, err_level, err_fmt)
