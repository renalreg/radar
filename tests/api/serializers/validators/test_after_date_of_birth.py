from datetime import date, datetime

from cornflake import fields, serializers
from cornflake.exceptions import ValidationError
import pytest
import pytz

from radar.api.serializers.validators import after_date_of_birth
from radar.models.patient_demographics import PatientDemographics
from radar.models.patients import Patient


def test_valid():
    value = run(date(1999, 1, 1), date(2000, 1, 1))
    assert value == date(2000, 1, 1)


def test_no_date_of_birth():
    run(None, date(1999, 1, 1))


def test_less_than():
    with pytest.raises(ValidationError):
        run(date(2000, 1, 1), date(1999, 12, 31))


def test_equal():
    run(date(2000, 1, 1), date(2000, 1, 1))


def test_greater_than():
    run(date(2000, 1, 1), date(2000, 1, 2))


def test_datetime():
    run(date(2000, 1, 1), datetime(2000, 1, 2, tzinfo=pytz.utc))


def run(date_of_birth, value):
    patient = Patient()
    patient_demographics = PatientDemographics()
    patient_demographics.date_of_birth = date_of_birth
    patient.patient_demographics.append(patient_demographics)

    class Serializer(serializers.Serializer):
        patient = fields.Field()
        date = fields.Field()

        class Meta:
            validators = [after_date_of_birth('date')]

    print(patient.earliest_date_of_birth)

    serializer = Serializer(data={
        'patient': patient,
        'date': value
    })

    serializer.is_valid(raise_exception=True)

    return serializer.validated_data['date']
