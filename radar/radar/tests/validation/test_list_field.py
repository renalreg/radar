import pytest

from radar.validation.core import ListField, Validation, Field, ValidationError
from radar.validation.validators import required


class BarValidation(Validation):
    bar = Field([required()])


class FooValidation(Validation):
    foo = ListField(BarValidation(), [required()])


def test_missing():
    with pytest.raises(ValidationError) as e:
        validate(FooValidation(), {})

    assert e.value.errors == {
        'foo': {
            '_': ['This field is required.']
        }
    }


def test_empty():
    obj = {'foo': []}
    new_obj = validate(FooValidation(), obj)
    assert new_obj == obj


def test_list():
    obj = {'foo': [{'bar': 'hello'}, {'bar': 'world'}]}
    new_obj = validate(FooValidation(), obj)
    assert new_obj == obj


def test_error_in_list():
    obj = {'foo': [{'bar': 'hello'}, {}]}

    with pytest.raises(ValidationError) as e:
        validate(FooValidation(), obj)

    assert e.value.errors == {
        'foo': {
            1: {
                'bar': ['This field is required.']
            }
        }
    }


def validate(validation, obj):
    old_obj = {}
    ctx = {}
    validation.before_update(ctx, old_obj)
    old_obj = validation.clone(old_obj)
    obj = validation.after_update(ctx, old_obj, obj)
    return obj
