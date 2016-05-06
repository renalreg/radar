from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields
from cornflake.validators import (
    not_empty,
    normalise_whitespace,
    max_length,
    none_if_blank,
    optional,
    required,
    postcode
)
from cornflake.exceptions import ValidationError, SkipField

from radar.common import PatientMixin, RadarSourceMixin, MetaMixin
from radar.models.patient_addresses import PatientAddress
from radar.serializers.validators import remove_trailing_comma, after_date_of_birth
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION


class PatientAddressSerializer(PatientMixin, RadarSourceMixin, MetaMixin, ModelSerializer):
    from_date = fields.DateField(required=False)
    to_date = fields.DateField(required=False)
    address_1 = fields.StringField([
        not_empty(),
        remove_trailing_comma(),
        not_empty(),
        normalise_whitespace(),
        max_length(100)
    ])
    address_2 = fields.StringField([
        none_if_blank(),
        optional(),
        remove_trailing_comma(),
        none_if_blank(),
        optional(),
        normalise_whitespace(),
        max_length(100)
    ])
    address_3 = fields.StringField([
        none_if_blank(),
        optional(),
        remove_trailing_comma(),
        none_if_blank(),
        optional(),
        normalise_whitespace(),
        max_length(100)
    ])
    address_4 = fields.StringField([
        none_if_blank(),
        optional(),
        remove_trailing_comma(),
        none_if_blank(),
        optional(),
        normalise_whitespace(),
        max_length(100)
    ])
    postcode = fields.StringField([required(), postcode()])

    class Meta(object):
        model_class = PatientAddress
        validators = [
            after_date_of_birth('from_date'),
            after_date_of_birth('to_date'),
        ]

    def validate(self, data):
        data = super(PatientAddressSerializer, self).validate(data)

        if (
            data['from_date'] is not None and
            data['to_date'] is not None and
            data['to_date'] < data['from_date']
        ):
            raise ValidationError({'to_date': 'Must be on or after from date.'})

    def to_representation(self, value):
        user = self.context['user']
        value = PatientAddressProxy(value, user)
        value = super(PatientAddressSerializer, self).to_representation(value)
        return value


class PatientAddressProxy(object):
    def __init__(self, address, user):
        self.address = address
        self.user = user
        self.demographics_permission = has_permission_for_patient(user, address.patient, PERMISSION.VIEW_DEMOGRAPHICS)

    @property
    def address_1(self):
        if self.demographics_permission:
            return self.address.address_1
        else:
            raise SkipField

    @property
    def address_2(self):
        if self.demographics_permission:
            return self.address.address_2
        else:
            raise SkipField

    @property
    def address_3(self):
        if self.demographics_permission:
            return self.address.address_3
        else:
            raise SkipField

    @property
    def address_4(self):
        if self.demographics_permission:
            return self.address.address_4
        else:
            raise SkipField

    @property
    def postcode(self):
        postcode = self.address.postcode

        if self.demographics_permission:
            return postcode
        else:
            # Return the first part of the postcode
            # Postcodes from the database should have a space but limit to 4 characters just in case
            return postcode.split(' ')[0][:4]

    def __getattr__(self, item):
        return getattr(self.address, item)
