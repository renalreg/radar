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


class PatientConsentField(ReferenceField):
    model_class = Patient

    def validate(self, patient):
        user = self.context['user']

        if not has_permission_for_patient(user, patient, PERMISSION.EDIT_CONSENT):
            raise PermissionDenied()

        return patient


class PatientConsentMixin(PatientMixin):
    patient = PatientConsentField()


class PatientConsentSerializer(PatientConsentMixin, MetaMixin, ModelSerializer):
    consent = ConsentField()
    signed_on_date = fields.DateField(validators=[not_in_future()])
    withdrawn_on_date = fields.DateField(required=False)
    reconsent_letter_sent_date = fields.DateField(required=False, validators=[not_in_future()])
    reconsent_letter_returned_date = fields.DateField(required=False, validators=[not_in_future()])

    class Meta(object):
        model_class = PatientConsent
        exclude = ['consent_id']

    def validate(self, serial_data):
        # Validating reconsent letter sent and returned dates make sense
        errors_dict = {}

        if serial_data['reconsent_letter_sent_date']:

            if serial_data['reconsent_letter_sent_date'] < serial_data['signed_on_date']:
                errors_dict['reconsent_letter_sent_date'] = "Signed on date after sent date!"
            if serial_data['reconsent_letter_returned_date']:
                if serial_data['reconsent_letter_sent_date'] > serial_data['reconsent_letter_returned_date']:
                    errors_dict['reconsent_letter_sent_date'] = "Signed on date after sent date!"

        if serial_data['reconsent_letter_returned_date']:

            if serial_data['reconsent_letter_returned_date'] < serial_data['signed_on_date']:
                errors_dict['reconsent_letter_returned_date'] = "Signed on date after return date!"
            if serial_data['reconsent_letter_sent_date']:
                if serial_data['reconsent_letter_sent_date'] > serial_data['reconsent_letter_returned_date']:
                    errors_dict['reconsent_letter_sent_date'] = "Sent date after return date!"

        if errors_dict:
            raise fields.ValidationError(errors_dict)

        return serial_data
