from radar.api.serializers.meta import MetaSerializerMixin
from radar.api.serializers.organisation_consultants import ConsultantReferenceField
from radar.api.serializers.patient_mixins import PatientSerializerMixin
from radar.lib.models import PatientConsultant
from radar.lib.serializers.models import ModelSerializer


class PatientConsultantSerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    consultant = ConsultantReferenceField()

    class Meta(object):
        model_class = PatientConsultant
        exclude = ['consultant_id']
