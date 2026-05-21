import pytest
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

class TestStringOrCodeDescriptionSerializer:
    """Unit tests for StringOrCodeDescriptionSerializer."""

    def test_plain_string_input_maps_to_code_field(self):
        serializer = StringOrCodeDescriptionSerializer(data="London")

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {"code": "London", "description": None}

    def test_code_only_dict_input(self):
        serializer = StringOrCodeDescriptionSerializer(data={"code": "LON"})

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {"code": "LON", "description": None}

    def test_description_only_dict_input(self):
        serializer = StringOrCodeDescriptionSerializer(data={"description": "London"})

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {"code": None, "description": "London"}

    def test_code_and_description_dict_input(self):
        serializer = StringOrCodeDescriptionSerializer(
            data={"code": "LON", "description": "London"}
        )

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {"code": "LON", "description": "London"}

    def test_empty_dict_input_is_invalid(self):
        serializer = StringOrCodeDescriptionSerializer(data={})

        assert not serializer.is_valid()


class TestAddressSerializer:
    """Unit tests for AddressSerializer."""

    @pytest.fixture
    def full_address_payload(self):
        return {
            "street": "Baker Street",
            "city": "London",
            "state": {"code": "LN"},
            "country": {"code": "GB", "description": "United Kingdom"},
            "zip": {"code": "NW1"},
        }

    def test_valid_address_with_mixed_field_formats(self, full_address_payload):
        serializer = AddressSerializer(data=full_address_payload)

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "street": "Baker Street",
            "city": {"code": "London", "description": None},
            "state": {"code": "LN", "description": None},
            "country": {"code": "GB", "description": "United Kingdom"},
            "zip": {"code": "NW1", "description": None},
            "from_time": None,
            "to_time": None,
        }

    def test_run_validation_with_blank_and_none_fields(self, full_address_payload):
        payload = {
            "street": "Baker Street",
            "city": "",
            "state": "  ",
            "country": None,
            "zip": {"code": "NW1", "description": None},
            "from_time": None,
            "to_time": None,
        }
        serializer = AddressSerializer(data=full_address_payload)
        serializer.is_valid()

        result = serializer.run_validation(payload)

        # Assert the shape of the result once expected behaviour is known
        assert result is not None
        assert result["state"] is None

    def test_valid_address_with_multi_word_city_and_state(self):
        serializer = AddressSerializer(data={
            "street": "Baker Street",
            "city": "New York",
            "state": "New York",
            "country": {"code": "US", "description": "United States"},
            "zip": {"code": "10001"},
        })

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {
            "street": "Baker Street",
            "city": {"code": "New York", "description": None},
            "state": {"code": "New York", "description": None},
            "country": {"code": "US", "description": "United States"},
            "zip": {"code": "10001", "description": None},
            "from_time": None,
            "to_time": None,
        }

