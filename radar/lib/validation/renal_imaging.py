from radar.lib.validation.core import Validation, Field, pass_call
from radar.lib.validation.data_sources import DataSourceValidationMixin
from radar.lib.validation.patients import PatientValidationMixin
from radar.lib.validation.validators import required, valid_date_for_patient, range_, optional


class RenalImagingValidation(PatientValidationMixin, DataSourceValidationMixin, Validation):
    data = Field([required(), valid_date_for_patient()])
    imaging_type = Field([required()])

    right_present = Field([required()])
    right_type = Field([required()])  # TODO in_
    right_length = Field([optional(), range_(0, 100)])  # TODO range
    right_cysts = Field([optional()])
    right_calcification = Field([optional()])
    right_nephrocalcinosis = Field([optional()])
    right_nephrolithiasis = Field([optional()])

    left_present = Field([required()])
    left_type = Field([required()])  # TODO in_
    left_length = Field([optional(), range_(0, 100)])  # TODO range
    left_cysts = Field([optional()])
    left_calcification = Field([optional()])
    left_nephrocalcinosis = Field([optional()])
    left_nephrolithiasis = Field([optional()])

    def pre_validate(self, obj):
        if not obj.right_present:
            obj.right_type = None
            obj.right_length = None
            obj.right_cysts = None
            obj.right_calcification = None
            obj.right_nephrocalcinosis = None
            obj.right_nephrolithiasis = None
        elif not obj.right_calcification:
            obj.right_nephrocalcinosis = None
            obj.right_nephrolithiasis = None

        if not obj.left_present:
            obj.left_type = None
            obj.left_length = None
            obj.left_cysts = None
            obj.left_calcification = None
            obj.left_nephrocalcinosis = None
            obj.left_nephrolithiasis = None
        elif not obj.left_calcification:
            obj.left_nephrocalcinosis = None
            obj.left_nephrolithiasis = None

        return obj

    @pass_call
    def validate(self, call, obj):
        if obj.right_present:
            call.validators_for_field([required()], obj, self.right_type)
            call.validators_for_field([required()], obj, self.right_length)
            call.validators_for_field([required()], obj, self.right_cysts)
            call.validators_for_field([required()], obj, self.right_calcification)

            if obj.right_calcification:
                call.validators_for_field([required()], obj, self.right_nephrocalcinosis)
                call.validators_for_field([required()], obj, self.right_nephrolithiasis)

        if obj.left_present:
            call.validators_for_field([required()], obj, self.left_type)
            call.validators_for_field([required()], obj, self.left_length)
            call.validators_for_field([required()], obj, self.left_cysts)
            call.validators_for_field([required()], obj, self.left_calcification)

            if obj.left_calcification:
                call.validators_for_field([required()], obj, self.left_nephrocalcinosis)
                call.validators_for_field([required()], obj, self.left_nephrolithiasis)
