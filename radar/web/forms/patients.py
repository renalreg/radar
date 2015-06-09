from flask_login import current_user
from wtforms import IntegerField, BooleanField
from wtforms.validators import Optional, InputRequired
from flask_wtf import Form

from radar.lib.database import db
from radar.models import EthnicityCode
from radar.web.forms.core import RadarDateField, RadarSelectField, RadarCHINoField, RadarNHSNoField, RadarDOBField, \
    RadarSelectObjectField, RadarPostcodeField, add_empty_object_choice, RadarStringField
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


class PatientDemographicsForm(Form):
    def __init__(self, *args, **kwargs):
        super(PatientDemographicsForm, self).__init__(*args, **kwargs)

        self.ethnicity_code_id.choices = add_empty_object_choice(EthnicityCode.choices(db.session))

    first_name = RadarStringField(validators=[InputRequired()])
    last_name = RadarStringField(validators=[InputRequired()])
    date_of_birth = RadarDOBField(validators=[InputRequired()])
    date_of_death = RadarDateField('Date of Death', validators=[Optional()])
    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[InputRequired()])
    ethnicity_code_id = RadarSelectObjectField('Ethnicity', validators=[InputRequired()])

    home_number = RadarStringField(validators=[Optional()])
    work_number = RadarStringField(validators=[Optional()])
    mobile_number = RadarStringField(validators=[Optional()])
    email_address = RadarStringField(validators=[Optional()])

    nhs_no = RadarNHSNoField(validators=[Optional()])
    chi_no = RadarCHINoField(validators=[Optional()])

    def populate_obj(self, obj):
        obj.first_name = self.first_name.data
        obj.last_name = self.last_name.data
        obj.date_of_birth = self.date_of_birth.data
        obj.date_of_death = self.date_of_death.data
        obj.gender = self.gender.data
        obj.ethnicity_code = self.ethnicity_code_id.obj
        obj.home_number = self.home_number.data
        obj.work_number = self.work_number.data
        obj.mobile_number = self.mobile_number.data
        obj.email_address = self.email_address.data
        obj.nhs_no = self.nhs_no.data
        obj.chi_no = self.chi_no.data


class PatientSearchForm(Form):
    def __init__(self, user, *args, **kwargs):
        super(PatientSearchForm, self).__init__(*args, **kwargs)

        self.disease_group_id.choices = get_disease_group_filter_choices(user)
        self.unit_id.choices = get_unit_filter_choices(user)

    radar_id = IntegerField('RaDaR ID', validators=[Optional()])

    first_name = RadarStringField(validators=[Optional()])
    last_name = RadarStringField(validators=[Optional()])
    gender = RadarSelectField(choices=[('', ''), ('M', 'Male'), ('F', 'Female')], validators=[Optional()])

    patient_number = RadarStringField(validators=[Optional()])

    unit_id = RadarSelectField('Unit', coerce=optional_int, validators=[Optional()])
    disease_group_id = RadarSelectField('Disease Group', coerce=optional_int, validators=[Optional()])

    date_of_birth = RadarDateField('Date of Birth', validators=[Optional()])
    year_of_birth = IntegerField('Year of Birth', validators=[Optional()])
    date_of_death = RadarDateField('Date of Death', validators=[Optional()])
    year_of_death = IntegerField('Year of Death', validators=[Optional()])

    include_inactive = BooleanField('Include Inactive', default=False, validators=[Optional()])

    order_by = RadarSelectField(choices=ORDER_BY_CHOICES, validators=[Optional()], default='radar_id')
    order_direction = RadarSelectField(choices=[(ASCENDING, 'Ascending'), (DESCENDING, 'Descending')], default=ASCENDING, validators=[Optional()])

    per_page = RadarSelectField(coerce=int, default=PER_PAGE_DEFAULT, choices=PER_PAGE_CHOICES, validators=[Optional()])


class PatientUnitForm(Form):
    unit_id = RadarSelectField('Unit', validators=[InputRequired()], coerce=int)


class AddPatientDiseaseGroupForm(Form):
    disease_group_id = RadarSelectField('Disease Group', validators=[InputRequired()], coerce=int)


class EditPatientDiseaseGroupForm(Form):
    is_active = BooleanField('Active')


class PatientNumberForm(Form):
    def __init__(self, obj=None, *args, **kwargs):
        super(PatientNumberForm, self).__init__(obj=obj, *args, **kwargs)

        if obj is not None:
            facilities = obj.patient.intersect_internal_facilities(current_user, with_edit_patient_permission=True)
            facilities.sort(key=lambda x: x.name)
            self.number_facility_id.choices = [(x.id, x.name, x) for x in facilities]

    number_facility_id = RadarSelectObjectField('Organisation', validators=[InputRequired()], coerce=int)
    number = RadarStringField(validators=[InputRequired()])

    def populate_obj(self, obj):
        obj.number_facility = self.number_facility_id.obj
        obj.number = self.number.data


class PatientAliasForm(Form):
    first_name = RadarStringField(validators=[InputRequired()])
    last_name = RadarStringField(validators=[InputRequired()])


class PatientAddressForm(Form):
    from_date = RadarDateField(validators=[Optional()])
    to_date = RadarDateField(validators=[Optional()])
    address_line_1 = RadarStringField(validators=[InputRequired()])
    address_line_2 = RadarStringField(validators=[Optional()])
    address_line_3 = RadarStringField(validators=[Optional()])
    postcode = RadarPostcodeField(validators=[InputRequired()])


class PatientActiveForm(Form):
    is_active = BooleanField('Active')
