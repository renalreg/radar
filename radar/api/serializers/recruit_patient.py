from cornflake import fields, serializers
from cornflake.exceptions import ValidationError
from cornflake.validators import not_empty, upper, not_in_future

from radar.api.serializers.common import GroupField, StringLookupField, IntegerLookupField
from radar.api.serializers.validators import get_number_validators
from radar.exceptions import PermissionDenied
from radar.models.groups import GROUP_TYPE, check_dependencies, DependencyError
from radar.models.patient_codes import GENDERS, ETHNICITIES
from radar.permissions import has_permission_for_group
from radar.roles import PERMISSION


class RecruitPatientSearchSerializer(serializers.Serializer):
    first_name = fields.StringField(validators=[not_empty(), upper()])
    last_name = fields.StringField(validators=[not_empty(), upper()])
    date_of_birth = fields.DateField(validators=[not_in_future()])
    gender = IntegerLookupField(GENDERS)
    number = fields.StringField(validators=[not_empty()])
    number_group = GroupField()

    def validate_number_group(self, number_group):
        # Group must have the is_recruitment_number_group flag set
        if not number_group.is_recruitment_number_group:
            raise ValidationError('Patient number not suitable for recruitment.')

        return number_group

    def validate(self, data):
        data = super(RecruitPatientSearchSerializer, self).validate(data)

        number_group = data['number_group']
        number_validators = get_number_validators(number_group)
        self.run_validators_on_field(data, 'number', number_validators)

        return data


class RecruitPatientSerializer(RecruitPatientSearchSerializer):
    ethnicity = StringLookupField(ETHNICITIES, required=False)
    cohort_group = GroupField()
    hospital_group = GroupField()

    def validate_cohort_group(self, cohort_group):
        current_user = self.context['user']

        # Must have the RECRUIT_PATIENT permission on the cohort (this can be granted through hospital permissions)
        if not has_permission_for_group(current_user, cohort_group, PERMISSION.RECRUIT_PATIENT):
            raise PermissionDenied()

        # Group must be a cohort
        if cohort_group.type != GROUP_TYPE.COHORT:
            raise ValidationError('Must be a cohort.')

        # Check group dependencies
        try:
            check_dependencies([cohort_group])
        except DependencyError as e:
            raise ValidationError(e.message)

        return cohort_group

    def validate_hospital_group(self, hospital_group):
        current_user = self.context['user']

        # Must have the RECRUIT_PATIENT permission on the hospital
        if not has_permission_for_group(current_user, hospital_group, PERMISSION.RECRUIT_PATIENT, explicit=True):
            raise PermissionDenied()

        # Group must be a hospital
        if hospital_group.type != GROUP_TYPE.HOSPITAL:
            raise ValidationError('Must be a hospital.')

        return hospital_group


class PatientSerializer(serializers.Serializer):
    id = fields.IntegerField()


class RecruitPatientResultSerializer(serializers.Serializer):
    patient = PatientSerializer()
