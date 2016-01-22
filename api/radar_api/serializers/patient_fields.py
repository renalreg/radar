from radar.models.patients import Patient
from radar.serializers.models import ReferenceField


class PatientReferenceField(ReferenceField):
    model_class = Patient
