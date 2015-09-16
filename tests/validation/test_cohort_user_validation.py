import pytest

from radar.lib.models import Cohort, User, CohortUser
from radar.lib.roles import COHORT_SENIOR_RESEARCHER
from radar.lib.validation.cohort_users import CohortUserValidation
from radar.lib.validation.core import ValidationError
from utils import validation_runner


@pytest.fixture
def cohort_user():
    obj = CohortUser()
    obj.user = User()
    obj.cohort = Cohort()
    obj.role = COHORT_SENIOR_RESEARCHER
    return obj


def test_valid(cohort_user):
    obj = valid(cohort_user)
    assert obj.user is not None
    assert obj.cohort is not None
    assert obj.role == COHORT_SENIOR_RESEARCHER


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


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(CohortUser, CohortUserValidation, obj, **kwargs)
