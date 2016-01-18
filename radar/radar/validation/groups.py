from radar.validation.core import Field, Validation, pass_context
from radar.validation.validators import required
from radar.models.groups import GROUP_TYPE_COHORT
from radar.exceptions import PermissionDenied


class CohortGroupValidationMixin(object):
    group = Field([required()])

    @pass_context
    def validate_group(self, ctx, group):
        patient = ctx['patient']

        if group.type != GROUP_TYPE_COHORT:
            raise PermissionDenied()

        if not patient.in_group(group):
            raise PermissionDenied()

        return group


# TODO
class GroupValidation(Validation):
    pass
