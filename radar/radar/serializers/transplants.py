
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake import serializers
from cornflake.exceptions import ValidationError

from radar.serializers.common import PatientMixin, MetaMixin, SourceMixin
from radar.models.transplants import (
    Transplant,
    TransplantRejection,
    TransplantBiopsy,
    TRANSPLANT_MODALITIES
)
from radar.serializers.validators import valid_date_for_patient
from radar.database import db


class ListSerializer(serializers.ListSerializer):
    def validate_patient(self, data, patient):
        for i in range(len(data)):
            try:
                data[i] = self.child.validate_patient(data[i], patient)
            except ValidationError as e:
                raise ValidationError({i: e.errors})

        return data


class TransplantRejectionSerializer(ModelSerializer):
    date_of_rejection = fields.DateField()  # TODO after date

    class Meta(object):
        model_class = TransplantRejection
        exclude = ['id']

    def validate_patient(self, data, patient):
        return self.run_validators_on_serializer(data, [
            valid_date_for_patient('date_of_rejection', patient)
        ])


class TransplantBiopsySerializer(ModelSerializer):
    date_of_biopsy = fields.DateField()  # TODO after date
    recurrence = fields.BooleanField(required=False)

    class Meta(object):
        model_class = TransplantBiopsy
        exclude = ['id']

    def validate_patient(self, data, patient):
        return self.run_validators_on_serializer(data, [
            valid_date_for_patient('date_of_biopsy', patient)
        ])


class TransplantSerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    date = fields.DateField()
    modality = fields.IntegerLookupField(TRANSPLANT_MODALITIES)
    date_of_recurrence = fields.DateField(required=False)
    date_of_failure = fields.DateField(required=False)
    rejections = ListSerializer(child=TransplantRejectionSerializer())
    biopsies = ListSerializer(child=TransplantBiopsySerializer())

    class Meta(object):
        model_class = Transplant
        validators = [
            valid_date_for_patient('date'),
            valid_date_for_patient('date_of_recurrence'),
            valid_date_for_patient('date_of_failure'),
        ]

    def validate(self, data):
        patient = data['patient']
        self.rejections.validate_patient(data['rejections'], patient)
        self.biopsies.validate_patient(data['biopsies'], patient)

        if data['date_of_recurrence'] is not None and data['date_of_recurrence'] < data['date']:
            raise ValidationError({'date_of_recurrence': 'Must be on or after transplant date.'})

        if data['date_of_failure'] is not None and data['date_of_failure'] < data['date']:
            raise ValidationError({'date_of_failure': 'Must be on or after transplant date.'})

        return data

    def _save(self, instance, data):
        instance.date = data['date']
        instance.modality = data['modality']
        instance.date_of_recurrence = data['date_of_recurrence']
        instance.date_of_failure = data['date_of_failure']
        instance.rejections = self.rejections.create(data['rejections'])
        instance.biopsies = self.biopsies.create(data['biopsies'])
        return instance

    def create(self, data):
        instance = Transplant()
        self._save(instance, data)
        return instance

    def update(self, instance, data):
        # Unique constraint fails unless we flush the deletes before the inserts
        instance.rejections = []
        instance.biopsies = []
        db.session.flush()

        self._save(instance, data)

        return instance
