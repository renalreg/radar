from collections import OrderedDict

from wtforms import FloatField, IntegerField
from wtforms.validators import Optional, InputRequired
from flask_wtf import Form
from wtforms.widgets import HiddenInput

from radar.lib.forms.core import RadarSelectMultipleField, RadarSelectField, RadarMeasurementInput, FacilityFormMixin, RadarDateField
from radar.lib.utils import optional_int


class LabResultTableForm(Form):
    test_item = RadarSelectMultipleField('Columns', validators=[Optional()])


class LabResultGraphForm(Form):
    test_item = RadarSelectField()


class SelectLabOrderForm(Form):
    lab_order_definition_id = RadarSelectField('Lab Order', validators=[InputRequired()], coerce=optional_int)


class AbstractLabOrderForm(FacilityFormMixin, Form):
    _result_fields = []

    lab_order_definition_id = IntegerField(widget=HiddenInput())
    date = RadarDateField(validators=[InputRequired()])

    @property
    def result_fields(self):
        return [getattr(self, x) for x in self._result_fields]


def lab_order_to_form(lab_order_definition):
    fields = OrderedDict()

    if lab_order_definition.pre_post:
        fields['pre_post'] = RadarSelectField('Pre / Post', choices=[('', ''), ('pre', 'Pre'), ('post', 'Post')], validators=[InputRequired()])

    result_fields = []

    for lab_result_definition in lab_order_definition.lab_result_definitions:
        if lab_result_definition.units is not None:
            widget = RadarMeasurementInput(lab_result_definition.units)
        else:
            widget = None

        field = FloatField(lab_result_definition.description, validators=[InputRequired()], widget=widget)
        field_name = lab_result_definition.code
        fields[field_name] = field
        result_fields.append(field_name)

    fields['_result_fields'] = result_fields

    form_class = type('LabOrderForm', (AbstractLabOrderForm,), fields)

    return form_class