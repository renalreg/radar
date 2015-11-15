import pytest

from radar.models.cohorts import Cohort
from radar.validation.cohorts import CohortValidation
from radar.validation.core import ValidationError
from radar.tests.validation.helpers import validation_runner


@pytest.fixture
def cohort():
    obj = Cohort()
    obj.code = 'HW'
    obj.name = 'Hello World'
    obj.short_name = 'Hi World'
    obj.notes = '<p>Hello!</p>'
    return obj


def test_valid(cohort):
    obj = valid(cohort)

    assert obj.code == 'HW'
    assert obj.name == 'Hello World'
    assert obj.short_name == 'Hi World'
    assert obj.notes == '<p>Hello!</p>'


def test_code_missing(cohort):
    cohort.code = None
    invalid(cohort)


def test_code_blank(cohort):
    cohort.code = ''
    invalid(cohort)


def test_name_missing(cohort):
    cohort.name = None
    invalid(cohort)


def test_name_blank(cohort):
    cohort.name = ''
    invalid(cohort)


def test_short_name_missing(cohort):
    cohort.short_name = None
    invalid(cohort)


def test_short_name_blank(cohort):
    cohort.short_name = ''
    invalid(cohort)


def test_notes_missing(cohort):
    cohort.notes = None
    obj = valid(cohort)
    assert obj.notes is None


def test_notes_blank(cohort):
    cohort.notes = ''
    obj = valid(cohort)
    assert obj.notes is None


def test_notes_sanitize_html(cohort):
    cohort.notes = '<script>alert("Hi")</script>'
    obj = valid(cohort)
    assert obj.notes == '&lt;script&gt;alert("Hi")&lt;/script&gt;'


def invalid(obj, **kwargs):
    with pytest.raises(ValidationError) as e:
        valid(obj, **kwargs)

    return e


def valid(obj, **kwargs):
    return validation_runner(Cohort, CohortValidation, obj, **kwargs)
