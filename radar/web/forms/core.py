from datetime import date

import re
from flask_login import current_user
from markupsafe import Markup
from wtforms import SelectField, SelectMultipleField, ValidationError, StringField, IntegerField, Field, DateField, \
    RadioField
from wtforms.validators import InputRequired
from wtforms.widgets import TextInput, Select, HTMLString, html_params
from flask_wtf import Form

from radar.lib.auth import check_password_policy
from radar.lib.validation.utils import validate_nhs_no, validate_postcode


class RadarDateField(DateField):
    def __init__(self, label=None, widget=None, **kwargs):
        if widget is None:
            widget = RadarDateInput()

        super(RadarDateField, self).__init__(label, widget=widget, format="%d/%m/%Y", **kwargs)


class RadarDOBField(RadarDateField):
    def __init__(self, label="Date of Birth", widget=None, **kwargs):
        if widget is None:
            widget = RadarDOBInput()

        super(RadarDOBField, self).__init__(label, widget=widget, **kwargs)

    def process_formdata(self, valuelist):
        super(RadarDOBField, self).process_formdata(valuelist)

        if self.data and self.data > date.today():
            raise ValidationError("Can't be in the future.")


class RadarDateInput(TextInput):
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (c, 'datepicker')

        kwargs['data-date-format'] = 'dd/mm/yy'
        kwargs.setdefault('placeholder', 'DD/MM/YYYY')

        return super(RadarDateInput, self).__call__(field, **kwargs)


class RadarDOBInput(RadarDateInput):
    def __call__(self, field, **kwargs):
        # Can't be in the future
        kwargs['data-max-date'] = '0D'

        return super(RadarDOBInput, self).__call__(field, **kwargs)


class RadarSelectField(SelectField):
    def process_data(self, value):
        # Fix for SelectField converting None to "None"
        if value is None:
            self.data = None
        else:
            super(RadarSelectField, self).process_data(value)


class RadarSelectObjectField(SelectField):
    widget = Select()

    def iter_choices(self):
        for value, label, obj in self.choices:
            yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        for value, label, obj in self.choices:
            if self.data == value:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

    @property
    def obj(self):
        for value, label, obj in self.choices:
            if self.data == value:
                return obj

        return None


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


class RadarNHSNoField(IntegerField):
    def __init__(self, label='NHS No.', **kwargs):
        super(RadarNHSNoField, self).__init__(label=label, **kwargs)

    def process_formdata(self, valuelist):
        super(RadarNHSNoField, self).process_formdata(valuelist)

        if self.data and not validate_nhs_no(self.data):
            raise ValidationError('Not a valid NHS number.')


class RadarCHINoField(IntegerField):
    def __init__(self, label='CHI No.', **kwargs):
        super(RadarCHINoField, self).__init__(label=label, **kwargs)

    def process_formdata(self, valuelist):
        super(RadarCHINoField, self).process_formdata(valuelist)

        if self.data and not validate_nhs_no(self.data):
            raise ValueError('Not a valid CHI number.')


class RadarPostcodeField(StringField):
    def process_formdata(self, valuelist):
        super(RadarPostcodeField, self).process_formdata(valuelist)

        if self.data and not validate_postcode(self.data):
            raise ValueError('Not a valid postcode.')


class RadarYesNoField(Field):
    def __init__(self, label=None, widget=None, **kwargs):
        if widget is None:
            widget = RadarYesNoWidget()

        super(RadarYesNoField, self).__init__(label=label, widget=widget, **kwargs)

    def _value(self):
        """ Value to use in the input tag """

        if self.data is None:
            return None
        elif self.data:
            return 'y'
        else:
            return 'n'

    def process_formdata(self, valuelist):
        """ Convert form value to a boolean """

        try:
            value = valuelist[0]

            if value == 'y':
                self.data = True
            elif value == 'n':
                self.data = False
            else:
                self.data = None
        except IndexError:
            self.data = None


class RadarYesNoWidget(object):
    def __call__(self, field, **kwargs):
        html_attributes = kwargs
        html_attributes.update({
            'id': field.id,
            'name': field.name,
        })

        html = []

        for value, label in [('y', 'Yes'), ('n', 'No'), ('', 'Not Answered')]:
            field_value = field._value()
            checked = field_value == value or (value == '' and field_value is None)
            html_attributes['checked'] = checked
            html_attributes['value'] = value
            input_tag = '<input type="radio" {} />\n'.format(html_params(**html_attributes))
            html.append('<label class="radio-inline">%s %s</label>' % (input_tag, label))

        return HTMLString("\n".join(html))


class RadarStringField(StringField):
    def __init__(self, label=None, none_if_empty=True, strip=True, **kwargs):
        self.none_if_empty = none_if_empty
        self.strip = strip
        super(RadarStringField, self).__init__(label=label, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            value = valuelist[0]

            if self.none_if_empty and len(value) == 0:
                value = None
        elif self.none_if_empty:
            value = None
        else:
            value = ''

        if self.strip and value is not None:
            value = value.strip()

        self.data = value


class RadarRadioField(RadioField):
    def process_data(self, value):
        # Fix for RadioField converting None to "None"
        if value is None:
            self.data = None
        else:
            super(RadarRadioField, self).process_data(value)


class RadarInlineRadioField(RadarRadioField):
    def __init__(self, label=None, widget=None, **kwargs):
        if widget is None:
            widget = RadarInlineRadioWidget()

        super(RadarInlineRadioField, self).__init__(label=label, widget=widget, **kwargs)


class RadarInlineRadioWidget(object):
    def __call__(self, field, **kwargs):
        html = []

        for subfield in field:
            html.append('<label class="radio-inline">%s %s</label>' % (subfield(), subfield.label.text))

        return HTMLString("\n".join(html))


class RadarMeasurementInput(TextInput):
    def __init__(self, unit):
        super(RadarMeasurementInput, self).__init__()
        self.unit = unit

    def __call__(self, field, **kwargs):
        return Markup('<div class="input-group">\n%s\n<span class="input-group-addon">%s</span></div>\n' % (
            super(RadarMeasurementInput, self).__call__(field, **kwargs),
            self.unit
        ))


class DeleteForm(Form):
    pass


class FacilityFormMixin(object):
    def __init__(self, obj=None, *args, **kwargs):
        super(FacilityFormMixin, self).__init__(obj=obj, *args, **kwargs)

        if obj is not None:
            facilities = obj.patient.intersect_internal_facilities(current_user, with_edit_patient_permission=True)
            facilities.sort(key=lambda x: x.name)
            self.facility_id.choices = [(x.id, x.name, x) for x in facilities]

    facility_id = RadarSelectObjectField('Data Source', validators=[InputRequired()], coerce=int)


def add_empty_choice(choices):
    choices.insert(0, ('', ''))
    return choices


def add_empty_object_choice(choices):
    choices.insert(0, ('', '', None))
    return choices


def radar_password_check(form, field):
    _ = form

    if not check_password_policy(field.data):
        raise ValidationError("Password doesn't meet the password policy.")
