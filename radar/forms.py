from datetime import date
from markupsafe import Markup
import re
from wtforms import SelectField, SelectMultipleField, ValidationError, StringField, IntegerField, Field, DateField, \
    RadioField
from wtforms.widgets import TextInput, Select, HTMLString, html_params
from flask_wtf import Form


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

        for value, label in [('y', 'Yes'), ('n', 'No')]:
            html_attributes['checked'] = field._value() == value
            html_attributes['value'] = value
            input_tag = '<input type="radio" {} />\n'.format(html_params(**html_attributes))
            html.append('<label class="radio-inline">%s %s</label>' % (input_tag, label))

        return HTMLString("\n".join(html))


class RadarInlineRadioField(RadioField):
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


def validate_postcode(value):
    regex = re.compile("GIR[ ]?0AA|((AB|AL|B|BA|BB|BD|BH|BL|BN|BR|BS|BT|BX|CA|CB|CF|CH|CM|CO|CR|CT|CV|CW|DA|DD|DE|DG|DH|DL|DN|DT|DY|E|EC|EH|EN|EX|FK|FY|G|GL|GY|GU|HA|HD|HG|HP|HR|HS|HU|HX|IG|IM|IP|IV|JE|KA|KT|KW|KY|L|LA|LD|LE|LL|LN|LS|LU|M|ME|MK|ML|N|NE|NG|NN|NP|NR|NW|OL|OX|PA|PE|PH|PL|PO|PR|RG|RH|RM|S|SA|SE|SG|SK|SL|SM|SN|SO|SP|SR|SS|ST|SW|SY|TA|TD|TF|TN|TQ|TR|TS|TW|UB|W|WA|WC|WD|WF|WN|WR|WS|WV|YO|ZE)(\\d[\\dA-Z]?[ ]?\\d[ABD-HJLN-UW-Z]{2}))|BFPO[ ]?\\d{1,4}")
    return bool(regex.match(value))


def validate_nhs_no(value):
    if not isinstance(value, basestring):
        value = str(value)

    if len(value) != 10:
        return False

    if not value.isdigit():
        return False

    check_digit = 0

    for i in range(0, 9):
        check_digit += int(value[i]) * (10 - i)

    check_digit = 11 - (check_digit % 11)

    if check_digit == 11:
        check_digit = 0

    if check_digit != int(value[9]):
        return False

    return True


def add_empty_choice(choices):
    choices.insert(0, ('', ''))
    return choices