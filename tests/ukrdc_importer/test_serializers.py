from cornflake.exceptions import ValidationError

from radar.ukrdc_importer.serializers import PatientNumberSerializer


def test_number_validator_works_correctly():
    data = {
        'number': '1111111111',
        'number_type': 'NHS',
        'organization': {'code': 'nhs', 'description': 'nhs desc'}
    }
    serializer = PatientNumberSerializer(data=data)
    assert serializer.is_valid()


def test_number_validator_doesnt_check_non_nhs():
    data = {
        'number': '111111',
        'number_type': 'RADAR',
        'organization': {'code': 'nhs', 'description': 'nhs desc'}
    }
    serializer = PatientNumberSerializer(data=data)
    assert serializer.is_valid()


def test_number_validator_invalid_nhs_number():
    data = {
        'number': '111111',
        'number_type': 'CHI',
        'organization': {'code': 'nhs', 'description': 'nhs desc'}
    }
    serializer = PatientNumberSerializer(data=data)
    assert serializer.is_valid() is False
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        assert 'Not a valid CHI number' in exc.errors['number'][0]
        # assert 'Not a valid CHI number' in exc.args[0]['number'][0]
