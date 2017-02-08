from cornflake import fields, serializers
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake.validators import max_length, none_if_blank, optional

from radar.api.serializers.common import (
    CohortGroupMixin,
    IntegerLookupField,
    MetaMixin,
    PatientMixin,
)
from radar.database import db
from radar.models.family_histories import FamilyHistory, FamilyHistoryRelative, RELATIONSHIPS
from radar.models.patients import Patient


class PatientSerializer(serializers.Serializer):
    id = fields.IntegerField()


class PatientField(ReferenceField):
    model_class = Patient
    serializer_class = PatientSerializer


class RelativeSerializer(ModelSerializer):
    relationship = IntegerLookupField(RELATIONSHIPS)
    patient = PatientField(required=False)  # TODO check not own relative

    class Meta(object):
        model_class = FamilyHistoryRelative
        exclude = ['id', 'patient_id', 'family_history_id']


class FamilyHistorySerializer(PatientMixin, CohortGroupMixin, MetaMixin, ModelSerializer):
    parental_consanguinity = fields.BooleanField()
    family_history = fields.BooleanField()
    other_family_history = fields.StringField(
        required=False,
        validators=[none_if_blank(), optional(), max_length(10000)]
    )
    relatives = serializers.ListSerializer(required=False, child=RelativeSerializer())

    class Meta(object):
        model_class = FamilyHistory

    def pre_validate(self, data):
        # No family history, no relatives
        if not data['family_history']:
            data['relatives'] = []

        return data

    def _save(self, instance, data):
        instance.patient = data['patient']

        instance.group = data['group']

        instance.parental_consanguinity = data['parental_consanguinity']
        instance.family_history = data['family_history']
        instance.other_family_history = data['other_family_history']
        instance.relatives = self.fields['relatives'].create(data['relatives'])

        instance.created_user = data['created_user']
        instance.modified_user = data['modified_user']
        instance.created_date = data['created_date']
        instance.modified_date = data['modified_date']

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
