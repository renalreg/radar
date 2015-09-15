from radar.lib.validation.cohorts import CohortValidationMixin
from radar.lib.validation.core import Field, Validation, pass_call
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, optional, max_length, \
    none_if_blank, valid_date_for_patient


class GeneticsValidation(PatientValidationMixin, CohortValidationMixin, Validation):
    sample_sent = Field([required()])
    sample_sent_date = Field([optional(), valid_date_for_patient()])
    laboratory = Field([none_if_blank(), optional(), max_length(100)])
    laboratory_reference_number = Field([none_if_blank(), optional(), max_length(100)])
    results = Field([none_if_blank(), optional(), max_length(10000)])

    @pass_call
    def pre_validate(self, call, obj):
        obj = call(super(GeneticsValidation, self).pre_validate, obj)

        if not obj.sample_sent:
            obj.sample_sent_date = None
            obj.laboratory = None
            obj.laboratory_reference_number = None
            obj.results = None

        return obj

    @pass_call
    def validate(self, call, obj):
        # If a sample was sent a date is required
        if obj.sample_sent:
            call.validators_for_field([required()], obj, self.sample_sent_date)

        return obj
