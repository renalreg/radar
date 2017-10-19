from cornflake import fields

from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField

from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
)

from radar.models.consents import Consent, PatientConsent


class ConsentSerializer(ModelSerializer):
    code = fields.StringField()
    label = fields.StringField()
    paediatric = fields.BooleanField(default=False)
    from_date = fields.DateField()

    class Meta(object):
        model_class = Consent


class ConsentField(ReferenceField):
    model_class = Consent
    serializer_class = ConsentSerializer


class PatientConsentSerializer(PatientMixin, MetaMixin, ModelSerializer):
    consent = ConsentField()
    signed_on_date = fields.DateField()

    class Meta(object):
        model_class = PatientConsent
        exclude = ['consent_id']
