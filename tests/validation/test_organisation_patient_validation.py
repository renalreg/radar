import pytest

from radar.lib.models import Patient, Organisation, OrganisationPatient
from radar.lib.validation.core import ValidationError
from radar.lib.validation.organisation_patients import OrganisationPatientValidation
from utils import validation_runner


@pytest.fixture
def organisation_patient():
    obj = OrganisationPatient()
    obj.patient = Patient()
    obj.organisation = Organisation()
    return obj


def test_valid(organisation_patient):
    obj = valid(organisation_patient)
    assert obj.patient is not None
    assert obj.organisation is not None


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
