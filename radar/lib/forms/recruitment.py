from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import Optional, InputRequired

from radar.lib.forms.core import RadarDOBField, RadarSelectField, RadarNHSNoField, RadarCHINoField
from radar.lib.utils import optional_int


class RecruitPatientSearchForm(Form):
    date_of_birth = RadarDOBField(validators=[InputRequired()])
    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[InputRequired()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[InputRequired()])
    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[Optional()])
    nhs_no = RadarNHSNoField(validators=[Optional()])
    chi_no = RadarCHINoField(validators=[Optional()])

    def validate(self):
        if not super(RecruitPatientSearchForm, self).validate():
            return False

        valid = True

        if not ((self.first_name.data and self.last_name.data) or self.nhs_no.data or self.chi_no.data):
            self.first_name.errors.append('Please supply a first name and last name, NHS number or CHI number.')
            valid = False

        return valid


class RecruitPatientRadarForm(Form):
    patient_id = IntegerField(validators=[Optional()])


class RecruitPatientRDCForm(Form):
    mpiid = IntegerField(validators=[Optional()])