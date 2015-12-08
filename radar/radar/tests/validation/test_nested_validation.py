import pytest

from radar.validation.validators import required, min_length
from radar.validation.core import Validation, Field, ValidationError, ListField


class GreetingValidation(Validation):
    message = Field([required()])


class FooValidation(Validation):
    bar = Field([required()])
    greeting = GreetingValidation([required()])


class BarValidation(Validation):
    greetings = ListField(GreetingValidation(), [required(), min_length(3)])


def test_parent_error():
    with pytest.raises(ValidationError) as e:
        validate(FooValidation, {})

    assert e.value.errors == {
        'bar': ['This field is required.'],
        'greeting': {
            '_': ['This field is required.']
        }
    }


def test_child_error():
    with pytest.raises(ValidationError) as e:
        validate(FooValidation, {'bar': 42, 'greeting': {}})

    assert e.value.errors == {
        'greeting': {
            'message': ['This field is required.'],
        },
    }


def test_parent_and_child_error():
    with pytest.raises(ValidationError) as e:
        validate(BarValidation, {'greetings': [{}]})

    assert e.value.errors == {
        'greetings': {
            '_': ['Value is too short (min length is 3 characters).'],
        },
    }


def validate(validation_class, obj):
    validation = validation_class()
    old_obj = {}
    ctx = {}
    validation.before_update(ctx, old_obj)
    old_obj = validation.clone(old_obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
