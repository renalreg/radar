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

        self.seen_defaults = set()
        self.defaults = {}

        self.required = {}
        self.visible = {}

        self.seen_validators = set()
        self.validators = {}

        self.formula = {}

        self.helpers = []

    def _get_property(self, name, index=0):
        return self.schema['items']['oneOf'][index]['properties'][name]

    def add_type(self, type, parser, formatter):
        self.parsers[type] = parser
        self.formatters[type] = formatter

    def get_parser(self, type):
        try:
            return self.parsers[type]
        except KeyError:
            raise SchemaError()

    def get_formatter(self, type):
        try:
            return self.formatters[type]
        except KeyError:
            raise SchemaError()

    def add_default(self, name, f, type=None):
        if name not in self.seen_defaults:
            schema = f.get_schema()
            p = self._get_property('default')
            schemas = p['oneOf']
            schemas.append(schema)
            self.seen_defaults.add(name)

        self.defaults.setdefault(type, {})[name] = f

    def get_default(self, type, name):
        try:
            return self.defaults[type][name]
        except KeyError:
            try:
                return self.defaults[None][name]
            except KeyError:
                raise SchemaError()

    def add_required(self, name, f):
        if name not in self.required:
            schema = f.get_schema()
            p = self._get_property('required')
            schemas = p['oneOf']
            schemas.append(schema)

        self.required[name] = f

    def get_required(self, name):
        try:
            return self.defaults[name]
        except KeyError:
            raise SchemaError()

    def add_visible(self, name, f):
        if name not in self.visible:
            schema = f.get_schema()

            for index in (0, 1):
                p = self._get_property('visible', index=0)
                schemas = p['oneOf']
                schemas.append(schema)

        self.visible[name] = f

    def get_visible(self, name):
        try:
            return self.visible[name]
        except KeyError:
            raise SchemaError()

    def add_validator(self, name, f, type=None):
        if name not in self.seen_validators:
            p = self._get_property('validators')
            schema = f.get_schema()
            schemas = p['items']['oneOf']
            schemas.append(schema)
            self.seen_validators.add(name)

        self.validators.setdefault(type, {})[name] = f

    def get_validator(self, type, name):
        try:
            return self.validators[type][name]
        except KeyError:
            try:
                return self.validators[None][name]
            except KeyError:
                raise SchemaError()

    def add_formula(self, name, f):
        if name not in self.formula:
            schema = f.get_schema()
            p = self._get_property('formula', index=1)
            schemas = p['oneOf']
            schemas.append(schema)

        self.formula[name] = f

    def get_formula(self, name):
        try:
            return self.formula[name]
        except KeyError:
            raise SchemaError()

    def add_js(self, code):
        self.helpers.append(code)

    def get_js_context(self):
        context = js2py.EvalJs()

        for helper in self.helpers:
            context.eval(helper)

        return context
