from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Optional, InputRequired, Email, DataRequired
from flask_wtf import Form

from radar.forms import RadarDateField, RadarSelectField, RadarCHINoField, RadarNHSNoField, RadarPostcodeField, \
    RadarDOBField
from radar.ordering import ASCENDING, DESCENDING
from radar.utils import optional_int


PER_PAGE_CHOICES = [(10, '10'), (25, '25'), (50, '50'), (100, '100'), (-1, 'All')]
PER_PAGE_DEFAULT = 50

ORDER_BY_CHOICES = [
    ('radar_id', 'RaDaR ID'),
    ('first_name', 'First Name'),
    ('last_name', 'Last Name'),
    ('date_of_birth', 'Date of Birth'),
    ('gender', 'Gender'),
]


class DemographicsForm(Form):
    first_name = StringField(validators=[InputRequired()])
    last_name = StringField(validators=[InputRequired()])

    # TODO validation
    date_of_birth = RadarDOBField(validators=[InputRequired()])

    # TODO validation
    date_of_death = RadarDateField('Date of Death', validators=[Optional()])

    gender = RadarSelectField(choices=[('', ''), (1, 'Male'), (2, 'Female')], coerce=optional_int, validators=[InputRequired()])

    # TODO
    ethnicity = StringField(validators=[InputRequired()])

    alias_first_name = StringField(validators=[Optional()])
    alias_last_name = StringField(validators=[Optional()])

    address_line_1 = StringField(validators=[Optional()])
    address_line_2 = StringField(validators=[Optional()])
    address_line_3 = StringField(validators=[Optional()])

    postcode = RadarPostcodeField(validators=[InputRequired()])

    home_number = StringField(validators=[Optional()])
    work_number = StringField(validators=[Optional()])
    mobile_number = StringField(validators=[Optional()])
    email_address = StringField(validators=[Optional(), Email()])

    nhs_no = RadarNHSNoField(validators=[Optional()])
    chi_no = RadarCHINoField(validators=[Optional()])


class PatientSearchForm(Form):
    radar_id = IntegerField('RaDaR ID', validators=[Optional()])

    first_name = StringField()
    last_name = StringField()
    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[Optional()])

    patient_number = StringField()

    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[Optional()])

    date_of_birth = RadarDateField('Date of Birth', validators=[Optional()])
    year_of_birth = IntegerField('Year of Birth', validators=[Optional()])
    date_of_death = RadarDateField('Date of Death', validators=[Optional()])
    year_of_death = IntegerField('Year of Death', validators=[Optional()])

    is_active = BooleanField('Active', default=True, validators=[Optional()])

    order_by = RadarSelectField(choices=ORDER_BY_CHOICES)
    order_direction = RadarSelectField(choices=[(ASCENDING, 'Ascending'), (DESCENDING, 'Descending')], default=ASCENDING)

    per_page = RadarSelectField(coerce=int, default=PER_PAGE_DEFAULT, choices=PER_PAGE_CHOICES)
    page = IntegerField()


class RecruitPatientSearchForm(Form):
    date_of_birth = RadarDOBField(validators=[DataRequired()])
    unit_id = RadarSelectField('Unit', coerce=optional_int)
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int)
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


class RecruitPatientRdcForm(Form):
    mpiid = IntegerField(validators=[Optional()])


class PatientUnitForm(Form):
    unit_id = RadarSelectField('Unit', validators=[InputRequired()], coerce=int)


class AddPatientDiseaseGroupForm(Form):
    disease_group_id = RadarSelectField('Disease Group', validators=[InputRequired()], coerce=int)


class EditPatientDiseaseGroupForm(Form):
    is_active = BooleanField('Active')