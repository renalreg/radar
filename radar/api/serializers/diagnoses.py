from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake import fields
from cornflake import serializers
from cornflake.validators import none_if_blank, optional, max_length
from cornflake.exceptions import ValidationError

from radar.api.serializers.common import (
    PatientMixin,
    SourceMixin,
    MetaMixin,
    TinyGroupSerializer,
    IntegerLookupField
)
from radar.api.serializers.validators import valid_date_for_patient
from radar.models.diagnoses import (
    Diagnosis,
    PatientDiagnosis,
    BIOPSY_DIAGNOSES,
    GROUP_DIAGNOSIS_TYPE
)


class GroupDiagnosisSerializer(serializers.Serializer):
    group = TinyGroupSerializer()
    type = fields.EnumField(GROUP_DIAGNOSIS_TYPE)


class DiagnosisSerializer(ModelSerializer):
    groups = fields.ListField(child=GroupDiagnosisSerializer(), source='group_diagnoses')

    class Meta(object):
        model_class = Diagnosis


class TinyDiagnosisSerializer(ModelSerializer):
    class Meta(object):
        model_class = Diagnosis


class DiagnosisField(ReferenceField):
    model_class = Diagnosis
    serializer_class = TinyDiagnosisSerializer


class PatientDiagnosisSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    diagnosis = DiagnosisField(required=False)
    diagnosis_text = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(1000)])
    symptoms_date = fields.DateField(required=False)
    symptoms_age = fields.IntegerField(read_only=True)
    from_date = fields.DateField()
    from_age = fields.IntegerField(read_only=True)
    to_date = fields.DateField(required=False)
    to_age = fields.IntegerField(read_only=True)
    gene_test = fields.BooleanField(required=False)
    biochemistry = fields.BooleanField(required=False)
    clinical_picture = fields.BooleanField(required=False)
    biopsy = fields.BooleanField(required=False)
    biopsy_diagnosis = IntegerLookupField(BIOPSY_DIAGNOSES, required=False)
    comments = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])

    class Meta(object):
        model_class = PatientDiagnosis
        exclude = ['diagnosis_id']
        validators = [
            valid_date_for_patient('symptoms_date'),
            valid_date_for_patient('from_date'),
            valid_date_for_patient('to_date'),
        ]

    def pre_validate(self, data):
        if data['diagnosis'] is not None:
            data['diagnosis_text'] = None

        if not data['biopsy']:
            data['biopsy_diagnosis'] = None

        return data

    def validate(self, data):
        if data['diagnosis'] is None and data['diagnosis_text'] is None:
            raise ValidationError({
                'diagnosis': 'Must specify a diagnosis.',
                'diagnosis_text': 'Must specify a diagnosis.',
            })

        # symptoms_date <= from_date <= to_date

        if data['symptoms_date'] is not None and data['from_date'] < data['symptoms_date']:
            raise ValidationError({'from_date': 'Must be on or after date of onset of symptoms.'})

        if data['to_date'] is not None and data['to_date'] < data['from_date']:
            raise ValidationError({'to_date': 'Must be on or after from date.'})

        return data
