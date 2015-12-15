from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedStringSerializer
from radar.models.pregnancies import Pregnancy, OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES


class PregnancySerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    outcome = CodedStringSerializer(OUTCOMES)
    delivery_method = CodedStringSerializer(DELIVERY_METHODS)
    pre_eclampsia = CodedStringSerializer(PRE_ECLAMPSIA_TYPES)

    class Meta(object):
        model_class = Pregnancy
