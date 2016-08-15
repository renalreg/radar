import copy
import json
import pkg_resources

import js2py

from radar.marmoset.exceptions import SchemaError

SCHEMA = json.load(pkg_resources.resource_stream(__name__, 'schema.json'))


class BaseRegistry(object):
    def __init__(self):
        self.schema = copy.deepcopy(SCHEMA)
        self.parsers = {}
        self.formatters = {}
        self.validators = {}
        self.defaults = {}
        self.required = {}
        self.visible = {}
        self.helpers = []

    def _get_schema(self, name):
        return self.schema['items']['properties'][name]

    def add_parser(self, type, f):
        self.parsers[type] = f

    def get_parser(self, type):
        try:
            return self.parsers[type]
        except KeyError:
            raise SchemaError()

    def add_formatter(self, type, f):
        self.formatters[type] = f

    def get_formatter(self, type):
        try:
            return self.formatters[type]
        except KeyError:
            raise SchemaError()

    def add_default(self, type, name, f):
        schema = f.get_schema()
        self._get_schema('default')['oneOf'].append(schema)
        self.defaults.setdefault(type, {})[name] = f

    def get_default(self, type, name):
        try:
            return self.defaults[type][name]
        except KeyError:
            raise SchemaError()

    def add_required(self, name, f):
        schema = f.get_schema()
        self._get_schema('required')['oneOf'].append(schema)
        self.required[name] = f

    def get_required(self, name):
        try:
            return self.defaults[name]
        except KeyError:
            raise SchemaError()

    def add_visible(self, name, f):
        schema = f.get_schema()
        self._get_schema('visible')['oneOf'].append(schema)
        self.visible[name] = f

    def get_visible(self, name):
        try:
            return self.visible[name]
        except KeyError:
            raise SchemaError()

    def add_validator(self, type, name, f):
        schema = f.get_schema()
        self._get_schema('validators')['items']['oneOf'].append(schema)
        self.validators.setdefault(type, {})[name] = f

    def get_validator(self, type, name):
        try:
            return self.validators[type][name]
        except KeyError:
            raise SchemaError()

    def add_js(self, value):
        self.helpers.append(value)

    def get_js_context(self):
        context = js2py.EvalJs()

        for helper in self.helpers:
            context.eval(helper)

        return context
