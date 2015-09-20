from radar.api.serializers.cohort_patients import CohortPatientSerializer
from radar.api.serializers.cohorts import CohortReferenceField
from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisation_patients import OrganisationPatientSerializer
from radar.api.serializers.organisations import OrganisationReferenceField
from radar.api.serializers.patient_demographics import EthnicityCodeReferenceField
from radar.lib.patient_demographics import PatientDemographicsProxy
from radar.lib.patients import PatientProxy
from radar.lib.serializers.core import Serializer
from radar.lib.serializers.fields import StringField, BooleanField, IntegerField, DateField, ListField
from radar.lib.serializers.models import ModelSerializer
from radar.lib.serializers.codes import CodedStringSerializer
from radar.lib.models import Patient, GENDERS


class PatientSerializer(MetaSerializerMixin, ModelSerializer):
    first_name = StringField(read_only=True)
    last_name = StringField(read_only=True)
    date_of_birth = DateField(read_only=True)
    year_of_birth = IntegerField(read_only=True)
    date_of_death = DateField(read_only=True)
    year_of_death = IntegerField(read_only=True)
    gender = CodedStringSerializer(GENDERS, read_only=True)
    ethnicity_code = EthnicityCodeReferenceField(read_only=True)
    organisations = ListField(field=OrganisationPatientSerializer(), source='organisation_patients', read_only=True)
    cohorts = ListField(field=CohortPatientSerializer(), source='cohort_patients', read_only=True)
    recruiting_organisation = OrganisationReferenceField(read_only=True)
    is_active = BooleanField()
    comments = StringField()

    class Meta(object):
        model_class = Patient
        fields = ['id']

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
