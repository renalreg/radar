import pytest

from radar.lib.models import User, OrganisationUser, Organisation
from radar.lib.roles import ORGANISATION_SENIOR_CLINICIAN
from radar.lib.validation.core import ValidationError
from radar.lib.validation.organisation_users import OrganisationUserValidation
from utils import validation_runner


@pytest.fixture
def organisation_user():
    obj = OrganisationUser()
    obj.user = User()
    obj.organisation = Organisation()
    obj.role = ORGANISATION_SENIOR_CLINICIAN
    return obj


def test_valid(organisation_user):
    obj = valid(organisation_user)
    assert obj.user is not None
    assert obj.organisation is not None
    assert obj.role == ORGANISATION_SENIOR_CLINICIAN


def test_user_missing(organisation_user):
    organisation_user.user = None
    invalid(organisation_user)


def test_organisation_missing(organisation_user):
    organisation_user.organisation = None
    invalid(organisation_user)


def test_role_missing(organisation_user):
    organisation_user.role = None
    invalid(organisation_user)


def test_role_invalid(organisation_user):
    organisation_user.role = 'SENIOR_RESEARCHER'
    invalid(organisation_user)


def test_role_blank(organisation_user):
    organisation_user.role = ''
    invalid(organisation_user)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(OrganisationUser, OrganisationUserValidation, obj, **kwargs)
