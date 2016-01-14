from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION
from radar.validation.core import Field, ValidationError, pass_context, pass_call, pass_new_obj, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, none_if_blank, max_length, optional


class PatientValidation(MetaValidationMixin, Validation):
    comments = Field([none_if_blank(), optional(), max_length(10000)])


class PatientField(Field):
    @pass_context
    def validate(self, ctx, patient):
        user = ctx['user']

        if not user.is_admin and not has_permission_for_patient(user, patient, PERMISSION.EDIT_PATIENT):
            raise ValidationError('PERMISSION denied!')

        return patient


class PatientValidationMixin(object):
    patient = PatientField([required()])

    @pass_new_obj
    @pass_call
    def get_context(self, ctx, call, obj):
        ctx = call(super(PatientValidationMixin, self).get_context, ctx)

        if obj.patient is not None:
            ctx['patient'] = obj.patient
        else:
            raise ValidationError({'patient': 'This field is required.'})

        return ctx
