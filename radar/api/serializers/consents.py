from cornflake import fields
from cornflake.sqlalchemy_orm import ModelSerializer, ReferenceField
from cornflake.validators import not_in_future


from radar.api.serializers.common import (
    MetaMixin,
    PatientMixin,
)
from radar.exceptions import PermissionDenied
from radar.models.consents import Consent, CONSENT_TYPE, PatientConsent
from radar.models.patients import Patient
from radar.permissions import has_permission_for_patient
from radar.roles import PERMISSION
from radar.variants import pick


class ConsentSerializer(ModelSerializer):
    code = fields.StringField()
    label = fields.StringField()
    paediatric = fields.BooleanField(default=False)
    from_date = fields.DateField()
    consent_type = fields.EnumField(CONSENT_TYPE)
    weight = fields.IntegerField()

    class Meta:
        model_class = Consent


class ConsentField(ReferenceField):
    model_class = Consent
    serializer_class = ConsentSerializer


class PatientConsentField(ReferenceField):
    model_class = Patient

    def validate(self, patient):
        user = self.context["user"]

        if not has_permission_for_patient(user, patient, PERMISSION.EDIT_CONSENT):
            raise PermissionDenied()

        return patient


class PatientConsentMixin(PatientMixin):
    patient = PatientConsentField()


class BasePatientConsentSerializer(PatientConsentMixin, MetaMixin, ModelSerializer):
    """Fields shared by every deployment."""

    consent = ConsentField()
    signed_on_date = fields.DateField()
    withdrawn_on_date = fields.DateField(required=False)

    class Meta:
        model_class = PatientConsent
        exclude = ["consent_id"]


class MainPatientConsentSerializer(BasePatientConsentSerializer):
    signed_on_date = fields.DateField(validators=[not_in_future()])
    reconsent_letter_sent_date = fields.DateField(
        required=False, validators=[not_in_future()]
    )
    reconsent_letter_returned_date = fields.DateField(
        required=False, validators=[not_in_future()]
    )

    def validate(self, serial_data):
        # Validating reconsent letter sent and returned dates make sense
        signed = serial_data["signed_on_date"]
        sent = serial_data["reconsent_letter_sent_date"]
        returned = serial_data["reconsent_letter_returned_date"]
        errors_dict = {}

        if sent and sent < signed:
            errors_dict["reconsent_letter_sent_date"] = "Signed on date after sent date!"

        if returned and returned < signed:
            errors_dict["reconsent_letter_returned_date"] = (
                "Signed on date after return date!"
            )

        if sent and returned and sent > returned:
            errors_dict["reconsent_letter_sent_date"] = "Sent date after return date!"

        if errors_dict:
            raise fields.ValidationError(errors_dict)

        return serial_data


class InternationalPatientConsentSerializer(BasePatientConsentSerializer):
    pass


PatientConsentSerializer:type[MainPatientConsentSerializer] | type[InternationalPatientConsentSerializer] = pick(
    main=MainPatientConsentSerializer,
    international=InternationalPatientConsentSerializer,
)
