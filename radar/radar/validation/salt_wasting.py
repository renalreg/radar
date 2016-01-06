from radar.validation.core import Validation, Field, pass_call
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import optional, required, none_if_blank, max_length, not_empty, range_
from radar.validation.meta import MetaValidationMixin


class SaltWastingClinicalFeaturesValidation(PatientValidationMixin, MetaValidationMixin, Validation):
    normal_pregnancy = Field([required()])
    abnormal_pregnancy_text = Field([none_if_blank(), optional(), max_length(10000)])

    neurological_problems = Field([required()])
    seizures = Field([optional()])
    abnormal_gait = Field([optional()])
    deafness = Field([optional()])
    other_neurological_problem = Field([optional()])
    other_neurological_problem_text = Field([none_if_blank(), optional(), max_length(10000)])

    joint_problems = Field([required()])
    joint_problems_age = Field([optional(), range_(0, 120)])
    x_ray_abnormalities = Field([optional()])
    chondrocalcinosis = Field([optional()])
    other_x_ray_abnormality = Field([optional()])
    other_x_ray_abnormality_text = Field([none_if_blank(), optional(), max_length(10000)])

    def pre_validate(self, obj):
        if obj.normal_pregnancy:
            obj.abnormal_pregnancy_text = None

        if not obj.neurological_problems:
            obj.seizures = None
            obj.abnormal_gait = None
            obj.deafness = None
            obj.other_neurological_problem = None
            obj.other_neurological_problem_text = None
        elif not obj.other_neurological_problem:
            obj.other_neurological_problem_text = None

        if not obj.joint_problems:
            obj.joint_problems_age = None
            obj.x_ray_abnormalities = None
            obj.chondrocalcinosis = None
            obj.other_x_ray_abnormality = None
            obj.other_x_ray_abnormality_text = None
        elif not obj.x_ray_abnormalities:
            obj.chondrocalcinosis = None
            obj.other_x_ray_abnormality = None
            obj.other_x_ray_abnormality_text = None
        elif not obj.other_x_ray_abnormality:
            obj.other_x_ray_abnormality_text = None

        return obj

    @pass_call
    def validate(self, call, obj):
        if not obj.normal_pregnancy:
            call.validators_for_field([not_empty()], obj, self.abnormal_pregnancy_text)

        if obj.neurological_problems:
            call.validators_for_field([required()], obj, self.seizures)
            call.validators_for_field([required()], obj, self.abnormal_gait)
            call.validators_for_field([required()], obj, self.deafness)
            call.validators_for_field([required()], obj, self.other_neurological_problem)

            if obj.other_neurological_problem:
                call.validators_for_field([not_empty()], obj, self.other_neurological_problem_text)

        if obj.joint_problems:
            call.validators_for_field([required()], obj, self.joint_problems_age)
            call.validators_for_field([required()], obj, self.x_ray_abnormalities)

            if obj.x_ray_abnormalities:
                call.validators_for_field([required()], obj, self.chondrocalcinosis)
                call.validators_for_field([required()], obj, self.other_x_ray_abnormality)

                if obj.other_x_ray_abnormality:
                    call.validators_for_field([not_empty()], obj, self.other_x_ray_abnormality_text)

        return obj
