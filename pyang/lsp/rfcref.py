"""YANG RFC References"""

rfcref_stmt_map = {
    'module': {
        'title': 'The `module` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1',
    },
    'yang-version': {
        'title': 'The `yang-version` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.2',
    },
    'namespace': {
        'title': 'The `namespace` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.3',
    },
    'prefix': {
        'title': 'The `prefix` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.4',
    },
    'import': {
        'title': 'The `import` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
        'substmt': {
            'prefix': {
                'title': 'The `import`\'s `prefix` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5',
            },
        },
    },
    'revision-date': {
        'title': 'The `revision-date` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.5.1',
    },
    'include': {
        'title': 'The `include` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.6',
    },
    'organization': {
        'title': 'The `organization` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.7',
    },
    'contact': {
        'title': 'The `contact` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.8',
    },
    'revision': {
        'title': 'The `revision` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.1.9',
    },
    'submodule': {
        'title': 'The `submodule` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2',
    },
    'belongs-to': {
        'title': 'The `belongs-to` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.2.2',
    },
    'typedef': {
        'title': 'The `typedef` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3',
        'substmt': {
            'type': {
                'title': 'The `typedef`\'s `type` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.2',
            },
            'default': {
                'title': 'The `typedef`\'s `default` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.4',
            },
        },
    },
    'units': {
        'title': 'The `units` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.3.3',
    },
    'type': {
        'title': 'The `type` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.4',
    },
    'container': {
        'title': 'The `container` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5',
    },
    'must': {
        'title': 'The `must` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.3',
    },
    'error-message': {
        'title': 'The `error-message` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.1',
    },
    'error-app-tag': {
        'title': 'The `error-app-tag` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.4.2',
    },
    'presence': {
        'title': 'The `presence` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.5.5',
    },
    'leaf': {
        'title': 'The `leaf` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6',
        'substmt': {
            'type': {
                'title': 'The `leaf`\'s `type` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.3',
            },
            'default': {
                'title': 'The `leaf`\'s `default` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.4',
            },
            'mandatory': {
                'title': 'The `leaf`\'s `mandatory` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.6.5',
            },
        },
    },
    'leaf-list': {
        'title': 'The `leaf-list` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7',
        'substmt': {
            'default': {
                'title': 'The `leaf-list`\'s `default` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.4',
            },
        },
    },
    'min-elements': {
        'title': 'The `min-elements` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.5',
    },
    'max-elements': {
        'title': 'The `max-elements` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.6',
    },
    'ordered-by': {
        'title': 'The `ordered-by` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.7.7',
    },
    'list': {
        'title': 'The `list` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8',
    },
    'key': {
        'title': 'The `list`\'s `key` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.2',
    },
    'unique': {
        'title': 'The `list`\'s `unique` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.8.3',
    },
    'choice': {
        'title': 'The `choice` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9',
        'substmt': {
            'default': {
                'title': 'The `choice`\'s `default` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.3',
            },
            'mandatory': {
                'title': 'The `choice`\'s `mandatory` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.4',
            },
        },
    },
    'case': {
        'title': 'The `choice`\'s `case` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.9.2',
    },
    'anydata': {
        'title': 'The `anydata` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.10',
    },
    'anyxml': {
        'title': 'The `anyxml` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.11',
    },
    'grouping': {
        'title': 'The `grouping` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.12',
    },
    'uses': {
        'title': 'The `uses` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13',
    },
    'refine': {
        'title': 'The `refine` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.13.2',
    },
    'rpc': {
        'title': 'The `rpc` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14',
    },
    'input': {
        'title': 'The `input` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.2',
    },
    'output': {
        'title': 'The `output` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.14.3',
    },
    'action': {
        'title': 'The `action` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.15',
    },
    'notification': {
        'title': 'The `notification` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.16',
    },
    'augment': {
        'title': 'The `augment` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.17',
    },
    'identity': {
        'title': 'The `identity` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18',
        'substmt': {
            'base': {
                'title': 'The `base` Statement',
                'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.18.2',
            },
        }
    },
    'extension': {
        'title': 'The `extension` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19',
    },
    'argument': {
        'title': 'The `argument` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2',
    },
    'yin-element': {
        'title': 'The `yin-element` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.19.2.2',
    },
    'feature': {
        'title': 'The `feature` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.1',
    },
    'if-feature': {
        'title': 'The `if-feature` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.2',
    },
    'deviation': {
        'title': 'The `deviation` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3',
    },
    'deviate': {
        'title': 'The `deviate` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.20.3.2',
    },
    'config': {
        'title': 'The `config` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.1',
    },
    'status': {
        'title': 'The `status` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.2',
    },
    'description': {
        'title': 'The `description` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.3',
    },
    'reference': {
        'title': 'The `reference` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.4',
    },
    'when': {
        'title': 'The `when` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-7.21.5',
    },
    'range': {
        'title': 'The `range` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2.4',
    },
    'fraction-digits': {
        'title': 'The `fraction-digits` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.3.4',
    },
    'length': {
        'title': 'The `length` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.4',
    },
    'pattern': {
        'title': 'The `pattern` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.5',
    },
    'modifier': {
        'title': 'The `modifier` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4.6',
    },
    'enum': {
        'title': 'The `enum` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4',
    },
    'value': {
        'title': 'The `value` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6.4.2',
    },
    'bit': {
        'title': 'The `bit` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4',
    },
    'position': {
        'title': 'The `position` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7.4.2',
    },
    'path': {
        'title': 'The `path` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.2',
    },
    'require-instance': {
        'title': 'The `require-instance` Statement',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9.3',
    },
}

rfcref_type_map = {
    'int8': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int16': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int32': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'int64': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint8': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint16': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint32': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'uint64': {
        'title': 'The Integer Built-In Types',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.2',
    },
    'decimal64': {
        'title': 'The decimal64 Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.3',
    },
    'string':{
        'title': 'The `string` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.4',
    },
    'boolean': {
        'title': 'The `boolean` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.5',
    },
    'enumeration': {
        'title': 'The `enumeration` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.6',
    },
    'bits': {
        'title': 'The `bits` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.7',
    },
    'binary': {
        'title': 'The `binary` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.8',
    },
    'leafref': {
        'title': 'The `leafref` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.9',
    },
    'identityref': {
        'title': 'The `identityref` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.10',
    },
    'empty': {
        'title': 'The `empty` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.11',
    },
    'union': {
        'title': 'The `union` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.12',
    },
    'instance-identifier': {
        'title': 'The `instance-identifier` Built-In Type',
        'uri': 'https://datatracker.ietf.org/doc/html/rfc7950#section-9.13',
    },
}
