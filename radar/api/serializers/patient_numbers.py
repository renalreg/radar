from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake.validators import max_length, normalise_whitespace, not_empty
from sqlalchemy import and_

from radar.api.serializers.common import (
    GroupField,
    MetaMixin,
    PatientMixin,
    SystemSourceMixin,
)
from radar.api.serializers.validators import get_number_validators
from radar.database import db
from radar.models.groups import GROUP_TYPE
from radar.models.patient_numbers import PatientNumber


class PatientNumberSerializer(PatientMixin, SystemSourceMixin, MetaMixin, ModelSerializer):
    number = fields.StringField(validators=[not_empty(), normalise_whitespace(), max_length(50)])
    number_group = GroupField()

    class Meta(object):
        model_class = PatientNumber
        exclude = ['number_group_id']

    def validate_number_group(self, number_group):
        # Don't allow patient numbers to be added for a system group (e.g. RADAR) as this
        # would cause confusion with the patient ID (from the patients.id column).
        if number_group.type == GROUP_TYPE.SYSTEM:
            raise ValidationError("Can't add system numbers.")

        return number_group

    def is_duplicate(self, data):
        q = PatientNumber.query

        # Check another patient doesn't already have this number (same source)
        q = q.filter(and_(
            PatientNumber.source_group == data['source_group'],
            PatientNumber.source_type == data['source_type'],
            PatientNumber.number_group == data['number_group'],
            PatientNumber.number == data['number']
        ))

        instance = self.instance

        if instance is not None:
            q = q.filter(PatientNumber.id != instance.id)

        q = q.exists()

        duplicate = db.session.query(q).scalar()

        return duplicate

    def validate(self, data):
        number_group = data['number_group']
        number_validators = get_number_validators(number_group)
        self.run_validators_on_field(data, 'number', number_validators)

        if self.is_duplicate(data):
            raise ValidationError({'number': 'A patient already exists with this number.'})

        return data
