from datetime import date, timedelta

import pytest
from cornflake.exceptions import ValidationError

from radar.api.serializers.hospitalisations import HospitalisationSerializer
from radar.models.groups import Group
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient
from radar.models.source_types import SOURCE_TYPE_RADAR
from radar.models.users import User


@pytest.fixture
def patient():
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date(2000, 1, 1)
    patient.patient_demographics.append(patient_demographics)
    return patient


@pytest.fixture
def hospitalisation(patient):
    return {
        'source_group': Group(),
        'source_type': SOURCE_TYPE_RADAR,
        'patient': patient,
        'date_of_admission': date(2015, 1, 1),
        'date_of_discharge': date(2015, 1, 2),
        'reason_for_admission': 'Foo',
        'comments': 'Bar'
    }


def test_valid(hospitalisation):
    obj = valid(hospitalisation)
    assert obj.date_of_admission == date(2015, 1, 1)
    assert obj.date_of_discharge == date(2015, 1, 2)
    assert obj.reason_for_admission == 'Foo'
    assert obj.comments == 'Bar'
    assert obj.created_date is not None
    assert obj.modified_date is not None
    assert obj.created_user is not None
    assert obj.modified_user is not None


def test_patient_none(hospitalisation):
    hospitalisation['patient'] = None
    invalid(hospitalisation)


def test_source_group_none(hospitalisation):
    hospitalisation['source_group'] = None
    invalid(hospitalisation)


def test_source_type_none(hospitalisation):
    hospitalisation['source_type'] = None
    hospitalisation = valid(hospitalisation)
    assert hospitalisation.source_type == 'RADAR'


def test_date_of_admission_none(hospitalisation):
    hospitalisation['date_of_admission'] = None
    invalid(hospitalisation)


def test_date_of_admission_before_dob(hospitalisation):
    hospitalisation['date_of_admission'] = date(1999, 1, 1)
    invalid(hospitalisation)


def test_date_of_admission_future(hospitalisation):
    hospitalisation['date_of_admission'] = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_date_of_discharge_none(hospitalisation):
    hospitalisation['date_of_discharge'] = None
    valid(hospitalisation)


def test_date_of_discharge_before_dob(hospitalisation):
    hospitalisation['date_of_discharge'] = date(1999, 1, 1)
    invalid(hospitalisation)


def test_date_of_discharge_future(hospitalisation):
    hospitalisation['date_of_discharge'] = date.today() + timedelta(days=1)
    invalid(hospitalisation)


def test_date_of_discharge_before_date_of_admission(hospitalisation):
    hospitalisation['date_of_discharge'] = hospitalisation['date_of_admission'] - timedelta(days=1)
    invalid(hospitalisation)


def test_reason_for_admission_none(hospitalisation):
    hospitalisation['reason_for_admission'] = None
    valid(hospitalisation)


def test_reason_for_admission_blank(hospitalisation):
    hospitalisation['reason_for_admission'] = ''
    obj = valid(hospitalisation)
    assert obj.reason_for_admission is None


def test_comments_none(hospitalisation):
    hospitalisation['comments'] = None
    valid(hospitalisation)


def test_comments_blank(hospitalisation):
    hospitalisation['comments'] = ''
    obj = valid(hospitalisation)
    assert obj.comments is None


def invalid(data):
    with pytest.raises(ValidationError) as e:
        valid(data)

    return e


def valid(data):
    serializer = HospitalisationSerializer(data=data, context={'user': User(is_admin=True)})
    serializer.is_valid(raise_exception=True)
    return serializer.save()
