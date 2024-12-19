from unittest.mock import MagicMock

import pytest

from radar.models.groups import Group
from radar.models.patients import Patient
from radar.ukrdc_importer.tasks import withdrawn_consent_cohorts

@pytest.fixture
def mock_patient():
    """Fixture to create a mock patient."""
    patient = MagicMock(spec=Patient)
    patient.cohorts = []
    return patient


def test_no_cohorts(mock_patient):
    """Test case: Patient has no cohorts."""
    mock_patient.cohorts = []
    assert not withdrawn_consent_cohorts(mock_patient)


def test_not_withdrawn_consent(mock_patient):
    """Test case: Patient has cohorts but none match withdrawn consent criteria."""
    mock_patient.cohorts = [
        Group(id=101, code="OTHER"),
        Group(id=102, code="DIFFERENT"),
    ]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_withdrawn_consent_match_code_only(mock_patient):
    """Test case: Patient has a cohort matching withdrawn consent code but not ID."""
    mock_patient.cohorts = [Group(id=999, code="CONS_WDTWN")]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_withdrawn_consent_match_id_only(mock_patient):
    """Test case: Patient has a cohort matching withdrawn consent ID but not code."""
    mock_patient.cohorts = [Group(id=182, code="SOMECODE")]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_withdrawn_consent_exact_match(mock_patient):
    """Test case: Patient has a cohort matching both withdrawn consent code and ID."""
    mock_patient.cohorts = [Group(id=182, code="CONS_WDTWN")]
    assert withdrawn_consent_cohorts(mock_patient)


def test_multiple_cohorts_no_match(mock_patient):
    """Test case: Patient has multiple cohorts, none of which match withdrawn consent."""
    mock_patient.cohorts = [
        Group(id=101, code="OTHER"),
        Group(id=200, code="ANOTHER"),
    ]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_multiple_cohorts_with_match(mock_patient):
    """Test case: Patient has multiple cohorts, one of which matches withdrawn consent."""
    mock_patient.cohorts = [
        Group(id=101, code="OTHER"),
        Group(id=152, code="NOCON"),  # Matches both code and ID
        Group(id=200, code="ANOTHER"),
    ]
    assert withdrawn_consent_cohorts(mock_patient)
