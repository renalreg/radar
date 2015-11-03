import pytest

from radar.models import Cohort, User, CohortUser
from radar.roles import COHORT_SENIOR_RESEARCHER, COHORT_RESEARCHER
from radar.validation.cohort_users import CohortUserValidation
from radar.validation.core import ValidationError
from helpers.validation import validation_runner


@pytest.fixture
def cohort_user():
    obj = CohortUser()
    obj.user = User(id=1)
    obj.cohort = Cohort(id=1)
    obj.role = COHORT_SENIOR_RESEARCHER
    return obj


def test_valid(cohort_user):
    obj = valid(cohort_user)
    assert obj.user is not None
    assert obj.cohort is not None
    assert obj.role == COHORT_SENIOR_RESEARCHER
    assert obj.created_user is not None
    assert obj.created_date is not None
    assert obj.modified_user is not None
    assert obj.modified_date is not None


def test_user_missing(cohort_user):
    cohort_user.user = None
    invalid(cohort_user)


def test_cohort_missing(cohort_user):
    cohort_user.cohort = None
    invalid(cohort_user)


def test_role_missing(cohort_user):
    cohort_user.role = None
    invalid(cohort_user)


def test_role_invalid(cohort_user):
    cohort_user.role = 'ADMIN'
    invalid(cohort_user)


def test_role_blank(cohort_user):
    cohort_user.role = ''
    invalid(cohort_user)


def test_add_to_cohort():
    cohort = Cohort()

    current_user = User(id=1)
    current_user_cohort_user = CohortUser()
    current_user_cohort_user.cohort = cohort
    current_user_cohort_user.user = current_user
    current_user_cohort_user.role = COHORT_SENIOR_RESEARCHER
    current_user.cohort_users.append(current_user_cohort_user)

    cohort_user = CohortUser()
    cohort_user.cohort = cohort
    cohort_user.user = User()
    cohort_user.role = COHORT_RESEARCHER

    valid(cohort_user, user=current_user)


def test_add_to_another_cohort():
    current_user = User(id=1)
    current_user_cohort_user = CohortUser()
    current_user_cohort_user.cohort = Cohort()
    current_user_cohort_user.user = current_user
    current_user_cohort_user.role = COHORT_SENIOR_RESEARCHER
    current_user.cohort_users.append(current_user_cohort_user)

    cohort_user = CohortUser()
    cohort_user.cohort = Cohort()
    cohort_user.user = User()
    cohort_user.role = COHORT_RESEARCHER

    invalid(cohort_user, user=current_user)


def test_add_to_cohort_not_managed_role():
    cohort = Cohort()

    current_user = User(id=1)
    current_user_cohort_user = CohortUser()
    current_user_cohort_user.cohort = cohort
    current_user_cohort_user.user = current_user
    current_user_cohort_user.role = COHORT_SENIOR_RESEARCHER
    current_user.cohort_users.append(current_user_cohort_user)

    cohort_user = CohortUser()
    cohort_user.cohort = cohort
    cohort_user.user = User()
    cohort_user.role = COHORT_SENIOR_RESEARCHER

    invalid(cohort_user, user=current_user)


def test_remove_own_membership():
    current_user = User()

    old_cohort_user = CohortUser()
    old_cohort_user.cohort = Cohort()
    old_cohort_user.user = current_user
    old_cohort_user.role = COHORT_SENIOR_RESEARCHER
    current_user.cohort_users.append(old_cohort_user)

    new_cohort_user = CohortUser()
    new_cohort_user.cohort = Cohort()
    new_cohort_user.user = User()
    new_cohort_user.role = COHORT_RESEARCHER

    invalid(new_cohort_user, user=current_user, old_obj=old_cohort_user)


def test_update_own_membership():
    current_user = User()
    cohort = Cohort()

    old_cohort_user = CohortUser()
    old_cohort_user.cohort = cohort
    old_cohort_user.user = current_user
    old_cohort_user.role = COHORT_SENIOR_RESEARCHER

    current_user.cohort_users.append(old_cohort_user)

    new_cohort_user = CohortUser()
    new_cohort_user.cohort = cohort
    new_cohort_user.user = current_user
    new_cohort_user.role = COHORT_RESEARCHER

    invalid(new_cohort_user, user=current_user, old_obj=old_cohort_user)


def test_already_in_cohort():
    user = User()
    cohort = Cohort()

    cohort_user1 = CohortUser()
    cohort_user1.user = user
    cohort_user1.cohort = cohort
    cohort_user1.role = COHORT_RESEARCHER
    user.cohort_users.append(cohort_user1)

    cohort_user2 = CohortUser()
    cohort_user2.user = user
    cohort_user2.cohort = cohort
    cohort_user2.role = COHORT_SENIOR_RESEARCHER

    invalid(cohort_user2)


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(CohortUser, CohortUserValidation, obj, **kwargs)
