class JSRequiredHandler(object):
    """Run JavaScript to determine if the field is required."""

    def __init__(self, field, data):
        context = field.registry.get_js_context()
        # TODO catch errors
        self.f = context.eval('function f(form, path) {{ {} }}'.format(data['value']))

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['js']
                },
                'value': {
                    'type': 'string'
                }
            },
            'required': ['type', 'value'],
            'additionalProperties': False
        }

    def __call__(self, form, path):
        return self.f(form, path)


class JSDefaultHandler(object):
    """Run JavaScript to get the default for a field."""

    def __init__(self, field, data):
        context = field.registry.get_js_context()
        # TODO catch errors
        self.f = context.eval('function f(form, path) {{ {} }}'.format(data['value']))

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['js']
                },
                'value': {
                    'type': 'string'
                }
            },
            'required': ['type', 'value'],
            'additionalProperties': False
        }

    def __call__(self, form, path):
        return self.f(form, path)


class JSVisibleHandler(object):
    """Run JavaScript to determine if the field is visible."""

    def __init__(self, field, data):
        context = field.registry.get_js_context()
        # TODO catch errors
        self.f = context.eval('function f(form, path) {{ {} }}'.format(data['value']))

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'type': {
                    'enum': ['js']
                },
                'value': {
                    'type': 'string'
                }
            },
            'required': ['type', 'value'],
            'additionalProperties': False
        }

    def __call__(self, form, path):
        return self.f(form, path)
