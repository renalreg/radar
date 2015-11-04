import pytest

from radar.validation.core import SkipField, ValidatorCall, pass_full, run_validators, Result, ValidationError


class MockFunction(object):
    def __init__(self):
        self.args = None

    def __call__(self, *args):
        self.args = args
        return 42


class MockSkipFunction(object):
    def __init__(self):
        self.args = None

    def __call__(self, *args):
        self.args = args
        raise SkipField()


class MockErrorFunction(object):
    def __init__(self):
        self.args = None

    def __call__(self, *args):
        self.args = args
        raise ValidationError('An error!')


def test_run_validators_empty_list():
    old_value = object()
    new_value = object()
    ctx = {}

    c = ValidatorCall(ctx, old_value)
    assert run_validators([], c, new_value) == new_value


def test_run_validators():
    old_value = object()
    new_value = object()
    ctx = {}

    fs = []

    for _ in range(3):
        f = MockFunction()
        pass_full(f)
        fs.append(f)

    c = ValidatorCall(ctx, old_value)
    assert run_validators(fs, c, new_value) == 42

    for i, f in enumerate(fs):
        assert f.args[0] is ctx
        assert f.args[1] is c
        assert f.args[2] is old_value

        if i == 0:
            assert f.args[3] is new_value
        else:
            assert f.args[3] == 42

        assert len(f.args) == 4


def test_run_validators_skip():
    old_value = object()
    new_value = object()
    ctx = {}

    fs = []

    for i in range(5):
        if i == 2:
            f = MockSkipFunction()
        else:
            f = MockFunction()

        pass_full(f)
        fs.append(f)

    c = ValidatorCall(ctx, old_value)
    r = Result()
    assert run_validators(fs, c, new_value, r) == 42
    assert r.skipped

    for i, f in enumerate(fs):
        if i <= 2:
            assert f.args[0] is ctx
            assert f.args[1] is c
            assert f.args[2] is old_value

            if i == 0:
                assert f.args[3] is new_value
            else:
                assert f.args[3] == 42
        else:
            assert f.args is None


def test_run_validators_skip():
    old_value = object()
    new_value = object()
    ctx = {}

    fs = []

    for i in range(5):
        if i == 2:
            f = MockErrorFunction()
        else:
            f = MockFunction()

        pass_full(f)
        fs.append(f)

    c = ValidatorCall(ctx, old_value)
    r = Result()

    with pytest.raises(ValidationError) as e:
        run_validators(fs, c, new_value)

    assert e.value.errors == ['An error!']

    for i, f in enumerate(fs):
        if i <= 2:
            assert f.args[0] is ctx
            assert f.args[1] is c
            assert f.args[2] is old_value

            if i == 0:
                assert f.args[3] is new_value
            else:
                assert f.args[3] == 42
        else:
            assert f.args is None
