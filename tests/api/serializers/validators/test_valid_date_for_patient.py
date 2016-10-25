from datetime import date, timedelta

from cornflake import serializers, fields
from cornflake.exceptions import ValidationError
import pytest

from radar.api.serializers.validators import valid_date_for_patient
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient


def test_before_dob():
    with pytest.raises(ValidationError):
        run(date(2000, 1, 1), date(1999, 12, 31))


def test_on_dob():
    value = run(date(2000, 1, 1), date(2000, 1, 1))
    assert value == date(2000, 1, 1)


def test_after_dob():
    value = run(date(2000, 1, 1), date(2000, 1, 2))
    assert value == date(2000, 1, 2)


def test_in_future():
    with pytest.raises(ValidationError):
        run(date(2000, 1, 1), date.today() + timedelta(days=1))


def test_before_day_zero():
    with pytest.raises(ValidationError):
        run(date(1800, 1, 1), date(1899, 12, 31))


def run(date_of_birth, value):
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date_of_birth
    patient.patient_demographics.append(patient_demographics)

    class Serializer(serializers.Serializer):
        patient = fields.Field()
        date = fields.Field()

        class Meta:
            validators = [valid_date_for_patient('date')]

    print patient.earliest_date_of_birth

    serializer = Serializer(data={
        'patient': patient,
        'date': value
    })

    serializer.is_valid(raise_exception=True)

    return serializer.validated_data['date']
