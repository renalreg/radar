from radar.models import RESULT_SPEC_TYPE_INTEGER, RESULT_SPEC_TYPE_FLOAT, RESULT_SPEC_TYPE_CODED_STRING, \
    RESULT_SPEC_TYPE_CODED_INTEGER
from radar.validation.core import Validation, Field, pass_context, pass_old_obj, ValidationError, CleanObject
from radar.validation.data_sources import DataSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, min_, max_, optional, in_, max_length, none_if_blank, min_length


class ResultsValidation(Validation):
    def __init__(self, result_group_spec, **kwargs):
        super(ResultsValidation, self).__init__(**kwargs)
        self.result_group_spec = result_group_spec

    def clone(self, results):
        cloned_results = {}

        if results is None:
            for field_name in self.fields.keys():
                cloned_results[field_name] = None
        else:
            for field_name in self.fields.keys():
                cloned_results[field_name] = results.get(field_name)

        return CleanObject(cloned_results)

    def pre_validate(self, results):
        # Results without unknown keys
        cleaned_results = {}

        for field_name in self.fields.keys():
            cleaned_results[field_name] = results.get(field_name)

        return cleaned_results

    def get_fields(self):
        fields = {}

        result_group_spec = self.result_group_spec

        for result_spec in result_group_spec.result_specs:
            type = result_spec.type

            if type == RESULT_SPEC_TYPE_INTEGER or type == RESULT_SPEC_TYPE_FLOAT:
                validators = [optional()]

                min_value = result_spec.min_value
                max_value = result_spec.max_value

                if min_value is not None:
                    validators.append(min_(min_value))

                if max_value is not None:
                    validators.append(max_(max_value))
            elif type == RESULT_SPEC_TYPE_CODED_STRING or type == RESULT_SPEC_TYPE_CODED_INTEGER:
                validators = [optional(), in_(result_spec.option_values)]
            else:
                validators = [none_if_blank(), optional()]

                min_length_value = result_spec.min_length
                max_length_value = result_spec.max_length

                if min_length_value is not None:
                    validators.append(min_length(min_length_value))

                if max_length_value is not None:
                    validators.append(max_length(max_length_value))
                else:
                    validators.append(max_length(1000))

            field = Field(validators)
            field.bind(result_spec.code)
            fields[result_spec.code] = field

        return fields

    def validate(self, obj):
        # True if at least one result was entered
        result_entered = False

        for field_name in self.fields.keys():
            if obj.get(field_name) is not None:
                result_entered = True
                break

        if not result_entered:
            errors = {}

            for field_name in self.fields.keys():
                errors[field_name] = 'Must enter at least one result.'

            raise ValidationError(errors)

        return obj


class ResultGroupValidation(PatientValidationMixin, DataSourceValidationMixin, MetaValidationMixin, Validation):
    date = Field([required()])
    result_group_spec = Field([required()])
    results = Field([required()])

    @pass_context
    @pass_old_obj
    def validate(self, ctx, old_obj, obj):
        validation = ResultsValidation(obj.result_group_spec)
        old_results = validation.clone(old_obj.results)

        try:
            obj.results = validation.after_update(ctx, old_results, obj.results)
        except ValidationError as e:
            raise ValidationError({'results': e.errors})

        return obj
