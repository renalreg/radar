from radar_api.serializers.patient_fields import PatientReferenceField


class PatientSerializerMixin(object):
    patient = PatientReferenceField()

    def get_model_exclude(self):
        attrs = super(PatientSerializerMixin, self).get_model_exclude()
        attrs.add('patient_id')
        return attrs
