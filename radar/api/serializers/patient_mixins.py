from radar.lib.models import Patient
from radar.lib.serializers import ReferenceField


class PatientReferenceField(ReferenceField):
    model_class = Patient


class PatientSerializerMixin(object):
    patient = PatientReferenceField()

    def get_model_exclude(self):
        attrs = super(PatientSerializerMixin, self).get_model_exclude()
        attrs.add('patient_id')
        return attrs
