from collections import OrderedDict
from flask import Markup, escape

class FormBuilder(object):
    def __init__(self, form):
        self.form = form

    @classmethod
    def _input_tag(cls, attributes):
        attributes_str = ' '.join(['%s="%s"' % (k, escape(v)) for k, v in attributes.items()])
        return Markup('<input %s />' % attributes_str)

    def text_field(self, model_attr, extra_attributes=None):
        model_value = getattr(self.form.obj, model_attr, None)

        if model_value is None:
            value = self.form.stash.get(model_attr, '')
        else:
            value = model_value

        attributes = {'name': model_attr, 'value': value, 'type': 'text'}

        if extra_attributes is not None:
            attributes.update(extra_attributes)

        return self._input_tag(attributes)

    def date_field(self, model_attr, datetime_format='%d/%m/%Y', extra_attributes=None):
        model_value = getattr(self.form.obj, model_attr, None)

        if model_value is None:
            value = self.form.stash.get(model_attr, '')
        else:
            value = model_value.strftime(datetime_format)

        attributes = {'name': model_attr, 'value': value, 'type': 'text'}

        if extra_attributes is not None:
            attributes.update(extra_attributes)

        return self._input_tag(attributes)

    def errors(self, model_attr):
        # TODO use error codes

        # Unique errors
        return list(OrderedDict.fromkeys(self.form.errors[model_attr]))