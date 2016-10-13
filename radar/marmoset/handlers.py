class JSHandler(object):
    def __init__(self, field, data):
        context = field.registry.get_js_context()
        # TODO catch errors
        self.f = context.eval('function f(form, path) {{ {} }}'.format(data['value']))

    @classmethod
    def get_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'name': {
                    'enum': ['js']
                },
                'value': {
                    'type': 'string'
                }
            },
            'required': ['name', 'value'],
            'additionalProperties': False
        }

    def __call__(self, form, path):
        return self.f(form, path)


class JSRequiredHandler(JSHandler):
    """Determine if the field is required by running a JavaScript function."""


class JSDefaultHandler(JSHandler):
    """Get the default for a field by running a JavaScript function."""


class JSVisibleHandler(JSHandler):
    """Determine if the field is visible by running a JavaScript function."""


class JSFormulaHandler(JSHandler):
    """Calculate the field's value using a JavaScript function."""
