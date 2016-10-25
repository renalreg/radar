from datetime import date, timedelta

from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.genetics import GeneticsSerializer
from radar.exceptions import PermissionDenied
from radar.models.groups import Group, GroupPatient, GROUP_TYPE
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.users import User


@pytest.fixture
def group():
    return Group(type=GROUP_TYPE.COHORT)


@pytest.fixture
def patient(group):
    patient = Patient()

    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)

    group_patient = GroupPatient()
    group_patient.group = group
    group_patient.patient = patient

    return patient


@pytest.fixture
def genetics(patient, group):
    return {
        'patient': patient,
        'group': group,
        'date_sent': date(2015, 1, 2),
        'laboratory': 'Test',
        'reference_number': '12345',
        'karyotype': 1,
        'results': 'foo\nbar\nbaz',
        'summary': 'hello\nworld'
    }


def test_valid(genetics):
    obj = valid(genetics)
    assert obj.date_sent == date(2015, 1, 2)
    assert obj.laboratory == 'Test'
    assert obj.reference_number == '12345'
    assert obj.karyotype == 1
    assert obj.results == 'foo\nbar\nbaz'
    assert obj.summary == 'hello\nworld'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(genetics):
    genetics['patient'] = None
    invalid(genetics)


def test_group_none(genetics):
    genetics['group'] = None
    invalid(genetics)


def test_group_not_cohort(genetics):
    genetics['group'].type = GROUP_TYPE.OTHER

    with pytest.raises(PermissionDenied):
        valid(genetics)


def test_date_sent_none(genetics):
    genetics['date_sent'] = None
    invalid(genetics)


def test_date_sent_future(genetics):
    genetics['date_sent'] = date.today() + timedelta(days=1)
    invalid(genetics)


def test_date_sent_before_dob(genetics):
    genetics['date_sent'] = date(1999, 12, 31)
    invalid(genetics)


def test_laboratory_blank(genetics):
    genetics['laboratory'] = ''
    obj = valid(genetics)
    assert obj.laboratory is None


def test_reference_number_blank(genetics):
    genetics['reference_number'] = ''
    obj = valid(genetics)
    assert obj.reference_number is None


def test_karyotype_none(genetics):
    genetics['karyotype'] = None
    obj = valid(genetics)
    assert obj.karyotype is None


def test_karyotype_invalid(genetics):
    genetics['karyotype'] = 99999
    invalid(genetics)


def test_results_blank(genetics):
    genetics['results'] = ''
    obj = valid(genetics)
    assert obj.results is None


def test_summary_blank(genetics):
    genetics['summary'] = ''
    obj = valid(genetics)
    assert obj.summary is None


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = GeneticsSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
