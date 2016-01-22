from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.serializers.models import ModelSerializer
from radar.serializers.fields import LabelledStringField
from radar.models.pregnancies import Pregnancy, OUTCOMES, DELIVERY_METHODS, PRE_ECLAMPSIA_TYPES


class PregnancySerializer(PatientSerializerMixin, MetaSerializerMixin, ModelSerializer):
    outcome = LabelledStringField(OUTCOMES)
    delivery_method = LabelledStringField(DELIVERY_METHODS)
    pre_eclampsia = LabelledStringField(PRE_ECLAMPSIA_TYPES)

    class Meta(object):
        model_class = Pregnancy
