"""YANG RFC Extract and References"""

#pylint: disable=line-too-long

stmt_map = {
    'module': {
        'title': 'The `module` Statement',
        'brief': 'The `module` statement defines the module\'s name and groups all statements that belong to the module together.  The `module` statement\'s argument is the name of the module, followed by a block of substatements that holds detailed module information.  The module name is an identifier (see [Section 6.2](https://datatracker.ietf.org/doc/html/rfc7950#section-6.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1',
    },
    'yang-version': {
        'title': 'The `yang-version` Statement',
        'brief': 'The `yang-version` statement specifies which version of the YANG language was used in developing the module.  The statement\'s argument is a string.  It MUST contain the value `1.1` for YANG modules defined based on this specification.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.2',
    },
    'namespace': {
        'title': 'The `namespace` Statement',
        'brief': 'The `namespace` statement defines the XML namespace that all identifiers defined by the module are qualified by in the XML encoding, with the exception of identifiers for data nodes, action nodes, and notification nodes defined inside a grouping (see [Section 7.13](https://datatracker.ietf.org/doc/html/rfc7950#section-7.13) for details).  The argument to the `namespace` statement is the URI of the namespace.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.3',
    },
    'prefix': {
        'title': 'The `prefix` Statement',
        'brief': 'The `prefix` statement is used to define the prefix associated with the module and its namespace.  The `prefix` statement\'s argument is the prefix string that is used as a prefix to access a module.  The prefix string MAY be used with the module to refer to definitions contained in the module, e.g., "if:ifName".  A prefix is an identifier (see Section 6.2).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.4',
    },
    'import': {
        'title': 'The `import` Statement',
        'brief': 'The `import` statement makes definitions from one module available inside another module or submodule.  The argument is the name of the module to import, and the statement is followed by a block of substatements that holds detailed import information.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
        'substmt': {
            'prefix': {
                'title': 'The `import`\'s `prefix` Statement',
                'brief': ' The mandatory `prefix` substatement assigns a prefix for the imported module that is scoped to the importing module or submodule.  Multiple `import` statements may be specified to import from different modules.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
            },
        },
    },
    'revision-date': {
        'title': 'The `import`\'s `revision-date` Statement',
        'brief': 'The `import`\'s `revision-date` statement is used to specify the version of the module to import.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5.1',
    },
    'include': {
        'title': 'The `include` Statement',
        'brief': 'The `include` statement is used to make content from a submodule available to that submodule\'s parent module.  The argument is an identifier that is the name of the submodule to include.  Modules are only allowed to include submodules that belong to that module, as defined by the `belongs-to` statement (see [Section 7.2.2](https://datatracker.ietf.org/doc/html/rfc7950#section-7.2.2)).',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.6',
    },
    'organization': {
        'title': 'The `organization` Statement',
        'brief': 'The `organization` statement defines the party responsible for this module.  The argument is a string that is used to specify a textual description of the organization(s) under whose auspices this module was developed.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.7',
    },
    'contact': {
        'title': 'The `contact` Statement',
        'brief': 'The `contact` statement provides contact information for the module. The argument is a string that is used to specify contact information for the person or persons to whom technical queries concerning this module should be sent, such as their name, postal address, telephone number, and electronic mail address.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.8',
    },
    'revision': {
        'title': 'The `revision` Statement',
        'brief': 'The `revision` statement specifies the editorial revision history of the module, including the initial revision.  A series of "revision" statements detail the changes in the module\'s definition.  The argument is a date string in the format "YYYY-MM-DD", followed by a block of substatements that holds detailed revision information.  A module SHOULD have at least one "revision" statement.  For every published editorial change, a new one SHOULD be added in front of the revisions sequence so that all revisions are in reverse chronological order.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.9',
    },
    'submodule': {
        'title': 'The `submodule` Statement',
        'brief': 'While the primary unit in YANG is a module, a YANG module can itself be constructed out of several submodules.  Submodules allow a module designer to split a complex model into several pieces where all the submodules contribute to a single namespace, which is defined by the module that includes the submodules.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2',
    },
    'belongs-to': {
        'title': 'The `belongs-to` Statement',
        'brief': 'The `belongs-to` statement specifies the module to which the submodule belongs.  The argument is an identifier that is the name of the module.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2.2',
    },
    'typedef': {
        'title': 'The `typedef` Statement',
        'brief': 'The "`typedef`" statement defines a new type that may be used locally in the module or submodule, and by other modules that import from it,  according to the rules in [Section 5.5](https://datatracker.ietf.org/doc/html/rfc7950#section-5.5).  The new type is called the "derived type", and the type from which it was derived is called the "base type".  All derived types can be traced back to a YANG built-in type.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3',
        'substmt': {
            'type': {
                'title': 'The `typedef`\'s `type` Statement',
                'brief': 'The "`type`" statement, which MUST be present, defines the base type from which this type is derived.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.2',
            },
            'default': {
                'title': 'The `typedef`\'s `default` Statement',
                'brief': 'The "`default`" statement takes as an argument a string that contains a default value for the new type.',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.4',
            },
        },
    },
    'units': {
        'title': 'The `units` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.3',
    },
    'type': {
        'title': 'The `type` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.4',
    },
    'container': {
        'title': 'The `container` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5',
    },
    'must': {
        'title': 'The `must` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.3',
    },
    'error-message': {
        'title': 'The `error-message` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.1',
    },
    'error-app-tag': {
        'title': 'The `error-app-tag` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.2',
    },
    'presence': {
        'title': 'The `presence` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.5',
    },
    'leaf': {
        'title': 'The `leaf` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6',
        'substmt': {
            'type': {
                'title': 'The `leaf`\'s `type` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.3',
            },
            'default': {
                'title': 'The `leaf`\'s `default` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.4',
            },
            'mandatory': {
                'title': 'The `leaf`\'s `mandatory` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.5',
            },
        },
    },
    'leaf-list': {
        'title': 'The `leaf-list` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7',
        'substmt': {
            'default': {
                'title': 'The `leaf-list`\'s `default` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.4',
            },
        },
    },
    'min-elements': {
        'title': 'The `min-elements` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.5',
    },
    'max-elements': {
        'title': 'The `max-elements` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.6',
    },
    'ordered-by': {
        'title': 'The `ordered-by` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.7',
    },
    'list': {
        'title': 'The `list` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8',
    },
    'key': {
        'title': 'The `list`\'s `key` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.2',
    },
    'unique': {
        'title': 'The `list`\'s `unique` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.3',
    },
    'choice': {
        'title': 'The `choice` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9',
        'substmt': {
            'default': {
                'title': 'The `choice`\'s `default` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.3',
            },
            'mandatory': {
                'title': 'The `choice`\'s `mandatory` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.4',
            },
        },
    },
    'case': {
        'title': 'The `choice`\'s `case` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.2',
    },
    'anydata': {
        'title': 'The `anydata` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.10',
    },
    'anyxml': {
        'title': 'The `anyxml` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.11',
    },
    'grouping': {
        'title': 'The `grouping` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.12',
    },
    'uses': {
        'title': 'The `uses` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13',
    },
    'refine': {
        'title': 'The `refine` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13.2',
    },
    'rpc': {
        'title': 'The `rpc` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14',
    },
    'input': {
        'title': 'The `input` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.2',
    },
    'output': {
        'title': 'The `output` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.3',
    },
    'action': {
        'title': 'The `action` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.15',
    },
    'notification': {
        'title': 'The `notification` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.16',
    },
    'augment': {
        'title': 'The `augment` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.17',
    },
    'identity': {
        'title': 'The `identity` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18',
        'substmt': {
            'base': {
                'title': 'The `base` Statement',
                'brief': '',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18.2',
            },
        }
    },
    'extension': {
        'title': 'The `extension` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19',
    },
    'argument': {
        'title': 'The `argument` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2',
    },
    'yin-element': {
        'title': 'The `yin-element` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2.2',
    },
    'feature': {
        'title': 'The `feature` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.1',
    },
    'if-feature': {
        'title': 'The `if-feature` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.2',
    },
    'deviation': {
        'title': 'The `deviation` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3',
    },
    'deviate': {
        'title': 'The `deviate` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'config': {
        'title': 'The `config` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.1',
    },
    'status': {
        'title': 'The `status` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
    'description': {
        'title': 'The `description` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.3',
    },
    'reference': {
        'title': 'The `reference` Statement',
        'brief': 'The `reference` statement takes as an argument a string that is a human-readable cross-reference to an external document -- either another module that defines related management information or a document that provides additional information relevant to this definition.',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.4',
    },
    'when': {
        'title': 'The `when` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.5',
    },
    'range': {
        'title': 'The `range` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2.4',
    },
    'fraction-digits': {
        'title': 'The `fraction-digits` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.3.4',
    },
    'length': {
        'title': 'The `length` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.4',
    },
    'pattern': {
        'title': 'The `pattern` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.5',
    },
    'modifier': {
        'title': 'The `modifier` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.6',
    },
    'enum': {
        'title': 'The `enum` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4',
    },
    'value': {
        'title': 'The `value` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4.2',
    },
    'bit': {
        'title': 'The `bit` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4',
    },
    'position': {
        'title': 'The `position` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4.2',
    },
    'path': {
        'title': 'The `path` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.2',
    },
    'require-instance': {
        'title': 'The `require-instance` Statement',
        'brief': '',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.3',
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
        'brief': 'The `bits` built-in type represents a bit set.  That is, a bits value is a set of flags identified by small integer position numbers starting at 0.  Each bit number has an assigned name.',
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
