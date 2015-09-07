from radar.lib.serializers import LookupField, ModelSerializer, MetaSerializerMixin, PatientSerializerMixin, \
    FacilitySerializerMixin, FacilityLookupField
from radar.models import DialysisType, Dialysis


class DialysisTypeLookupField(LookupField):
    model_class = DialysisType


class DialysisTypeSerializer(ModelSerializer):
    class Meta:
        model_class = DialysisType


class DialysisSerializer(MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    dialysis_type = DialysisTypeSerializer(read_only=True)
    dialysis_type_id = DialysisTypeLookupField(write_only=True)
    facility_id = FacilityLookupField(write_only=True)

    class Meta:
        model_class = Dialysis
