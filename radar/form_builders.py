from collections import OrderedDict
from flask import Markup, escape
from radar.utils import humanize_datetime_format


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

    def text_field(self, model_key, attributes=None):
        if attributes is None:
            attributes = {}

        model_value = self.form.get_model_value(model_key)

        if model_value is None:
            value = self.form.stash.get(model_key, '')
        else:
            value = model_value

        attributes.setdefault('id', model_key)
        attributes.setdefault('name', model_key)
        attributes.setdefault('value', value)
        attributes.setdefault('type', 'text')

        return self._input_tag(attributes)

    def date_field(self, model_key, datetime_format='%d/%m/%Y', attributes=None):
        if attributes is None:
            attributes = {}

        model_value = self.form.get_model_value(model_key)

        if model_value is None:
            value = self.form.stash.get(model_key, '')
        else:
            value = model_value.strftime(datetime_format)

        attributes.setdefault('id', model_key)
        attributes.setdefault('name', model_key)
        attributes.setdefault('value', value)
        attributes.setdefault('type', 'text')
        attributes.setdefault('placeholder', humanize_datetime_format(datetime_format))

        return self._input_tag(attributes)

    def select(self, model_key, choices, include_blank=False, attributes=None):
        if attributes is None:
            attributes = {}

        model_value = self.form.get_model_value(model_key)

        if include_blank:
            choices.insert(0, ('', ''))

        options = []

        for label, value in choices:
            if model_value == value:
                option = '<option value="%s" selected="selected">%s</option>' % (escape(value), escape(label))
            else:
                option = '<option value="%s">%s</option>' % (escape(value), escape(label))

            options.append(option)

        options_str = ''.join(options)

        attributes.setdefault('id', model_key)
        attributes.setdefault('name', model_key)

        return Markup('<select %s>%s</select>' % (self._attributes_to_str(attributes), options_str))

    def errors(self, model_key):
        # TODO use error codes

        # Unique errors
        return list(OrderedDict.fromkeys(self.form.errors[model_key]))

class RadarFormBuilder(FormBuilder):
    def text_field(self, model_key, attributes=None):
        if attributes is None:
            attributes = {}

        attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).text_field(model_key, attributes)

    def date_field(self, model_key, datetime_format='%d/%m/%Y', attributes=None):
        if attributes is None:
            attributes = {}

        attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).date_field(model_key, datetime_format, attributes)

    def select(self, model_key, choices, include_blank=False, attributes=None):
        if attributes is None:
            attributes = {}

        attributes.setdefault('class', 'form-control')

        return super(RadarFormBuilder, self).select(model_key, choices, include_blank, attributes)