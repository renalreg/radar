from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.organisation_consultants import ConsultantReferenceField
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models import PatientConsultant
from radar.serializers.models import ModelSerializer


class PatientConsultantSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    consultant = ConsultantReferenceField()

    class Meta(object):
        model_class = PatientConsultant
        exclude = ['consultant_id']
