from radar.permissions import intersect_patient_and_user_organisations
from radar.validation.core import Field, ValidationError, pass_context, pass_call, pass_new_obj, Validation
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import required, none_if_blank, max_length, optional


class PatientValidation(MetaValidationMixin, Validation):
    recruited_organisation = Field([required()])  # TODO validate
    is_active = Field([required()])
    comments = Field([none_if_blank(), optional(), max_length(1000)])


class PatientField(Field):
    @pass_context
    def validate(self, ctx, patient):
        user = ctx['user']

        if not user.is_admin:
            organisation_users = intersect_patient_and_user_organisations(patient, user, user_membership=True)

            if not any(x.has_edit_patient_permission for x in organisation_users):
                raise ValidationError('Permission denied!')

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
