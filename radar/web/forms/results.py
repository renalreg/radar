from flask import request
from wtforms import FloatField, IntegerField
from wtforms.validators import Optional, InputRequired
from flask_wtf import Form
from wtforms.widgets import HiddenInput

from radar.lib.database import db
from radar.models import Result
from radar.web.forms.core import RadarSelectMultipleField, RadarSelectField, RadarMeasurementInput, FacilityFormMixin, RadarDateField
from radar.lib.utils import optional_int


class ResultTableForm(Form):
    result_codes = RadarSelectMultipleField('Columns', validators=[Optional()])


class ResultGraphForm(Form):
    result_code = RadarSelectField()


class SelectAddResultGroupForm(Form):
    result_group_definition_id = RadarSelectField('Result Group', validators=[InputRequired()], coerce=optional_int)


class SelectResultGroupForm(Form):
    result_group_definition_id = RadarSelectField('Result Group', validators=[Optional()], coerce=optional_int)


def result_group_to_form(result_group_definition):
    class ResultGroupForm(FacilityFormMixin, Form):
        def __init__(self, *args, **kwargs):
            super(ResultGroupForm, self).__init__(*args, **kwargs)
            self.no_results_entered = False

        _result_fields = []

        result_group_definition_id = IntegerField(widget=HiddenInput())
        date = RadarDateField(validators=[InputRequired()])

        def is_submitted(self):
            return super(ResultGroupForm, self).is_submitted() and 'result_group_form' in request.form

        @property
        def result_fields(self):
            return [getattr(self, x) for x in self._result_fields]

        def validate(self):
            if not super(ResultGroupForm, self).validate():
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

            for x in obj.results:
                db.session.delete(x)

            obj.results = []

            for i, result_definition in enumerate(obj.result_group_definition.result_definitions):
                field_name = 'result%d' % i
                value = getattr(self, field_name).data

                if value is not None:
                    result = Result(
                        result_group=obj,
                        result_definition=result_definition,
                        value=value
                    )
                    obj.results.append(result)

    if result_group_definition.pre_post:
        ResultGroupForm.pre_post = RadarSelectField('Pre / Post', choices=[('', ''), ('pre', 'Pre'), ('post', 'Post')], validators=[InputRequired()])

    for i, result_definition in enumerate(result_group_definition.result_definitions):
        if result_definition.units is not None:
            widget = RadarMeasurementInput(result_definition.units)
        else:
            widget = None

        field = FloatField(result_definition.name, validators=[Optional()], widget=widget)
        field_name = 'result%d' % i

        setattr(ResultGroupForm, field_name, field)
        ResultGroupForm._result_fields.append(field_name)

    return ResultGroupForm


def result_group_to_form_data(result_group):
    data = dict()

    code_to_field_name = dict()

    for i, result_definition in enumerate(result_group.result_group_definition.result_definitions):
        code_to_field_name[result_definition.code] = 'result%d' % i

    for result in result_group.results:
        # Might not exist if definition has changed
        field_name = code_to_field_name.get(result.result_definition.code)

        if field_name is None:
            continue

        data[field_name] = result.value

    return data
