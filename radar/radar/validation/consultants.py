from radar.validation.core import Field, Validation, ListField, ValidationError
from radar.validation.meta import MetaValidationMixin
from radar.validation.validators import not_empty, none_if_blank, optional, email_address, max_length, required, upper, lower
from radar.validation.number_validators import gmc_number
from radar.models.groups import GROUP_TYPE


class GroupConsultantValidation(MetaValidationMixin, Validation):
    group = Field([required()])

    def validate_group(self, group):
        if group.type != GROUP_TYPE.HOSPITAL:
            raise ValidationError('Must be a hospital.')

        return group


class GroupConsultantListField(ListField):
    def __init__(self, chain=None):
        super(GroupConsultantListField, self).__init__(GroupConsultantValidation(), chain=chain)

    def validate(self, group_consultants):
        groups = set()

        for i, group_consultant in enumerate(group_consultants):
            group = group_consultant.group

            if group in groups:
                raise ValidationError({i: {'group': 'Consultant already in group.'}})
            else:
                groups.add(group)

        return group_consultants


class ConsultantValidation(MetaValidationMixin, Validation):
    first_name = Field([not_empty(), upper(), max_length(100)])
    last_name = Field([not_empty(), upper(), max_length(100)])
    email = Field([none_if_blank(), optional(), lower(), email_address()])
    telephone_number = Field([none_if_blank(), optional(), max_length(100)])
    gmc_number = Field([optional(), gmc_number()])
    group_consultants = GroupConsultantListField()
