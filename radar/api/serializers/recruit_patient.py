from cornflake import fields, serializers
from cornflake.exceptions import ValidationError
from cornflake.validators import min_length, not_empty, not_in_future, upper

from radar.api.serializers.common import GroupField, IntegerLookupField
from radar.api.serializers.demographics import EthnicityField, NationalityField
from radar.api.serializers.validators import get_number_validators
from radar.exceptions import PermissionDenied
from radar.models.diagnoses import BIOPSY_DIAGNOSES
from radar.models.groups import check_dependencies, DependencyError, GROUP_TYPE
from radar.models.patient_codes import GENDERS
from radar.permissions import has_permission_for_group
from radar.roles import PERMISSION


class RecruitPatientSearchSerializer(serializers.Serializer):
    first_name = fields.StringField(validators=[not_empty(), upper(), min_length(2)])
    last_name = fields.StringField(validators=[not_empty(), upper(), min_length(2)])
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


class RecruitPatientDiagnosisSerializer(serializers.Serializer):
    diagnosis_id = fields.IntegerField()
    symptoms_date = fields.DateField(required=False)
    from_date = fields.DateField()
    to_date = fields.DateField(required=False)
    prenatal = fields.BooleanField(required=False)
    gene_test = fields.BooleanField(required=False)
    biochemistry = fields.BooleanField(required=False)
    clinical_picture = fields.BooleanField(required=False)
    biopsy = fields.BooleanField(required=False)
    biopsy_diagnosis = IntegerLookupField(BIOPSY_DIAGNOSES, required=False)
    comments = fields.StringField(required=False)


class RecruitPatientSerializer(RecruitPatientSearchSerializer):
    cohort_group = GroupField()
    hospital_group = GroupField()
    consents = fields.Field()
    ethnicity = EthnicityField(required=False)
    nationality = NationalityField(required=False)
    diagnosis = RecruitPatientDiagnosisSerializer()

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
            raise ValidationError(e.args[0])

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
