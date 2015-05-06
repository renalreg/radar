from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Optional, InputRequired, Email
from flask_wtf import Form

from radar.forms import RadarDateField, RadarSelectField, RadarCHINoField, RadarNHSNoField, RadarPostcodeField

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
    date_of_birth = RadarDateField('Date of Birth')

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
    first_name = StringField()
    last_name = StringField()
    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[Optional()])
    date_of_birth = RadarDateField('Date of Birth', validators=[Optional()])
    patient_number = StringField()
    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[Optional()])
    radar_id = IntegerField('RaDaR ID', validators=[Optional()])
    year_of_birth = IntegerField('Year of Birth', validators=[Optional()])
    order_by = RadarSelectField(choices=ORDER_BY_CHOICES)
    order_direction = RadarSelectField(choices=[(ASCENDING, 'Ascending'), (DESCENDING, 'Descending')], default=ASCENDING)
    per_page = RadarSelectField(coerce=int, default=50, choices=PER_PAGE_CHOICES)
    page = IntegerField()