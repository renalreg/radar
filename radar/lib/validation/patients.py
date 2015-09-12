from radar.lib.permissions import intersect_patient_and_user_organisations
from radar.lib.validation.core import Field, ValidationError, pass_context, pass_call, pass_new_obj
from radar.lib.validation.validators import required


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
    patient = PatientField(chain=[required()])
    created_date = Field()

    @pass_new_obj
    @pass_call
    def get_context(self, ctx, call, obj):
        ctx = call(super(PatientValidationMixin, self).get_context, ctx)

        if obj.patient is not None:
            ctx['patient'] = obj.patient
        else:
            raise ValidationError({'patient': 'This field is required.'})

        return ctx
