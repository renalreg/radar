from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.exceptions import ValidationError, SkipField
from cornflake.validators import (
    not_empty,
    upper,
    normalise_whitespace,
    max_length,
    not_in_future,
    none_if_blank,
    optional,
    lower,
    email_address
)

from radar.api.serializers.common import (
    PatientMixin,
    SystemSourceMixin,
    MetaMixin,
    StringLookupField,
    IntegerLookupField
)
from radar.api.serializers.validators import after_day_zero
from radar.models.patient_codes import ETHNICITIES, GENDERS
from radar.models.patient_demographics import PatientDemographics
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION


class PatientDemographicsSerializer(PatientMixin, SystemSourceMixin, MetaMixin, ModelSerializer):
    first_name = fields.StringField(validators=[not_empty(), upper(), normalise_whitespace(), max_length(100)])
    last_name = fields.StringField(validators=[not_empty(), upper(), normalise_whitespace(), max_length(100)])
    date_of_birth = fields.DateField(validators=[after_day_zero(), not_in_future()])
    year_of_birth = fields.IntegerField(read_only=True)
    date_of_death = fields.DateField(required=False, validators=[after_day_zero(), not_in_future()])
    year_of_death = fields.IntegerField(read_only=True)
    gender = IntegerLookupField(GENDERS)
    ethnicity = StringLookupField(ETHNICITIES, required=False)
    home_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), normalise_whitespace(), max_length(30)])
    work_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), normalise_whitespace(), max_length(30)])
    mobile_number = fields.StringField(required=False, validators=[none_if_blank(), optional(), normalise_whitespace(), max_length(30)])
    email_address = fields.StringField(required=False, validators=[none_if_blank(), optional(), lower(), email_address()])

    class Meta(object):
        model_class = PatientDemographics

    def to_representation(self, value):
        user = self.context['user']
        value = PatientDemographicsProxy(value, user)
        value = super(PatientDemographicsSerializer, self).to_representation(value)
        return value

    def validate(self, data):
        data = super(PatientDemographicsSerializer, self).validate(data)

        if data['date_of_death'] is not None and data['date_of_death'] < data['date_of_birth']:
            raise ValidationError({'date_of_death': 'Must be after date of birth.'})

        return data


class PatientDemographicsProxy(object):
    def __init__(self, demographics, user):
        self.demographics = demographics
        self.user = user
        self.demographics_permission = has_permission_for_patient(user, demographics.patient, PERMISSION.VIEW_DEMOGRAPHICS)

    @property
    def first_name(self):
        if self.demographics_permission:
            return self.demographics.first_name
        else:
            raise SkipField

    @property
    def last_name(self):
        if self.demographics_permission:
            return self.demographics.last_name
        else:
            raise SkipField

    @property
    def date_of_birth(self):
        if self.demographics_permission:
            return self.demographics.date_of_birth
        else:
            raise SkipField

    @property
    def year_of_birth(self):
        return self.demographics.date_of_birth.year

    @property
    def date_of_death(self):
        if self.demographics_permission:
            return self.demographics.date_of_death
        else:
            raise SkipField

    @property
    def year_of_death(self):
        if self.demographics.date_of_death is not None:
            return self.demographics.date_of_death.year
        else:
            return None

    @property
    def home_number(self):
        if self.demographics_permission:
            return self.demographics.home_number
        else:
            raise SkipField

    @property
    def work_number(self):
        if self.demographics_permission:
            return self.demographics.work_number
        else:
            raise SkipField

    @property
    def mobile_number(self):
        if self.demographics_permission:
            return self.demographics.mobile_number
        else:
            raise SkipField

    @property
    def email_address(self):
        if self.demographics_permission:
            return self.demographics.email_address
        else:
            raise SkipField

    def __getattr__(self, item):
        return getattr(self.demographics, item)
