from radar_api.serializers.cohort_patients import CohortPatientSerializer
from radar_api.serializers.cohorts import CohortReferenceField, TinyCohortReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisation_patients import OrganisationPatientSerializer
from radar_api.serializers.organisations import OrganisationReferenceField, TinyOrganisationReferenceField
from radar.patients import PatientProxy
from radar.serializers.core import Serializer
from radar.serializers.fields import StringField, BooleanField, IntegerField, \
    DateField, ListField, DateTimeField
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer, CodedIntegerSerializer
from radar.models.patients import Patient, GENDERS, ETHNICITIES


class TinyOrganisationPatientSerializer(Serializer):
    id = IntegerField()
    organisation = TinyOrganisationReferenceField()
    is_active = BooleanField()


class TinyCohortPatientSerializer(Serializer):
    id = IntegerField()
    cohort = TinyCohortReferenceField()
    is_active = BooleanField()


class TinyPatientSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name = StringField(read_only=True)
    last_name = StringField(read_only=True)
    date_of_birth = DateField(read_only=True)
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    gender = CodedIntegerSerializer(GENDERS, read_only=True)
    ethnicity = CodedStringSerializer(ETHNICITIES, read_only=True)
    organisations = ListField(field=TinyOrganisationPatientSerializer(), source='organisation_patients', read_only=True)
    cohorts = ListField(field=TinyCohortPatientSerializer(), source='cohort_patients', read_only=True)
    recruited_organisation = TinyOrganisationReferenceField(read_only=True)
    is_active = BooleanField()
    comments = StringField()
    recruited_date = DateTimeField(read_only=True)

    def __init__(self, current_user, **kwargs):
        super(TinyPatientSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientProxy(value, self.current_user)
        return super(TinyPatientSerializer, self).to_data(value)


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField(read_only=True)
    last_name = StringField(read_only=True)
    date_of_birth = DateField(read_only=True)
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    gender = CodedIntegerSerializer(GENDERS, read_only=True)
    ethnicity = CodedStringSerializer(ETHNICITIES, read_only=True)
    organisations = ListField(field=OrganisationPatientSerializer(), source='organisation_patients', read_only=True)
    cohorts = ListField(field=CohortPatientSerializer(), source='cohort_patients', read_only=True)
    recruited_organisation = OrganisationReferenceField(read_only=True)
    is_active = BooleanField()
    comments = StringField()
    recruited_date = DateTimeField(read_only=True)

    class Meta(object):
        model_class = Patient
        fields = ['id', 'created_date', 'modified_date']

    def __init__(self, current_user, **kwargs):
        super(PatientSerializer, self).__init__(**kwargs)
        self.current_user = current_user

    def to_data(self, value):
        value = PatientProxy(value, self.current_user)
        return super(PatientSerializer, self).to_data(value)


class PatientListRequestSerializer(Serializer):
    id = IntegerField()
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField()
    date_of_death = DateField()
    year_of_death = IntegerField()
    gender = StringField()
    patient_number = StringField()
    organisation = OrganisationReferenceField()
    cohort = CohortReferenceField()
    is_active = BooleanField()
