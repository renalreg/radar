from radar.lib.serializers import MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer, \
    DateField, StringField
from radar.models import Hospitalisation


class HospitalisationSerializer(MetaSerializerMixin, PatientSerializerMixin, FacilitySerializerMixin, ModelSerializer):
    date_of_admission = DateField()
    date_of_discharge = DateField()
    reason_for_admission = StringField()
    comments = StringField()

    class Meta:
        model_class = Hospitalisation
