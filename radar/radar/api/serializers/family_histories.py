from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake import fields
from cornflake import serializers
from cornflake.validators import none_if_blank, optional, max_length

from radar.serializers.common import PatientMixin, SourceMixin, MetaMixin
from radar.models.family_history import FamilyHistory, FamilyHistoryRelative, RELATIONSHIPS
from radar.models.patients import Patient
from radar.database import db


class PatientSerializer(serializers.Serializer):
    id = fields.IntegerField()


class PatientField(ReferenceField):
    model_class = Patient
    serializer_class = PatientSerializer


class RelativeSerializer(ModelSerializer):
    relationship = fields.IntegerLookupField(RELATIONSHIPS)
    patient = PatientField(required=False)  # TODO check not own relative

    class Meta(object):
        model_class = FamilyHistoryRelative
        exclude = ['id', 'patient_id']


class FamilyHistorySerializer(PatientMixin, SourceMixin, MetaMixin, ModelSerializer):
    parental_consanguinity = fields.BooleanField()
    family_history = fields.BooleanField()
    other_family_history = fields.StringField(required=False, validators=[none_if_blank(), optional(), max_length(10000)])
    relatives = serializers.ListSerializer(child=RelativeSerializer())

    class Meta(object):
        model_class = FamilyHistory

    def pre_validate(self, data):
        if not data['family_history']:
            data['relatives'] = []

        return data

    def _save(self, instance, data):
        instance.parental_consanguinity = data['parental_consanguinity']
        instance.family_history = data['family_history']
        instance.other_family_history = data['other_family_history']
        instance.relatives = self.relatives.create(data['relatives'])

    def create(self, data):
        instance = FamilyHistory()
        self._save(instance, data)
        return instance

    def update(self, instance, data):
        # Unique constraint fails unless we flush the deletes before the inserts
        instance.relatives = []
        db.session.flush()

        self._save(instance, data)

        return instance
