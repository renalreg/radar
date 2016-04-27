from sqlalchemy import and_, or_

from radar.groups import is_radar_group
from radar.validation.core import Validation, pass_call, ValidationError, Field
from radar.validation.sources import RadarSourceValidationMixin
from radar.validation.meta import MetaValidationMixin
from radar.validation.patients import PatientValidationMixin
from radar.validation.validators import required, max_length, not_empty, normalise_whitespace
from radar.validation.number_validators import NUMBER_VALIDATORS
from radar.models.patient_numbers import PatientNumber
from radar.database import db


class PatientNumberValidation(PatientValidationMixin, RadarSourceValidationMixin, MetaValidationMixin, Validation):
    number = Field([not_empty(), normalise_whitespace(), max_length(50)])
    number_group = Field([required()])

    def validate_number_group(self, number_group):
        if is_radar_group(number_group):
            raise ValidationError("Can't add RaDaR numbers.")

        return number_group

    @classmethod
    def is_duplicate(cls, obj):
        q = PatientNumber.query

        # Check another patient doesn't already have this number (same source)
        c1 = and_(
            PatientNumber.source_group == obj.source_group,
            PatientNumber.source_type == obj.source_type,
            PatientNumber.number_group == obj.number_group,
            PatientNumber.number == obj.number
        )

        # Check this patient doesn't already have a number of this type (same source)
        c2 = and_(
            PatientNumber.patient == obj.patient,
            PatientNumber.source_group == obj.source_group,
            PatientNumber.source_type == obj.source_type,
            PatientNumber.number_group == obj.number_group
        )

        q = q.filter(or_(c1, c2))

        if obj.id is not None:
            q = q.filter(PatientNumber.id != obj.id)

        q = q.exists()

        duplicate = db.session.query(q).scalar()

        return duplicate

    @pass_call
    def validate(self, call, obj):
        number_group = obj.number_group

        number_validators = NUMBER_VALIDATORS.get((number_group.type, number_group.code))

        if number_validators is not None:
            call.validators_for_field(number_validators, obj, self.number)

        if self.is_duplicate(obj):
            raise ValidationError({'number': 'A patient already exists with this number.'})

        return obj
