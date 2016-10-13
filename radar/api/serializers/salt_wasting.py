from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import (
    range_,
    none_if_blank,
    optional,
    max_length,
    required,
    not_empty
)

from radar.api.serializers.common import PatientMixin, MetaMixin
from radar.models.salt_wasting import SaltWastingClinicalFeatures


class SaltWastingClinicalFeaturesSerializer(PatientMixin, MetaMixin, ModelSerializer):
    normal_pregnancy = fields.BooleanField(required=False)
    abnormal_pregnancy_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    neurological_problems = fields.BooleanField(required=False)
    seizures = fields.BooleanField(required=False)
    abnormal_gait = fields.BooleanField(required=False)
    deafness = fields.BooleanField(required=False)
    other_neurological_problem = fields.BooleanField(required=False)
    other_neurological_problem_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    joint_problems = fields.BooleanField(required=False)
    joint_problems_age = fields.IntegerField(required=False, validators=[range_(0, 120)])
    x_ray_abnormalities = fields.BooleanField(required=False)
    chondrocalcinosis = fields.BooleanField(required=False)
    other_x_ray_abnormality = fields.BooleanField(required=False)
    other_x_ray_abnormality_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = SaltWastingClinicalFeatures

    def pre_validate(self, data):
        if data['normal_pregnancy']:
            data['abnormal_pregnancy_text'] = None

        if not data['neurological_problems']:
            data['seizures'] = None
            data['abnormal_gait'] = None
            data['deafness'] = None
            data['other_neurological_problem'] = None
            data['other_neurological_problem_text'] = None
        elif not data['other_neurological_problem']:
            data['other_neurological_problem_text'] = None

        if not data['joint_problems']:
            data['joint_problems_age'] = None
            data['x_ray_abnormalities'] = None
            data['chondrocalcinosis'] = None
            data['other_x_ray_abnormality'] = None
            data['other_x_ray_abnormality_text'] = None
        elif not data['x_ray_abnormalities']:
            data['chondrocalcinosis'] = None
            data['other_x_ray_abnormality'] = None
            data['other_x_ray_abnormality_text'] = None
        elif not data['other_x_ray_abnormality']:
            data['other_x_ray_abnormality_text'] = None

        return data

    def validate(self, data):
        if data['normal_pregnancy'] is False:
            self.run_validators_on_field(data, 'abnormal_pregnancy_text', [not_empty()])

        if data['neurological_problems']:
            self.run_validators_on_field(data, 'seizures', [required()])
            self.run_validators_on_field(data, 'abnormal_gait', [required()])
            self.run_validators_on_field(data, 'deafness', [required()])
            self.run_validators_on_field(data, 'other_neurological_problem', [required()])

            if data['other_neurological_problem']:
                self.run_validators_on_field(data, 'other_neurological_problem_text', [not_empty()])

        if data['joint_problems']:
            self.run_validators_on_field(data, 'joint_problems_age', [required()])
            self.run_validators_on_field(data, 'x_ray_abnormalities', [required()])

            if data['x_ray_abnormalities']:
                self.run_validators_on_field(data, 'chondrocalcinosis', [required()])
                self.run_validators_on_field(data, 'other_x_ray_abnormality', [required()])

                if data['other_x_ray_abnormality']:
                    self.run_validators_on_field(data, 'other_x_ray_abnormality_text', [not_empty()])

        return data
