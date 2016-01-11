from radar.validation.core import Field, ValidationError
from radar.validation.validators import required
from radar.models.groups import GROUP_TYPE_COHORT


class CohortGroupValidationMixin(object):
    group = Field([required()])

    def validate_group(self, group):
        if group.type != GROUP_TYPE_COHORT:
            raise ValidationError('Must be a cohort.')

        return group
