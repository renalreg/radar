from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake import serializers
from cornflake.exceptions import SkipField
from cornflake.validators import none_if_blank, optional, max_length

from radar.serializers.common import (
    MetaMixin,
    TinyGroupSerializer,
    TinyGroupPatientSerializer,
    TinyUserSerializer
)
from radar.models.patients import Patient, GENDERS, ETHNICITIES
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION
from radar.serializers.patient_numbers import PatientNumberSerializer


class PatientSerializer(MetaMixin, ModelSerializer):
    first_name = fields.StringField(read_only=True)
    last_name = fields.StringField(read_only=True)
    date_of_birth = fields.DateField(read_only=True)
    year_of_birth = fields.IntegerField(read_only=True)
    date_of_death = fields.DateField(read_only=True)
    year_of_death = fields.IntegerField(read_only=True)
    gender = fields.IntegerLookupField(GENDERS, read_only=True)
    ethnicity = fields.StringLookupField(ETHNICITIES, read_only=True)
    groups = fields.ListField(child=GroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = fields.DateTimeField(read_only=True)
    recruited_group = TinyGroupSerializer(read_only=True)
    recruited_user = TinyUserSerializer(read_only=True)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    current = fields.BooleanField(read_only=True)
    primary_patient_number = PatientNumberSerializer(read_only=True)

    class Meta(object):
        model_class = Patient

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
    gender = fields.IntegerLookupField(GENDERS, read_only=True)
    ethnicity = fields.StringLookupField(ETHNICITIES, read_only=True)
    groups = fields.ListField(child=TinyGroupPatientSerializer(), source='group_patients', read_only=True)
    recruited_date = fields.DateTimeField(read_only=True)
    recruited_group = TinyGroupSerializer(read_only=True)
    recruited_user = TinyUserSerializer(read_only=True)
    comments = fields.StringField(read_only=True)
    current = fields.BooleanField(read_only=True)
    primary_patient_number = PatientNumberSerializer(read_only=True)

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

    @property
    def year_of_birth(self):
        if self.patient.date_of_birth is not None:
            return self.patient.date_of_birth.year
        else:
            return None

    @property
    def year_of_death(self):
        if self.patient.date_of_death is not None:
            return self.patient.date_of_death.year
        else:
            return None

    def __getattr__(self, item):
        return getattr(self.patient, item)
