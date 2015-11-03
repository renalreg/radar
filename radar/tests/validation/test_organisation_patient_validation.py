import pytest

from radar.models import Patient, Organisation, OrganisationPatient
from radar.validation.core import ValidationError
from radar.validation.organisation_patients import OrganisationPatientValidation
from helpers.validation import validation_runner


@pytest.fixture
def organisation_patient():
    obj = OrganisationPatient()
    obj.patient = Patient()
    obj.organisation = Organisation()
    obj.is_active = True
    return obj


def test_valid(organisation_patient):
    obj = valid(organisation_patient)
    assert obj.patient is not None
    assert obj.organisation is not None
    assert obj.is_active is True
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_patient_missing(organisation_patient):
    organisation_patient.patient = None
    invalid(organisation_patient)


def test_organisation_missing(organisation_patient):
    organisation_patient.organisation = None
    invalid(organisation_patient)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(OrganisationPatient, OrganisationPatientValidation, obj, **kwargs)
