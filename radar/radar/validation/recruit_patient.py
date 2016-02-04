from radar.validation.core import Validation, Field, pass_call, pass_context, ValidationError, ListField
from radar.validation.validators import optional, required, not_in_future, in_, not_empty, upper
from radar.models.patients import GENDERS, ETHNICITIES, Patient
from radar.permissions import has_permission_for_group
from radar.groups import is_radar_group
from radar.validation.number_validators import NUMBER_VALIDATORS
from radar.roles import PERMISSION
from radar.models.groups import GROUP_TYPE
from radar.patient_search import filter_by_patient_number_at_group
from radar.database import db
from radar.exceptions import PermissionDenied


def get_number_validators(number_group):
    return NUMBER_VALIDATORS.get((number_group.type, number_group.code))


class RecruitPatientSearchValidation(Validation):
    first_name = Field([not_empty(), upper()])
    last_name = Field([not_empty(), upper()])
    date_of_birth = Field([required(), not_in_future()])
    number = Field([not_empty()])
    number_group = Field([required()])

    def validate_number_group(self, number_group):
        # Group must have the is_recruitment_number_group flag set
        if not number_group.is_recruitment_number_group:
            raise ValidationError('Patient number not suitable for recruitment.')

        return number_group

    @pass_call
    def validate(self, call, obj):
        number_group = obj['number_group']

        number_validators = get_number_validators(number_group)

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        first_name = obj['first_name']
        last_name = obj['last_name']
        date_of_birth = obj['date_of_birth']
        number = obj['number']

        number_filter = filter_by_patient_number_at_group(number, number_group)
        patients = Patient.query.filter(number_filter).all()

        for patient in patients:
            # Check the supplied demographics match existing demographics
            # Note: Users are able to check if a patient is on RaDaR by only supplying a patient number
            # TODO this could do with being less strict (soundex?)
            match = (
                first_name in patient.first_names and
                last_name in patient.last_names and
                date_of_birth in patient.date_of_births
            )

            if not match:
                raise ValidationError({'number': "Supplied demographics don't match existing demographics."})

        return obj


class PatientNumberValidation(Validation):
    number = Field([not_empty()])
    number_group = Field([required()])

    @pass_call
    def validate(self, call, obj):
        number_group = obj['number_group']

        number_validators = get_number_validators(number_group)

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        return obj


class PatientNumberListField(ListField):
    def __init__(self, chain=None):
        super(PatientNumberListField, self).__init__(PatientNumberValidation(), chain=chain)

    def validate(self, obj):
        groups = set()

        # Check for groups with multiple numbers (e.g. two NHS numbers)
        for i, x in enumerate(obj):
            group = x['number_group']

            if group in groups:
                raise ValidationError({i: {'number_group': 'Number already supplied for group.'}})
            else:
                groups.add(group)

        return obj


class RecruitPatientValidation(Validation):
    first_name = Field([not_empty(), upper()])
    last_name = Field([not_empty(), upper()])
    date_of_birth = Field([required(), not_in_future()])
    gender = Field([optional(), in_(GENDERS.keys())])  # Required when adding a new patient
    ethnicities = Field([optional(), in_(ETHNICITIES.keys())])
    cohort_group = Field([required()])
    hospital_group = Field([required()])
    patient_numbers = PatientNumberListField([required()])

    @classmethod
    def get_patient(cls, obj):
        for i, x in enumerate(obj['patient_numbers']):
            if is_radar_group(x['number_group']):
                patient_id = int(x['number'])
                patient = Patient.query.get(patient_id)

                if patient is None:
                    raise ValidationError({'patient_numbers': {i: {'number': 'Patient not found.'}}})

                return patient

        return None

    @classmethod
    def get_recruitment_group(cls, obj):
        """Returns the first group with the recruitment flag set."""

        for x in obj['patient_numbers']:
            if x['number_group'].is_recruitment_number_group:
                return x['number_group']

        return None

    @classmethod
    def is_duplicate_patient_number(cls, obj):
        """Checks for a patient with this patient number."""
        number = obj['number']
        number_group = obj['number_group']
        number_filter = filter_by_patient_number_at_group(number, number_group)
        q = Patient.query.filter(number_filter).exists()
        duplicate = db.session.query(q).scalar()
        return duplicate

    def check_patient_numbers(cls, obj):
        for i, x in enumerate(obj['patient_numbers']):
            # Check if a patient already exists with this patient number
            if cls.is_duplicate_patient_number(x):
                raise ValidationError({'patient_numbers': {i: {'number': 'A patient already exists with this number.'}}})

    @pass_context
    def validate_cohort_group(self, ctx, cohort_group):
        current_user = ctx['user']

        # Must have the RECRUIT_PATIENT permission on the cohort (this can be granted through hospital permissions)
        if not has_permission_for_group(current_user, cohort_group, PERMISSION.RECRUIT_PATIENT):
            raise PermissionDenied()

        # Group must be a cohort
        if cohort_group.type != GROUP_TYPE.COHORT:
            raise ValidationError('Must be a cohort.')

        # Check this is a recruitment group
        if not cohort_group.is_recruitment_group:
            raise ValidationError('Cannot recruit into this cohort.')

        return cohort_group

    @pass_context
    def validate_hospital_group(self, ctx, hospital_group):
        current_user = ctx['user']

        # Must have the RECRUIT_PATIENT permission on the hospital
        if not has_permission_for_group(current_user, hospital_group, PERMISSION.RECRUIT_PATIENT, explicit=True):
            raise PermissionDenied()

        # Group must be a hospital
        if hospital_group.type != GROUP_TYPE.HOSPITAL:
            raise ValidationError('Must be a hospital.')

        return hospital_group

    @pass_call
    def validate(self, call, obj):
        # If a RaDaR number was supplied, find the patient
        patient = self.get_patient(obj)

        # Adding an existing patient to another cohort/hospital
        if patient:
            first_name = obj['first_name']
            last_name = obj['last_name']
            date_of_birth = obj['date_of_birth']

            # Check the supplied demographics match existing demographics
            # This is to prevent a user recruiting a patient without knowing their demographics
            # TODO this is very strict
            match = (
                first_name in patient.first_names and
                last_name in patient.last_names and
                date_of_birth in patient.date_of_births
            )

            if not match:
                raise ValidationError("Supplied demographics don't match existing demographics.")
        else:
            # Gender is required when adding a new patient
            call.validators_for_field([required()], obj, self.gender)

            recruitment_group = self.get_recruitment_group(obj)

            # Must supply a patient number for a group with the recruitment flag set (e.g. a NHS number)
            if recruitment_group is None:
                raise ValidationError({'patient_numbers': {'_': 'Missing a patient number suitable for recruitment.'}})

            self.check_patient_numbers(obj)

        return obj
