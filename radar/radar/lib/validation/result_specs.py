from radar.lib.models import RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT, RESULT_SPEC_TYPES, RESULT_SPEC_TYPE_CODED_INTEGER, RESULT_SPEC_TYPE_CODED_STRING
from radar.lib.validation.core import Validation, Field, ValidationError, pass_new_obj, pass_call
from radar.lib.validation.validators import required, optional, none_if_blank, in_, max_length


class ResultSpecValidation(Validation):
    code = Field([required(), max_length(30)])  # TODO validate hco_3
    name = Field([required(), max_length(50)])
    short_name = Field([required(), max_length(30)])
    type = Field([required(), in_(RESULT_SPEC_TYPES)])
    units = Field([none_if_blank(), optional(), max_length(30)])
    min_value = Field([optional()])
    max_value = Field([optional()])
    options = Field([optional()])

    @pass_new_obj
    def validate_min_value(self, obj, min_value):
        if obj.type not in [RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT]:
            raise ValidationError('Only INTEGER and DECIMAL can specify a min_value.')

        if obj.type == RESULT_SPEC_TYPE_INTEGER and int(min_value) != min_value:
            raise ValidationError('min_value not a INTEGER.')

        return min_value

    @pass_new_obj
    def validate_max_value(self, obj, max_value):
        if obj.type not in [RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT]:
            raise ValidationError('Only INTEGER and DECIMAL can specify a max_value.')

        if obj.type == RESULT_SPEC_TYPE_INTEGER and int(max_value) != max_value:
            raise ValidationError('max_value not a INTEGER.')

        if obj.min_value is not None and max_value < obj.min_value:
            raise ValidationError('max_value must be >= min_value.')

        return max_value

    @pass_new_obj
    def validate_units(self, obj, units):
        if obj.type not in [RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT]:
            raise ValidationError('Only INTEGER and DECIMAL can specify units.')

        return units

    @pass_call
    def validate(self, call, obj):
        if obj.type == RESULT_SPEC_TYPE_CODED_STRING or obj.type == RESULT_SPEC_TYPE_CODED_INTEGER:
            call.validators_for_field([required()], obj, self.options)

        return obj
