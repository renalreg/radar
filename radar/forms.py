from wtforms.widgets import TextInput
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