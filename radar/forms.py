from wtforms import SelectField, SelectMultipleField
from wtforms.widgets import TextInput, Select
from wtforms.ext.dateutil.fields import DateField


class RadarDateField(DateField):
    def __init__(self, label=None, widget=None, display_format="%d/%m/%Y", **kwargs):
        if widget is None:
            widget = RadarDateInput()

        super(RadarDateField, self).__init__(label, widget=widget, display_format=display_format, **kwargs)


class RadarDateInput(TextInput):
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (c, 'datepicker')
        return super(RadarDateInput, self).__call__(field, **kwargs)


class RadarSelectField(SelectField):
    def process_data(self, value):
        # Fix for SelectField converting None to "None"
        if value is None:
            value = ''

        super(SelectField, self).process_data(value)


class RadarSelectMultiple(Select):
    def __init__(self):
        super(RadarSelectMultiple, self).__init__(True)

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (c, 'chosen-select')
        return super(RadarSelectMultiple, self).__call__(field, **kwargs)


class RadarSelectMultipleField(SelectMultipleField):
    def __init__(self, label=None, widget=None, **kwargs):
        if widget is None:
            widget = RadarSelectMultiple()

        super(RadarSelectMultipleField, self).__init__(label, widget=widget, **kwargs)