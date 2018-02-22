from datetime import date
from mock import MagicMock
from radar.models.results import OBSERVATION_VALUE_TYPE, Result


def make_patient(years=48, gender='F', race='P'):
    patient = MagicMock()
    patient.to_age.return_value = 12 * years
    patient.is_female = True if gender == 'F' else False
    patient.is_male = True if gender == 'M' else False
    patient.ethnicity = MagicMock()
    patient.ethnicity.code = race
    return patient


def make_observation(short_name='creatinine'):
    observation = MagicMock()
    observation.short_name = short_name
    observation.value_type = OBSERVATION_VALUE_TYPE.REAL
    return observation


def make_result(creat_value, result_date, patient, observation):
    result = Result()
    result.value = creat_value
    result.patient = patient
    result.observation = observation
    result.date = result_date
    return result


def test_non_numeric_value_doesnt_throw_error():
    result = make_result('see comments', date(2018, 2, 22), make_patient(), make_observation('phos'))
    assert result.egfr_calculated == ''


def test_non_creatinine_returns_empty_string():
    result = make_result(10, date(2018, 2, 22), make_patient(), make_observation('phos'))
    assert result.egfr_calculated == ''


def test_nonblack_female_correctly_calculates():
    result = make_result(285, date(2018, 2, 22), make_patient(48, 'F', 'A'), make_observation())
    assert round(result.egfr_calculated) == 16


def test_black_female_correctly_calculates():
    result = make_result(285, date(2018, 2, 22), make_patient(48, 'F', 'M'), make_observation())
    assert round(result.egfr_calculated) == 19


def test_nonblack_male_correctly_calculates():
    result = make_result(285, date(2018, 2, 22), make_patient(48, 'M', 'A'), make_observation())
    assert round(result.egfr_calculated) == 22


def test_black_male_correctly_calculates():
    result = make_result(285, date(2018, 2, 22), make_patient(48, 'M', 'P'), make_observation())
    assert round(result.egfr_calculated) == 25


def test_nonblack_female_correctly_calculates_with_low_creat():
    result = make_result(60, date(2018, 2, 22), make_patient(48, 'F', 'A'), make_observation())
    assert round(result.egfr_calculated) == 104


def test_black_female_correctly_calculates_with_low_creat():
    result = make_result(60, date(2018, 2, 22), make_patient(48, 'F', 'M'), make_observation())
    assert round(result.egfr_calculated) == 120


def test_nonblack_male_correctly_calculates_with_low_creat():
    result = make_result(60, date(2018, 2, 22), make_patient(48, 'M', 'A'), make_observation())
    assert round(result.egfr_calculated) == 113


def test_black_male_correctly_calculates_with_low_creat():
    result = make_result(60, date(2018, 2, 22), make_patient(48, 'M', 'P'), make_observation())
    assert round(result.egfr_calculated) == 131
