from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import Optional, InputRequired, Email
from flask_wtf import Form

from radar.web.forms.core import RadarDateField, RadarSelectField, RadarCHINoField, RadarNHSNoField, RadarDOBField
from radar.lib.ordering import ASCENDING, DESCENDING
from radar.lib.patient_search import get_disease_group_filter_choices, get_unit_filter_choices
from radar.lib.utils import optional_int


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

    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[InputRequired()])

    # TODO
    ethnicity = StringField(validators=[InputRequired()])

    #alias_first_name = StringField(validators=[Optional()])
    #alias_last_name = StringField(validators=[Optional()])

    #address_line_1 = StringField(validators=[Optional()])
    #address_line_2 = StringField(validators=[Optional()])
    #address_line_3 = StringField(validators=[Optional()])
    #postcode = RadarPostcodeField(validators=[InputRequired()])

    home_number = StringField(validators=[Optional()])
    work_number = StringField(validators=[Optional()])
    mobile_number = StringField(validators=[Optional()])
    email_address = StringField(validators=[Optional(), Email()])

    nhs_no = RadarNHSNoField(validators=[Optional()])
    chi_no = RadarCHINoField(validators=[Optional()])


class PatientSearchForm(Form):
    def __init__(self, user, *args, **kwargs):
        super(PatientSearchForm, self).__init__(*args, **kwargs)

        self.disease_group_id.choices = get_disease_group_filter_choices(user)
        self.unit_id.choices = get_unit_filter_choices(user)

    radar_id = IntegerField('RaDaR ID', validators=[Optional()])

    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[Optional()])
    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[Optional()])

    patient_number = StringField(validators=[Optional()])

    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[Optional()])

    date_of_birth = RadarDateField('Date of Birth', validators=[Optional()])
    year_of_birth = IntegerField('Year of Birth', validators=[Optional()])
    date_of_death = RadarDateField('Date of Death', validators=[Optional()])
    year_of_death = IntegerField('Year of Death', validators=[Optional()])

    include_inactive = BooleanField('Include Inactive', default=False, validators=[Optional()])

    order_by = RadarSelectField(choices=ORDER_BY_CHOICES, validators=[Optional()])
    order_direction = RadarSelectField(choices=[(ASCENDING, 'Ascending'), (DESCENDING, 'Descending')], default=ASCENDING, validators=[Optional()])

    per_page = RadarSelectField(coerce=int, default=PER_PAGE_DEFAULT, choices=PER_PAGE_CHOICES, validators=[Optional()])


class PatientUnitForm(Form):
    unit_id = RadarSelectField('Unit', validators=[InputRequired()], coerce=int)


class AddPatientDiseaseGroupForm(Form):
    disease_group_id = RadarSelectField('Disease Group', validators=[InputRequired()], coerce=int)


class EditPatientDiseaseGroupForm(Form):
    is_active = BooleanField('Active')