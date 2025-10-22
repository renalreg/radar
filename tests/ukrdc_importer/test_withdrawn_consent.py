from unittest.mock import MagicMock
import pytest

from radar.models.groups import Group
from radar.models.patients import Patient
from radar.models.groups import GroupPatient
from radar.ukrdc_importer.tasks import withdrawn_consent_cohorts


@pytest.fixture
def mock_patient():
    """Fixture to create a mock patient."""
    patient = MagicMock(spec=Patient)
    patient.groups = []  # matches function logic
    return patient


def make_group_patient(group_id, code, to_date=None):
    """Helper to make a mock GroupPatient with given group and to_date."""
    gp = MagicMock(spec=GroupPatient)
    gp.group = Group(id=group_id, code=code)
    gp.to_date = to_date
    return gp


def test_no_groups(mock_patient):
    """Test case: Patient has no group associations."""
    mock_patient.groups = []
    assert not withdrawn_consent_cohorts(mock_patient)


def test_not_withdrawn_consent(mock_patient):
    """Test case: Patient has groups but none match withdrawn consent criteria."""
    mock_patient.groups = [
        make_group_patient(101, "OTHER"),
        make_group_patient(102, "DIFFERENT"),
    ]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_withdrawn_consent_match_code_only(mock_patient):
    """Test case: Patient has a group matching withdrawn consent code but not ID."""
    mock_patient.groups = [make_group_patient(999, "CONS_WDTWN")]
    assert withdrawn_consent_cohorts(mock_patient)  # ✅ should return True


def test_withdrawn_consent_match_id_only(mock_patient):
    """Test case: Patient has a group matching withdrawn consent ID but not code."""
    mock_patient.groups = [make_group_patient(182, "SOMECODE")]
    assert withdrawn_consent_cohorts(mock_patient)  # ✅ should return True


def test_withdrawn_consent_exact_match(mock_patient):
    """Test case: Patient has a group matching both withdrawn consent code and ID."""
    mock_patient.groups = [make_group_patient(182, "CONS_WDTWN")]
    assert withdrawn_consent_cohorts(mock_patient)


def test_multiple_groups_no_match(mock_patient):
    """Test case: Patient has multiple groups, none of which match withdrawn consent."""
    mock_patient.groups = [
        make_group_patient(101, "OTHER"),
        make_group_patient(200, "ANOTHER"),
    ]
    assert not withdrawn_consent_cohorts(mock_patient)


def test_multiple_groups_with_match(mock_patient):
    """Test case: Patient has multiple groups, one of which matches withdrawn consent."""
    mock_patient.groups = [
        make_group_patient(101, "OTHER"),
        make_group_patient(152, "NOCON"),  # Matches both code and ID
        make_group_patient(200, "ANOTHER"),
    ]
    assert withdrawn_consent_cohorts(mock_patient)
