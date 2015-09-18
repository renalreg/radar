from radar.api.serializers.cohort_patients import CohortPatientSerializer
from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisation_patients import OrganisationPatientSerializer
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.api.serializers.patient_demographics import EthnicityCodeReferenceField
from radar.lib.serializers import ModelSerializer, ListField, StringField, DateField, IntegerField, \
    Serializer, BooleanField, CodedStringSerializer
from radar.lib.models import Patient, GENDERS


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField()
    year_of_death = IntegerField(read_only=True)
    gender = CodedStringSerializer(GENDERS)
    ethnicity_code = EthnicityCodeReferenceField()
    organisations = ListField(field=OrganisationPatientSerializer(), source='organisation_patients')
    cohorts = ListField(field=CohortPatientSerializer(), source='cohort_patients')

    class Meta(object):
        model_class = Patient
        fields = ['id']


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
    organisation_id = OrganisationReferenceField(write_only=True)
    cohort_id = CohortReferenceField(write_only=True)
    is_active = BooleanField()
