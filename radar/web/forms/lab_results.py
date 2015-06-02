from collections import OrderedDict

from wtforms import FloatField, IntegerField
from wtforms.validators import Optional, InputRequired
from flask_wtf import Form
from wtforms.widgets import HiddenInput

from radar.web.forms.core import RadarSelectMultipleField, RadarSelectField, RadarMeasurementInput, FacilityFormMixin, RadarDateField
from radar.lib.utils import optional_int


class LabResultTableForm(Form):
    result_codes = RadarSelectMultipleField('Columns', validators=[Optional()])


class LabResultGraphForm(Form):
    result_code = RadarSelectField()


class SelectLabGroupForm(Form):
    lab_group_definition_id = RadarSelectField('Lab Group', validators=[InputRequired()], coerce=optional_int)


def lab_group_to_form(lab_group_definition=None):
    class LabGroupForm(FacilityFormMixin, Form):
        def __init__(self, *args, **kwargs):
            super(LabGroupForm, self).__init__(*args, **kwargs)
            self.no_results_entered = False

        _result_fields = []

        lab_group_definition_id = IntegerField(widget=HiddenInput())
        date = RadarDateField(validators=[InputRequired()])

        @property
        def result_fields(self):
            return [getattr(self, x) for x in self._result_fields]

        def validate(self):
            if not super(LabGroupForm, self).validate():
                return False

            valid = True
            results_entered = False

            for field in self.result_fields:
                if field.data is not None:
                    results_entered = True
                    break

            if not results_entered:
                self.no_results_entered = True
                valid = False

            return valid

    if lab_group_definition.pre_post:
        LabGroupForm.pre_post = RadarSelectField('Pre / Post', choices=[('', ''), ('pre', 'Pre'), ('post', 'Post')], validators=[InputRequired()])

    for lab_result_definition in lab_group_definition.lab_result_definitions:
        if lab_result_definition.units is not None:
            widget = RadarMeasurementInput(lab_result_definition.units)
        else:
            widget = None

        field = FloatField(lab_result_definition.name, validators=[Optional()], widget=widget)
        field_name = lab_result_definition.code

        setattr(LabGroupForm, field_name, field)
        LabGroupForm._result_fields.append(field_name)

    return LabGroupForm


def lab_group_to_form_data(lab_group):
    data = dict()

    for lab_result in lab_group.lab_results:
        data[lab_result.lab_result_definition.code] = lab_result.value

    return data