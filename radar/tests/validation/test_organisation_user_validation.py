import pytest

from radar.models import User, OrganisationUser, Organisation
from radar.roles import ORGANISATION_SENIOR_CLINICIAN, ORGANISATION_CLINICIAN
from radar.validation.core import ValidationError
from radar.validation.organisation_users import OrganisationUserValidation
from helpers.validation import validation_runner


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
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


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


def test_add_to_organisation():
    organisation = Organisation()

    current_user = User(id=1)
    current_user_organisation_user = OrganisationUser()
    current_user_organisation_user.organisation = organisation
    current_user_organisation_user.user = current_user
    current_user_organisation_user.role = ORGANISATION_SENIOR_CLINICIAN
    current_user.organisation_users.append(current_user_organisation_user)

    organisation_user = OrganisationUser()
    organisation_user.organisation = organisation
    organisation_user.organisation = organisation
    organisation_user.user = User()
    organisation_user.role = ORGANISATION_CLINICIAN

    valid(organisation_user, user=current_user)


def test_add_to_another_organisation():
    current_user = User(id=1)
    current_user_organisation_user = OrganisationUser()
    current_user_organisation_user.organisation = Organisation()
    current_user_organisation_user.user = current_user
    current_user_organisation_user.role = ORGANISATION_SENIOR_CLINICIAN
    current_user.organisation_users.append(current_user_organisation_user)

    organisation_user = OrganisationUser()
    organisation_user.organisation = Organisation()
    organisation_user.user = User()
    organisation_user.role = ORGANISATION_CLINICIAN

    invalid(organisation_user, user=current_user)


def test_add_to_organisation_not_managed_role():
    organisation = Organisation()

    current_user = User(id=1)
    current_user_organisation_user = OrganisationUser()
    current_user_organisation_user.organisation = organisation
    current_user_organisation_user.user = current_user
    current_user_organisation_user.role = ORGANISATION_SENIOR_CLINICIAN
    current_user.organisation_users.append(current_user_organisation_user)

    organisation_user = OrganisationUser()
    organisation_user.organisation = organisation
    organisation_user.user = User()
    organisation_user.role = ORGANISATION_SENIOR_CLINICIAN

    invalid(organisation_user, user=current_user)


def test_remove_own_membership():
    current_user = User()

    old_organisation_user = OrganisationUser()
    old_organisation_user.organisation = Organisation()
    old_organisation_user.user = current_user
    old_organisation_user.role = ORGANISATION_SENIOR_CLINICIAN
    current_user.organisation_users.append(old_organisation_user)

    new_organisation_user = OrganisationUser()
    new_organisation_user.organisation = Organisation()
    new_organisation_user.user = User()
    new_organisation_user.role = ORGANISATION_CLINICIAN

    invalid(new_organisation_user, user=current_user, old_obj=old_organisation_user)


def test_update_own_membership():
    current_user = User()
    organisation = Organisation()

    old_organisation_user = OrganisationUser()
    old_organisation_user.organisation = organisation
    old_organisation_user.user = current_user
    old_organisation_user.role = ORGANISATION_SENIOR_CLINICIAN

    current_user.organisation_users.append(old_organisation_user)

    new_organisation_user = OrganisationUser()
    new_organisation_user.organisation = organisation
    new_organisation_user.user = current_user
    new_organisation_user.role = ORGANISATION_CLINICIAN

    invalid(new_organisation_user, user=current_user, old_obj=old_organisation_user)


def test_already_in_organisation():
    user = User()
    organisation = Organisation()

    organisation_user1 = OrganisationUser()
    organisation_user1.user = user
    organisation_user1.organisation = organisation
    organisation_user1.role = ORGANISATION_SENIOR_CLINICIAN
    user.organisation_users.append(organisation_user1)

    organisation_user2 = OrganisationUser()
    organisation_user2.user = user
    organisation_user2.organisation = organisation
    organisation_user2.role = ORGANISATION_CLINICIAN

    invalid(organisation_user2)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(OrganisationUser, OrganisationUserValidation, obj, **kwargs)
