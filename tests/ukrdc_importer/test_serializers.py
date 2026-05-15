from cornflake.exceptions import ValidationError

from radar.ukrdc_importer.serializers import PatientNumberSerializer, StringOrCodeDescriptionSerializer, \
    AddressSerializer


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

def test_string_or_code_description_serializer():
    serializer = StringOrCodeDescriptionSerializer(data="London")
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == {
        "code": "London", "description": None
    }

    serializer = StringOrCodeDescriptionSerializer(data={
        "code": "LON"
    })
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == {
        "code": "LON", "description": None
    }

    serializer = StringOrCodeDescriptionSerializer(data={
        "description": "London"
    })
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == {
        "code": None, "description": "London"
    }

    serializer = StringOrCodeDescriptionSerializer(data={
        "code": "LON",
        "description": "London"
    })
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == {
        "code": "LON",
        "description": "London"
    }

    serializer = StringOrCodeDescriptionSerializer(data={})
    assert not serializer.is_valid()


    serializer = AddressSerializer(data={
        "street": "221B Baker Street",
        "city": "London",
        "state": {
            "code": "LN"
        },
        "country": {
            "code": "GB",
            "description": "United Kingdom"
        },
        "zip": {
            "code": "NW1"
        }
    })

    assert serializer.is_valid(), serializer.errors

    assert serializer.validated_data == {
        "street": "221B Baker Street",
        "city": {
            "code": "London",
            "description": None
        },
        'from_time': None,
        "state": {
            "code": "LN",
            "description": None
        },
        "country": {
            "code": "GB",
            "description": "United Kingdom"
        },
        'to_time': None,
        "zip": {
            "code": "NW1",
            "description": None
        }
    }
