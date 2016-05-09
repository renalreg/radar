from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.exceptions import ValidationError
from cornflake.validators import not_empty, normalise_whitespace, max_length
from sqlalchemy import and_, or_

from radar.api.serializers.common import (
    PatientMixin,
    RadarSourceMixin,
    MetaMixin,
    GroupField
)
from radar.api.serializers.validators import get_number_validators
from radar.database import db
from radar.groups import is_radar_group
from radar.models.patient_numbers import PatientNumber


class PatientNumberSerializer(PatientMixin, RadarSourceMixin, MetaMixin, ModelSerializer):
    number = fields.StringField(validators=[not_empty(), normalise_whitespace(), max_length(50)])
    number_group = GroupField()

    class Meta(object):
        model_class = PatientNumber
        exclude = ['number_group_id']

    def validate_number_group(self, number_group):
        if is_radar_group(number_group):
            raise ValidationError("Can't add RaDaR numbers.")

        return number_group

    def is_duplicate(self, data):
        q = PatientNumber.query

        # Check another patient doesn't already have this number (same source)
        c1 = and_(
            PatientNumber.source_group == data['source_group'],
            PatientNumber.source_type == data['source_type'],
            PatientNumber.number_group == data['number_group'],
            PatientNumber.number == data['number']
        )

        # Check this patient doesn't already have a number of this type (same source)
        c2 = and_(
            PatientNumber.patient == data['patient'],
            PatientNumber.source_group == data['source_group'],
            PatientNumber.source_type == data['source_type'],
            PatientNumber.number_group == data['number_group']
        )

        q = q.filter(or_(c1, c2))

        instance = self.instance

        if instance is not None:
            q = q.filter(PatientNumber.id != instance.id)

        q = q.exists()

        duplicate = db.session.query(q).scalar()

        return duplicate

    def validate(self, data):
        number_group = data['number_group']
        number_validators = get_number_validators(number_group)
        self.run_validators_on_field(data, self.number, number_validators)

        if self.is_duplicate(data):
            raise ValidationError({'number': 'A patient already exists with this number.'})

        return data
