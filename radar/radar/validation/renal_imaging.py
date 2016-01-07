from radar.models import RENAL_IMAGING_TYPES, RENAL_IMAGING_KIDNEY_TYPES
from radar.validation.core import Validation, Field, pass_call, ValidationError
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, valid_date_for_patient, range_, optional, in_, none_if_blank, \
    max_length


class RenalImagingValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date = Field([required(), valid_date_for_patient()])
    imaging_type = Field([required(), in_(RENAL_IMAGING_TYPES.keys())])

    right_present = Field([optional()])
    right_type = Field([optional(), in_(RENAL_IMAGING_KIDNEY_TYPES.keys())])
    right_length = Field([optional(), range_(1, 30)])
    right_volume = Field([optional()])  # TODO range
    right_cysts = Field([optional()])
    right_stones = Field([optional()])
    right_calcification = Field([optional()])
    right_nephrocalcinosis = Field([optional()])
    right_nephrolithiasis = Field([optional()])
    right_other_malformation = Field([none_if_blank(), optional(), max_length(10000)])

    left_present = Field([optional()])
    left_type = Field([optional(), in_(RENAL_IMAGING_KIDNEY_TYPES.keys())])
    left_length = Field([optional(), range_(1, 30)])
    left_volume = Field([optional()])  # TODO range
    left_cysts = Field([optional()])
    left_stones = Field([optional()])
    left_calcification = Field([optional()])
    left_nephrocalcinosis = Field([optional()])
    left_nephrolithiasis = Field([optional()])
    left_other_malformation = Field([none_if_blank(), optional(), max_length(10000)])

    def pre_validate(self, obj):
        if not obj.right_present:
            obj.right_type = None
            obj.right_length = None
            obj.right_volume = None
            obj.right_cysts = None
            obj.right_stones = None
            obj.right_calcification = None
            obj.right_nephrocalcinosis = None
            obj.right_nephrolithiasis = None
            obj.right_other_malformation = None
        elif not obj.right_calcification:
            obj.right_nephrocalcinosis = None
            obj.right_nephrolithiasis = None

        if not obj.left_present:
            obj.left_type = None
            obj.left_length = None
            obj.left_volume = None
            obj.left_cysts = None
            obj.left_stones = None
            obj.left_calcification = None
            obj.left_nephrocalcinosis = None
            obj.left_nephrolithiasis = None
            obj.left_other_malformation = None
        elif not obj.left_calcification:
            obj.left_nephrocalcinosis = None
            obj.left_nephrolithiasis = None

        return obj

    @pass_call
    def validate(self, call, obj):
        if obj.right_present is None and obj.left_present is None:
            raise ValidationError({
                'right_present': 'Either right or left must be present.',
                'left_present': 'Either right or left must be present.'
            })

        if obj.right_present:
            call.validators_for_field([required()], obj, self.right_type)
            call.validators_for_field([required()], obj, self.right_cysts)
            call.validators_for_field([required()], obj, self.right_stones)
            call.validators_for_field([required()], obj, self.right_calcification)

            if obj.right_calcification:
                call.validators_for_field([required()], obj, self.right_nephrocalcinosis)
                call.validators_for_field([required()], obj, self.right_nephrolithiasis)

        if obj.left_present:
            call.validators_for_field([required()], obj, self.left_type)
            call.validators_for_field([required()], obj, self.left_cysts)
            call.validators_for_field([required()], obj, self.left_stones)
            call.validators_for_field([required()], obj, self.left_calcification)

            if obj.left_calcification:
                call.validators_for_field([required()], obj, self.left_nephrocalcinosis)
                call.validators_for_field([required()], obj, self.left_nephrolithiasis)

        return obj
