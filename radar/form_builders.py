from collections import OrderedDict
from flask import Markup, escape

class FormBuilder(object):
    def __init__(self, form):
        self.form = form

    @classmethod
    def _input_tag(cls, attributes):
        attributes_str = cls._attributes_to_str(attributes)
        return Markup('<input %s />' % attributes_str)

    @classmethod
    def _attributes_to_str(cls, attributes=None):
        return ' '.join(['%s="%s"' % (k, escape(v)) for k, v in attributes.items()])

    def text_field(self, model_key, extra_attributes=None):
        model_value = self.form.get_model_value(model_key)

        if model_value is None:
            value = self.form.stash.get(model_key, '')
        else:
            value = model_value

        attributes = {'id': model_key, 'name': model_key, 'value': value, 'type': 'text'}

        if extra_attributes is not None:
            attributes.update(extra_attributes)

        return self._input_tag(attributes)

    def date_field(self, model_key, datetime_format='%d/%m/%Y', extra_attributes=None):
        model_value = self.form.get_model_value(model_key)

        if model_value is None:
            value = self.form.stash.get(model_key, '')
        else:
            value = model_value.strftime(datetime_format)

        attributes = {'id': model_key, 'name': model_key, 'value': value, 'type': 'text'}

        if extra_attributes is not None:
            attributes.update(extra_attributes)

        return self._input_tag(attributes)

    def select(self, model_key, choices, extra_attributes=None):
        model_value = self.form.get_model_value(model_key)

        options = []

        for label, value in choices:
            if model_value == value:
                option = '<option value="%s" selected="selected">%s</option>' % (escape(value), escape(label))
            else:
                option = '<option value="%s">%s</option>' % (escape(value), escape(label))

            options.append(option)

        options_str = ''.join(options)

        attributes = {'id': model_key, 'name': model_key}

        if extra_attributes is not None:
            attributes.update(extra_attributes)

        return Markup('<select %s>%s</select>' % (self._attributes_to_str(attributes), options_str))

    def errors(self, model_key):
        # TODO use error codes

        # Unique errors
        return list(OrderedDict.fromkeys(self.form.errors[model_key]))

class RadarFormBuilder(FormBuilder):
    def text_field(self, model_key, extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}

        extra_attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).text_field(model_key, extra_attributes)

    def date_field(self, model_key, datetime_format='%d/%m/%Y', extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}

        extra_attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).date_field(model_key, datetime_format, extra_attributes)

    def select(self, model_key, choices, extra_attributes=None):
        if extra_attributes is None:
            extra_attributes = {}

        extra_attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).select(model_key, choices, extra_attributes)