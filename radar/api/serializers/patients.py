from cornflake import fields, serializers
from cornflake.exceptions import SkipField, ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import (
    IntegerLookupField,
    MetaMixin,
    StringLookupField,
    TinyGroupPatientSerializer,
    TinyGroupSerializer,
    TinyUserSerializer,
)
from radar.api.serializers.group_patients import GroupPatientSerializer
from radar.api.serializers.nationalities import NationalityField
from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.models.patient_codes import ETHNICITIES, GENDERS
from radar.models.patients import Patient
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION


class RecruitedDateField(fields.DateField):
    def get_attribute(self, patient):
        return patient.recruited_date()


class RecruitedGroupField(TinyGroupSerializer):
    def get_attribute(self, patient):
        return patient.recruited_group()


class RecruitedUserField(TinyUserSerializer):
    def get_attribute(self, patient):
        return patient.recruited_user()


class CurrentField(fields.BooleanField):
    def get_attribute(self, patient):
        return patient.current()


class PatientSerializer(MetaMixin, ModelSerializer):
    first_name = fields.StringField(read_only=True)
    last_name = fields.StringField(read_only=True)
    date_of_birth = fields.DateField(read_only=True)
    year_of_birth = fields.IntegerField(read_only=True)
    date_of_death = fields.DateField(read_only=True)
    year_of_death = fields.IntegerField(read_only=True)
    gender = IntegerLookupField(GENDERS, read_only=True)
    nationality = NationalityField()
    ethnicity = StringLookupField(ETHNICITIES, read_only=True)
    groups = fields.ListField(child=GroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = RecruitedDateField(read_only=True)
    recruited_group = RecruitedGroupField(read_only=True)
    recruited_user = RecruitedUserField(read_only=True)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    current = CurrentField(read_only=True)
    primary_patient_number = PatientNumberSerializer(read_only=True)
    test = fields.BooleanField(default=False)
    frozen = fields.BooleanField(read_only=True)
    ukrdc = fields.BooleanField(read_only=True)

    class Meta(object):
        model_class = Patient

    def validate_test(self, value):
        instance = self.root.instance
        user = self.context['user']

        # Must be an admin to change the test flag
        if (
            (
                (instance is None and value) or
                (instance is not None and instance.test != value)
            ) and
            not user.is_admin
        ):
            raise ValidationError('Must be an admin!')

        return value

    def to_representation(self, value):
        user = self.context['user']
        value = PatientProxy(value, user)
        value = super(PatientSerializer, self).to_representation(value)
        return value


class TinyPatientSerializer(serializers.Serializer):
    id = fields.IntegerField(read_only=True)
    first_name = fields.StringField(read_only=True)
    last_name = fields.StringField(read_only=True)
    date_of_birth = fields.DateField(read_only=True)
    year_of_birth = fields.IntegerField(read_only=True)
    date_of_death = fields.DateField(read_only=True)
    year_of_death = fields.IntegerField(read_only=True)
    gender = IntegerLookupField(GENDERS, read_only=True)
    nationality = NationalityField()
    ethnicity = StringLookupField(ETHNICITIES, read_only=True)
    groups = fields.ListField(child=TinyGroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = RecruitedDateField(read_only=True)
    recruited_group = RecruitedGroupField(read_only=True)
    recruited_user = RecruitedUserField(read_only=True)
    comments = fields.StringField(read_only=True)
    current = fields.BooleanField(read_only=True)
    primary_patient_number = PatientNumberSerializer(read_only=True)
    test = fields.BooleanField(default=False)
    frozen = fields.BooleanField(read_only=True)
    ukrdc = fields.BooleanField(read_only=True)

    def to_representation(self, value):
        user = self.context['user']
        value = PatientProxy(value, user)
        value = super(TinyPatientSerializer, self).to_representation(value)
        return value


class PatientProxy(object):
    def __init__(self, patient, user):
        self.patient = patient
        self.user = user
        self.demographics_permission = has_permission_for_patient(user, patient, PERMISSION.VIEW_DEMOGRAPHICS)

    @property
    def first_name(self):
        if self.demographics_permission:
            return self.patient.first_name
        else:
            raise SkipField

    @property
    def last_name(self):
        if self.demographics_permission:
            return self.patient.last_name
        else:
            raise SkipField

    @property
    def date_of_birth(self):
        if self.demographics_permission:
            return self.patient.date_of_birth
        else:
            raise SkipField

    @property
    def primary_patient_number(self):
        if self.demographics_permission:
            return self.patient.primary_patient_number
        else:
            raise SkipField

    def __getattr__(self, item):
        return getattr(self.patient, item)
