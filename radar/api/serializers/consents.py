from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
)
from radar.models.consents import Consent, CONSENT_TYPE, PatientConsent


class ConsentSerializer(ModelSerializer):
    code = fields.StringField()
    label = fields.StringField()
    paediatric = fields.BooleanField(default=False)
    from_date = fields.DateField()
    consent_type = fields.EnumField(CONSENT_TYPE)
    weight = fields.IntegerField()

    class Meta(object):
        model_class = Consent


class ConsentField(ReferenceField):
    model_class = Consent
    serializer_class = ConsentSerializer


class PatientConsentSerializer(PatientMixin, MetaMixin, ModelSerializer):
    consent = ConsentField()
    signed_on_date = fields.DateField()
    withdrawn_on_date = fields.DateField(required=False)

    class Meta(object):
        model_class = PatientConsent
        exclude = ['consent_id']
