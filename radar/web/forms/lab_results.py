from collections import OrderedDict

from wtforms import FloatField, IntegerField
from wtforms.validators import Optional, InputRequired
from flask_wtf import Form
from wtforms.widgets import HiddenInput
from radar.lib.database import db
from radar.models import LabResult

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

        def populate_obj(self, obj):
            obj.facility = self.facility_id.obj
            obj.date = self.date.data

            if hasattr(self, 'pre_post'):
                obj.pre_post = self.pre_post.data

            for x in obj.lab_results:
                db.session.delete(x)

            obj.lab_results = []

            for i, lab_result_definition in enumerate(obj.lab_group_definition.lab_result_definitions):
                field_name = 'result%d' % i
                value = getattr(self, field_name).data

                if value is not None:
                    lab_result = LabResult(
                        lab_group=obj,
                        lab_result_definition=lab_result_definition,
                        value=value
                    )
                    obj.lab_results.append(lab_result)

    if lab_group_definition.pre_post:
        LabGroupForm.pre_post = RadarSelectField('Pre / Post', choices=[('', ''), ('pre', 'Pre'), ('post', 'Post')], validators=[InputRequired()])

    for i, lab_result_definition in enumerate(lab_group_definition.lab_result_definitions):
        if lab_result_definition.units is not None:
            widget = RadarMeasurementInput(lab_result_definition.units)
        else:
            widget = None

        field = FloatField(lab_result_definition.name, validators=[Optional()], widget=widget)
        field_name = 'result%d' % i

        setattr(LabGroupForm, field_name, field)
        LabGroupForm._result_fields.append(field_name)

    return LabGroupForm


def lab_group_to_form_data(lab_group):
    data = dict()

    code_to_field_name = dict()

    for i, lab_result_definition in enumerate(lab_group.lab_group_definition.lab_result_definitions):
        code_to_field_name[lab_result_definition.code] = 'result%d' % i

    for lab_result in lab_group.lab_results:
        # Might not exist if definition has changed
        field_name = code_to_field_name.get(lab_result.lab_result_definition.code)

        if field_name is None:
            continue

        data[field_name] = lab_result.value

    return data