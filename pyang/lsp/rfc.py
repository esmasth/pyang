"""YANG RFC Extract and References"""

#pylint: disable=line-too-long

stmt_map = {
    'module': {
        'title': 'The "`module`" Statement',
        'brief': 'The "`module`" statement defines the module\'s name and groups all statements that belong to the module together.  The "`module`" statement\'s argument is the name of the module, followed by a block of substatements that holds detailed module information.  The module name is an identifier (see [Section 6.2](https://datatracker.ietf.org/doc/html/rfc7950#section-6.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1',
    },
    'yang-version': {
        'title': 'The "`yang-version`" Statement',
        'brief': 'The "`yang-version`" statement specifies which version of the YANG language was used in developing the module.  The statement\'s argument is a string.  It MUST contain the value "`1.1`" for YANG modules defined based on this specification.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.2',
    },
    'namespace': {
        'title': 'The "`namespace`" Statement',
        'brief': 'The "`namespace`" statement defines the XML namespace that all identifiers defined by the module are qualified by in the XML encoding, with the exception of identifiers for data nodes, action nodes, and notification nodes defined inside a grouping (see [Section 7.13](https://datatracker.ietf.org/doc/html/rfc7950#section-7.13) for details).  The argument to the "`namespace`" statement is the URI of the namespace.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.3',
    },
    'prefix': {
        'title': 'The "`prefix`" Statement',
        'brief': 'The "`prefix`" statement is used to define the prefix associated with the module and its namespace.  The "`prefix`" statement\'s argument is the prefix string that is used as a prefix to access a module.  The prefix string MAY be used with the module to refer to definitions contained in the module, e.g., "`if:ifName`".  A prefix is an identifier (see [Section 6.2](https://datatracker.ietf.org/doc/html/rfc7950#section-6.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.4',
    },
    'import': {
        'title': 'The "`import`" Statement',
        'brief': 'The "`import`" statement makes definitions from one module available inside another module or submodule.  The argument is the name of the module to import, and the statement is followed by a block of substatements that holds detailed import information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
        'substmt': {
            'prefix': {
                'title': 'The `import`\'s "`prefix`" Statement',
                'brief': 'The mandatory `prefix` substatement assigns a prefix for the imported module that is scoped to the importing module or submodule.  Multiple `import` statements may be specified to import from different modules.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
            },
        },
    },
    'revision-date': {
        'title': 'The `import`\'s "`revision-date`" Statement',
        'brief': 'The `import`\'s "`revision-date`" statement is used to specify the version of the module to import.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5.1',
    },
    'include': {
        'title': 'The "`include`" Statement',
        'brief': 'The "`include`" statement is used to make content from a submodule available to that submodule\'s parent module.  The argument is an identifier that is the name of the submodule to include.  Modules are only allowed to include submodules that belong to that module, as defined by the `belongs-to` statement (see [Section 7.2.2](https://datatracker.ietf.org/doc/html/rfc7950#section-7.2.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.6',
    },
    'organization': {
        'title': 'The "`organization`" Statement',
        'brief': 'The "`organization`" statement defines the party responsible for this module.  The argument is a string that is used to specify a textual description of the organization(s) under whose auspices this module was developed.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.7',
    },
    'contact': {
        'title': 'The "`contact`" Statement',
        'brief': 'The "`contact`" statement provides contact information for the module. The argument is a string that is used to specify contact information for the person or persons to whom technical queries concerning this module should be sent, such as their name, postal address, telephone number, and electronic mail address.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.8',
    },
    'revision': {
        'title': 'The "`revision`" Statement',
        'brief': 'The "`revision`" statement specifies the editorial revision history of the module, including the initial revision.  A series of "revision" statements detail the changes in the module\'s definition.  The argument is a date string in the format "`YYYY-MM-DD`", followed by a block of substatements that holds detailed revision information.  A module SHOULD have at least one "`revision`" statement.  For every published editorial change, a new one SHOULD be added in front of the revisions sequence so that all revisions are in reverse chronological order.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.9',
    },
    'submodule': {
        'title': 'The "`submodule`" Statement',
        'brief': 'While the primary unit in YANG is a module, a YANG module can itself be constructed out of several submodules.  Submodules allow a module designer to split a complex model into several pieces where all the submodules contribute to a single namespace, which is defined by the module that includes the submodules.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2',
    },
    'belongs-to': {
        'title': 'The "`belongs-to`" Statement',
        'brief': 'The "`belongs-to`" statement specifies the module to which the submodule belongs.  The argument is an identifier that is the name of the module.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2.2',
    },
    'typedef': {
        'title': 'The "`typedef`" Statement',
        'brief': 'The "`typedef`" statement defines a new type that may be used locally in the module or submodule, and by other modules that import from it,  according to the rules in [Section 5.5](https://datatracker.ietf.org/doc/html/rfc7950#section-5.5).  The new type is called the "derived type", and the type from which it was derived is called the "base type".  All derived types can be traced back to a YANG built-in type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3',
        'substmt': {
            'type': {
                'title': 'The `typedef`\'s "`type`" Statement',
                'brief': 'The "`type`" statement, which MUST be present, defines the base type from which this type is derived.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.2',
            },
            'default': {
                'title': 'The `typedef`\'s "`default`" Statement',
                'brief': 'The "`default`" statement takes as an argument a string that contains a default value for the new type.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.4',
            },
        },
    },
    'units': {
        'title': 'The "`units`" Statement',
        'brief': 'The "`units`" statement, which is optional, takes as an argument a string that contains a textual definition of the units associated with the type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.3',
    },
    'type': {
        'title': 'The "`type`" Statement',
        'brief': 'The "`type`" statement takes as an argument a string that is the name of a YANG built-in type (see [Section 9](https://datatracker.ietf.org/doc/html/rfc7950#section-9)) or a derived type (see [Section 7.3](https://datatracker.ietf.org/doc/html/rfc7950#section-7.3)), followed by an optional block of substatements that is used to put further restrictions on the type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.4',
        'substmt': {
            'base': {
                'title': 'The `identityref`\'s "`base`" Statement',
                'brief': 'The "`base`" statement, which is a substatement to the "`type`" statement, MUST be present at least once if the type is "`identityref`".  The argument is the name of an identity, as defined by an "`identity`" statement.  If a prefix is present on the identity name, it refers to an identity defined in the module that was imported with that prefix.  Otherwise, an identity with the matching name MUST be defined in the current module or an included submodule.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.10.2',
            },
        },
    },
    'container': {
        'title': 'The "`container`" Statement',
        'brief': 'The "`container`" statement is used to define an interior data node in the schema tree.  It takes one argument, which is an identifier, followed by a block of substatements that holds detailed container information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5',
    },
    'must': {
        'title': 'The "`must`" Statement',
        'brief': 'The "`must`" statement, which is optional, takes as an argument a string that contains an XPath expression (see [Section 6.4](https://datatracker.ietf.org/doc/html/rfc7950#section-6.4)).  It is used to formally declare a constraint on valid data.  The constraint is enforced according to the rules in [Section 8](https://datatracker.ietf.org/doc/html/rfc7950#section-8).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.3',
    },
    'error-message': {
        'title': 'The "`error-message`" Statement',
        'brief': 'The "`error-message`" statement, which is optional, takes a string as an argument.  If the constraint evaluates to "`false`", the string is passed as `<error-message>` in the `<rpc-error>` in NETCONF.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.1',
    },
    'error-app-tag': {
        'title': 'The "`error-app-tag`" Statement',
        'brief': 'The "`error-app-tag`" statement, which is optional, takes a string as an argument.  If the constraint evaluates to "`false`", the string is passed as `<error-app-tag>` in the `<rpc-error>` in NETCONF.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.2',
    },
    'presence': {
        'title': 'The "`presence`" Statement',
        'brief': 'The "`presence`" statement assigns a meaning to the presence of a container in the data tree.  It takes as an argument a string that contains a textual description of what the node\'s presence means.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.5',
    },
    'leaf': {
        'title': 'The "`leaf`" Statement',
        'brief': 'The "`leaf`" statement is used to define a leaf node in the schema tree.  It takes one argument, which is an identifier, followed by a block of substatements that holds detailed leaf information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6',
        'substmt': {
            'type': {
                'title': 'The `leaf`\'s "`type`" Statement',
                'brief': 'The "`type`" statement, which MUST be present, takes as an argument the name of an existing built-in or derived type.  The optional substatements specify restrictions on this type.  See [Section 7.4](https://datatracker.ietf.org/doc/html/rfc7950#section-7.4) for details.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.3',
            },
            'default': {
                'title': 'The `leaf`\'s "`default`" Statement',
                'brief': 'The "`default`" statement, which is optional, takes as an argument a string that contains a default value for the leaf.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.4',
            },
            'mandatory': {
                'title': 'The `leaf`\'s "`mandatory`" Statement',
                'brief': 'The "`mandatory`" statement, which is optional, takes as an argument the string "`true`" or "`false`" and puts a constraint on valid data.  If not specified, the default is "`false`".',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.5',
            },
        },
    },
    'leaf-list': {
        'title': 'The "`leaf-list`" Statement',
        'brief': 'Where the "`leaf`" statement is used to define a simple scalar variable of a particular type, the "`leaf-list`" statement is used to define an array of a particular type.  The "`leaf-list`" statement takes one argument, which is an identifier, followed by a block of substatements that holds detailed leaf-list information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7',
        'substmt': {
            'default': {
                'title': 'The `leaf-list`\'s "`default`" Statement',
                'brief': 'The "`default`" statement, which is optional, takes as an argument a string that contains a default value for the leaf-list.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.4',
            },
        },
    },
    'min-elements': {
        'title': 'The "`min-elements`" Statement',
        'brief': 'The "`min-elements`" statement, which is optional, takes as an argument a non-negative integer that puts a constraint on valid list entries. A valid leaf-list or list MUST have at least min-elements entries.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.5',
    },
    'max-elements': {
        'title': 'The "`max-elements`" Statement',
        'brief': 'The "`max-elements`" statement, which is optional, takes as an argument a positive integer or the string "`unbounded`", which puts a constraint on valid list entries.  A valid leaf-list or list always has at most max-elements entries.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.6',
    },
    'ordered-by': {
        'title': 'The "`ordered-by`" Statement',
        'brief': 'The "`ordered-by`" statement defines whether the order of entries within a list are determined by the user or the system.  The argument is one of the strings "`system`" or "`user`".  If not present, ordering defaults to "`system`".',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.7',
    },
    'list': {
        'title': 'The "`list`" Statement',
        'brief': 'The "`list`" statement is used to define an interior data node in the schema tree.  A list node may exist in multiple instances in the data tree.  Each such instance is known as a list entry.  The "`list`" statement takes one argument, which is an identifier, followed by a block of substatements that holds detailed list information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8',
    },
    'key': {
        'title': 'The `list`\'s "`key`" Statement',
        'brief': 'The "`key`" statement, which MUST be present if the list represents configuration and MAY be present otherwise, takes as an argument a string that specifies a space-separated list of one or more leaf identifiers of this list.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.2',
    },
    'unique': {
        'title': 'The `list`\'s "`unique`" Statement',
        'brief': 'The "`unique`" statement is used to put constraints on valid list entries.  It takes as an argument a string that contains a space- separated list of schema node identifiers, which MUST be given in the descendant form (see the rule "`descendant-schema-nodeid`" in [Section 14](https://datatracker.ietf.org/doc/html/rfc7950#section-14)).  Each such schema node identifier MUST refer to a leaf.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.3',
    },
    'choice': {
        'title': 'The "`choice`" Statement',
        'brief': 'The "`choice`" statement defines a set of alternatives, only one of which may be present in any one data tree.  The argument is an identifier, followed by a block of substatements that holds detailed choice information.  The identifier is used to identify the choice node in the schema tree.  A choice node does not exist in the data tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9',
        'substmt': {
            'default': {
                'title': 'The `choice`\'s "`default`" Statement',
                'brief': 'The "`default`" statement indicates if a case should be considered as the default if no child nodes from any of the choice\'s cases exist. The argument is the identifier of the default "`case`" statement.  If the "`default`" statement is missing, there is no default case.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.3',
            },
            'mandatory': {
                'title': 'The `choice`\'s "`mandatory`" Statement',
                'brief': 'The "`mandatory`" statement, which is optional, takes as an argument the string "`true`" or "`false`" and puts a constraint on valid data.  If "`mandatory`" is "`true`", at least one node from exactly one of the choice\'s case branches MUST exist.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.4',
            },
        },
    },
    'case': {
        'title': 'The `choice`\'s "`case`" Statement',
        'brief': 'The "`case`" statement is used to define branches of the `choice`.  It takes as an argument an identifier, followed by a block of substatements that holds detailed case information.\n\nThe identifier is used to identify the case node in the schema tree. A case node does not exist in the data tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.2',
    },
    'anydata': {
        'title': 'The "`anydata`" Statement',
        'brief': 'The "`anydata`" statement defines an interior node in the schema tree. It takes one argument, which is an identifier, followed by a block of substatements that holds detailed anydata information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.10',
    },
    'anyxml': {
        'title': 'The "`anyxml`" Statement',
        'brief': 'The "`anyxml`" statement defines an interior node in the schema tree. It takes one argument, which is an identifier, followed by a block of substatements that holds detailed anyxml information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.11',
    },
    'grouping': {
        'title': 'The "`grouping`" Statement',
        'brief': 'The "`grouping`" statement is used to define a reusable block of nodes, which may be used locally in the module or submodule, and by other modules that import from it, according to the rules in [Section 5.5](https://datatracker.ietf.org/doc/html/rfc7950#section-5.5). It takes one argument, which is an identifier, followed by a block of substatements that holds detailed grouping information.\n\nThe "`grouping`" statement is not a data definition statement and, as such, does not define any nodes in the schema tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.12',
    },
    'uses': {
        'title': 'The "`uses`" Statement',
        'brief': 'The "`uses`" statement is used to reference a "`grouping`" definition. It takes one argument, which is the name of the grouping.\n\nThe effect of a "`uses`" reference to a grouping is that the nodes defined by the grouping are copied into the current schema tree and are then updated according to the "`refine`" and "`augment`" statements.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13',
    },
    'refine': {
        'title': 'The "`refine`" Statement',
        'brief': 'Some of the properties of each node in the grouping can be refined with the "`refine`" statement.  The argument is a string that identifies a node in the `grouping`.  This node is called the `refine`\'s target node.  If a node in the `grouping` is not present as a target node of a "`refine`" statement, it is not refined and thus is used exactly as it was defined in the `grouping`.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13.2',
    },
    'rpc': {
        'title': 'The "`rpc`" Statement',
        'brief': 'The "`rpc`" statement is used to define an RPC operation.  It takes one argument, which is an identifier, followed by a block of substatements that holds detailed `rpc` information.  This argument is the name of the RPC.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14',
    },
    'input': {
        'title': 'The "`input`" Statement',
        'brief': 'The "`input`" statement, which is optional, is used to define input parameters to the operation.  It does not take an argument.  The substatements to "`input`" define nodes under the operation\'s input node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.2',
    },
    'output': {
        'title': 'The "`output`" Statement',
        'brief': 'The "`output`" statement, which is optional, is used to define output parameters to the RPC operation.  It does not take an argument.  The substatements to "`output`" define nodes under the operation\'s output node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.3',
    },
    'action': {
        'title': 'The "`action`" Statement',
        'brief': 'The "`action`" statement is used to define an operation connected to a specific container or list data node.  It takes one argument, which is an identifier, followed by a block of substatements that holds detailed action information.  The argument is the name of the action.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.15',
    },
    'notification': {
        'title': 'The "`notification`" Statement',
        'brief': 'The "`notification`" statement is used to define a notification.  It takes one argument, which is an identifier, followed by a block of substatements that holds detailed notification information.  The "`notification`" statement defines a notification node in the schema tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.16',
    },
    'augment': {
        'title': 'The "`augment`" Statement',
        'brief': 'The "`augment`" statement allows a module or submodule to add to a schema tree defined in an external module, or in the current module and its submodules, and to add to the nodes from a grouping in a "`uses`" statement.  The argument is a string that identifies a node in the schema tree.  This node is called the `augment`\'s target node.  The target node MUST be either a `container`, `list`, `choice`, `case`, `input`, `output`, or `notification` node.  It is augmented with the nodes defined in the substatements that follow the "`augment`" statement.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.17',
    },
    'identity': {
        'title': 'The "`identity`" Statement',
        'brief': 'The "`identity`" statement is used to define a new globally unique, abstract, and untyped identity.  The identity\'s only purpose is to denote its name, semantics, and existence.  An identity can be either defined from scratch or derived from one or more base identities. The identity\'s argument is an identifier that is the name of the identity.  It is followed by a block of substatements that holds detailed identity information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18',
        'substmt': {
            'base': {
                'title': 'The "`base`" Statement',
                'brief': 'The "`base`" statement, which is optional, takes as an argument a string that is the name of an existing identity, from which the new identity is derived.  If no "`base`" statement is present, the identity is defined from scratch.  If multiple "`base`" statements are present, the identity is derived from all of them.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18.2',
            },
        },
    },
    'extension': {
        'title': 'The "`extension`" Statement',
        'brief': 'The "`extension`" statement allows the definition of new statements within the YANG language.  This new statement definition can be imported and used by other modules.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19',
    },
    'argument': {
        'title': 'The "`argument`" Statement',
        'brief': 'The "`argument`" statement, which is optional, takes as an argument a string that is the name of the argument to the keyword.  If no "`argument`" statement is present, the keyword expects no argument when it is used.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2',
    },
    'yin-element': {
        'title': 'The "`yin-element`" Statement',
        'brief': 'The "`yin-element`" statement, which is optional, takes as an argument the string "`true`" or "`false`".  This statement indicates whether the argument is mapped to an XML element in YIN or to an XML attribute (see [Section 13](https://datatracker.ietf.org/doc/html/rfc7950#section-13)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2.2',
    },
    'feature': {
        'title': 'The "`feature`" Statement',
        'brief': 'The "`feature`" statement is used to define a mechanism by which portions of the schema are marked as conditional.  A feature name is defined that can later be referenced using the "`if-feature`" statement (see [Section 7.20.2](https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.2)).  Schema nodes tagged with an "`if-feature`" statement are ignored by the server unless the server supports the given feature expression.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.1',
    },
    'if-feature': {
        'title': 'The "`if-feature`" Statement',
        'brief': 'The "`if-feature`" statement makes its parent statement conditional. The argument is a boolean expression over feature names.  In this expression, a feature name evaluates to "`true`" if and only if the feature is supported by the server.  The parent statement is implemented by servers where the boolean expression evaluates to "`true`".',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.2',
    },
    'deviation': {
        'title': 'The "`deviation`" Statement',
        'brief': 'The "`deviation`" statement defines a hierarchy of a module that the server does not implement faithfully.  The argument is a string that identifies the node in the schema tree where a deviation from the module occurs.  This node is called the deviation\'s target node.  The contents of the "`deviation`" statement give details about the deviation.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3',
    },
    'deviate': {
        'title': 'The "`deviate`" Statement',
        'brief': 'The "`deviate`" statement defines how the server\'s implementation of the target node deviates from its original definition.  The argument is one of the strings "`not-supported`", "`add`", "`replace`", or "`delete`".',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'config': {
        'title': 'The "`config`" Statement',
        'brief': 'The "`config`" statement takes as an argument the string "`true`" or "`false`".  If "`config`" is "`true`", the definition represents configuration.  Data nodes representing configuration are part of configuration datastores.\n\nIf "`config`" is "`false`", the definition represents state data.  Data nodes representing state data are not part of configuration datastores.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.1',
    },
    'status': {
        'title': 'The "`status`" Statement',
        'brief': 'The "`status`" statement takes as an argument one of the strings "`current`", "`deprecated`", or "`obsolete`".',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
    'description': {
        'title': 'The "`description`" Statement',
        'brief': 'The "`description`" statement takes as an argument a string that contains a human-readable textual description of this definition.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.3',
    },
    'reference': {
        'title': 'The "`reference`" Statement',
        'brief': 'The "`reference`" statement takes as an argument a string that is a human-readable cross-reference to an external document -- either another module that defines related management information or a document that provides additional information relevant to this definition.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.4',
    },
    'when': {
        'title': 'The "`when`" Statement',
        'brief': 'The "`when`" statement makes its parent data definition statement conditional.  The node defined by the parent data definition statement is only valid when the condition specified by the "`when`" statement is satisfied.  The statement\'s argument is an XPath expression (see [Section 6.4](https://datatracker.ietf.org/doc/html/rfc7950#section-6.4)), which is used to formally specify this condition.  If the XPath expression conceptually evaluates to "`true`" for a particular instance, then the node defined by the parent data definition statement is valid; otherwise, it is not.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.5',
    },
    'range': {
        'title': 'The "`range`" Statement',
        'brief': 'The "`range`" statement, which is an optional substatement to the "`type`" statement, takes as an argument a range expression string.  It is used to restrict integer and decimal built-in types, or types derived from them.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2.4',
    },
    'fraction-digits': {
        'title': 'The "`fraction-digits`" Statement',
        'brief': 'The "`fraction-digits`" statement, which is a substatement to the "`type`" statement, MUST be present if the type is "`decimal64`".  It takes as an argument an integer between `1` and `18`, inclusively.  It controls the size of the minimum difference between values of a `decimal64` type by restricting the value space to numbers that are expressible as "`i x 10^-n`" where `n` is the `fraction-digits` argument.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.3.4',
    },
    'length': {
        'title': 'The "`length`" Statement',
        'brief': 'The "`length`" statement, which is an optional substatement to the "`type`" statement, takes as an argument a length expression string. It is used to restrict the built-in types "`string`" and "`binary`" or types derived from them.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.4',
    },
    'pattern': {
        'title': 'The "`pattern`" Statement',
        'brief': 'The "pattern" statement, which is an optional substatement to the "type" statement, takes as an argument a regular expression string, as defined in [[XSD-TYPES](http://www.w3.org/TR/2004/REC-xmlschema-2-20041028)].  It is used to restrict the built-in type "string", or types derived from "string", to values that match the pattern.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.5',
    },
    'modifier': {
        'title': 'The "`modifier`" Statement',
        'brief': 'The "`modifier`" statement, which is an optional substatement to the "pattern" statement, takes as an argument the string "`invert-match`".\n\nIf a pattern has the "`invert-match`" modifier present, the type is restricted to values that do not match the pattern.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.6',
    },
    'enum': {
        'title': 'The "`enum`" Statement',
        'brief': 'The "`enum`" statement, which is a substatement to the "`type`" statement, MUST be present if the type is "`enumeration`".  It is repeatedly used to specify each assigned name of an enumeration type. It takes as an argument a string that is the assigned name.  The string MUST NOT be zero-length and MUST NOT have any leading or trailing whitespace characters (any Unicode character with the "White_Space" property).  The use of Unicode control codes SHOULD be avoided.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4',
    },
    'value': {
        'title': 'The "`value`" Statement',
        'brief': 'The "`value`" statement, which is optional, is used to associate an integer value with the assigned name for the enum.  This integer value MUST be in the range `-2147483648` to `2147483647`, and it MUST be unique within the enumeration type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4.2',
    },
    'bit': {
        'title': 'The "`bit`" Statement',
        'brief': 'The "`bit`" statement, which is a substatement to the "`type`" statement, MUST be present if the type is "`bits`".  It is repeatedly used to specify each assigned named bit of a bits type.  It takes as an argument a string that is the assigned name of the bit.  It is followed by a block of substatements that holds detailed bit information.  The assigned name follows the same syntax rules as an identifier (see [Section 6.2](https://datatracker.ietf.org/doc/html/rfc7950#section-6.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4',
    },
    'position': {
        'title': 'The "`position`" Statement',
        'brief': 'The "`position`" statement, which is optional, takes as an argument a non-negative integer value that specifies the bit\'s position within a hypothetical bit field.  The position value MUST be in the range `0` to `4294967295`, and it MUST be unique within the bits type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4.2',
    },
    'path': {
        'title': 'The "`path`" Statement',
        'brief': 'The "`path`" statement, which is a substatement to the "`type`" statement, MUST be present if the type is "`leafref`".  It takes as an argument a string that MUST refer to a `leaf` or `leaf-list` node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.2',
    },
    'require-instance': {
        'title': 'The "`require-instance`" Statement',
        'brief': 'The "`require-instance`" statement, which is a substatement to the "`type`" statement, MAY be present if the type is "`instance-identifier`" or "`leafref`".  It takes as an argument the string "`true`" or "`false`". If this statement is not present, it defaults to "`true`".',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.3',
    },
}

deviate_map = {
    'not-supported': {
        'title': '',
        'brief': 'The argument "`not-supported`" indicates that the target node is not implemented by this server.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'add': {
        'title': '',
        'brief': 'The argument "`add`" adds properties to the target node.  The properties to add are identified by substatements to the "`deviate`" statement.  If a property can only appear once, the property MUST NOT exist in the target node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'replace': {
        'title': '',
        'brief': 'The argument "`replace`" replaces properties of the target node.  The properties to replace are identified by substatements to the "`deviate`" statement.  The properties to replace MUST exist in the target node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'delete': {
        'title': '',
        'brief': 'The argument "`delete`" deletes properties from the target node.  The properties to delete are identified by substatements to the "`delete`" statement.  The substatement\'s keyword MUST match a corresponding keyword in the target node, and the argument\'s string MUST be equal to the corresponding keyword\'s argument string in the target node.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
}

status_map = {
    'current': {
        'title': '',
        'brief': '"`current`" means that the definition is current and valid.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
    'deprecated': {
        'title': '',
        'brief': '"`deprecated`" indicates an obsolete definition, but it permits new/continued implementation in order to foster interoperability with older/existing implementations.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
    'obsolete': {
        'title': '',
        'brief': '"`obsolete`" means that the definition is obsolete and SHOULD NOT be implemented and/or can be removed from implementations.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
}

type_map = {
    'int8': {
        'title': 'The Integer Built-In Types',
        'brief': '`int8`  represents integer values between `-128` and `127`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int16': {
        'title': 'The Integer Built-In Types',
        'brief': '`int16`  represents integer values between `-32768` and `32767`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int32': {
        'title': 'The Integer Built-In Types',
        'brief': '`int32`  represents integer values between `-2147483648` and `2147483647`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int64': {
        'title': 'The Integer Built-In Types',
        'brief': '`int64`  represents integer values between `-9223372036854775808` and `9223372036854775807`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint8': {
        'title': 'The Integer Built-In Types',
        'brief': '`uint8`  represents integer values between `0` and `255`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint16': {
        'title': 'The Integer Built-In Types',
        'brief': '`uint16`  represents integer values between `0` and `65535`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint32': {
        'title': 'The Integer Built-In Types',
        'brief': '`uint32`  represents integer values between 0 and 4294967295, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint64': {
        'title': 'The Integer Built-In Types',
        'brief': '`uint64`  represents integer values between 0 and 18446744073709551615, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'decimal64': {
        'title': 'The `decimal64` Built-In Type',
        'brief': 'The `decimal64` built-in type represents a subset of the real numbers, which can be represented by decimal numerals.  The value space of `decimal64` is the set of numbers that can be obtained by multiplying a 64-bit signed integer by a negative power of ten, i.e., expressible as `i x 10^-n` where `i` is an `integer64` and `n` is an integer between `1` and `18`, inclusively.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.3',
    },
    'string':{
        'title': 'The `string` Built-In Type',
        'brief': 'The `string` built-in type represents human-readable strings in YANG. Legal characters are the Unicode and ISO/IEC 10646 [[ISO.10646](https://www.iso.org/standard/63182.html)] characters, including tab, carriage return, and line feed but excluding the other C0 control  characters, the surrogate blocks, and the noncharacters.  The string syntax is formally defined by the rule `yang-string` in [Section 14](https://datatracker.ietf.org/doc/html/rfc7950#section-14).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4',
    },
    'boolean': {
        'title': 'The `boolean` Built-In Type',
        'brief': 'The `boolean` built-in type represents a boolean value.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.5',
    },
    'enumeration': {
        'title': 'The `enumeration` Built-In Type',
        'brief': 'The `enumeration` built-in type represents values from a set of assigned names.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6',
    },
    'bits': {
        'title': 'The `bits` Built-In Type',
        'brief': 'The `bits` built-in type represents a bit set.  That is, a bits value is a set of flags identified by small integer position numbers starting at `0`.  Each bit number has an assigned name.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7',
    },
    'binary': {
        'title': 'The `binary` Built-In Type',
        'brief': 'The `binary` built-in type represents any binary data, i.e., a sequence of octets.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.8',
    },
    'leafref': {
        'title': 'The `leafref` Built-In Type',
        'brief': 'The `leafref` built-in type is restricted to the value space of some `leaf` or `leaf-list` node in the schema tree and optionally further restricted by corresponding instance nodes in the data tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9',
    },
    'identityref': {
        'title': 'The `identityref` Built-In Type',
        'brief': 'The identityref built-in type is used to reference an existing identity (see [Section 7.18](https://datatracker.ietf.org/doc/html/rfc7950#section-7.18)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.10',
    },
    'empty': {
        'title': 'The `empty` Built-In Type',
        'brief': 'The `empty` built-in type represents a leaf that does not have any value; it conveys information by its presence or absence.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.11',
    },
    'union': {
        'title': 'The `union` Built-In Type',
        'brief': 'The `union` built-in type represents a value that corresponds to one of its member types.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.12',
    },
    'instance-identifier': {
        'title': 'The `instance-identifier` Built-In Type',
        'brief': 'The `instance-identifier` built-in type is used to uniquely identify a particular instance node in the data tree.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.13',
    },
}
