from radar.validation.core import ContextBeforeUpdateCall, pass_call, pass_full, pass_old_obj, ContextCall, pass_new_obj, \
    pass_context, ValidatorCall, pass_old_value, PreValidateCall, ValidateBeforeUpdateCall, ValidateCall, \
    ValidateFieldBeforeUpdateCall, ValidateFieldCall


class MockFunction(object):
    def __init__(self):
        self.args = []

    def __call__(self, *args):
        self.args = args
        return 42


def test_context_before_update_call():
    old_obj = object()
    ctx = {}
    f = MockFunction()

    c = ContextBeforeUpdateCall(old_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert len(f.args) == 1


def test_context_before_update_call_with_call():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ContextBeforeUpdateCall(old_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert len(f.args) == 2


def test_context_before_update_call_with_old_obj():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = ContextBeforeUpdateCall(old_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is old_obj
    assert len(f.args) == 2


def test_context_before_update_call_with_full():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ContextBeforeUpdateCall(old_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert len(f.args) == 3


def test_context_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()

    c = ContextCall(old_obj, new_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert len(f.args) == 1


def test_context_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ContextCall(old_obj, new_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert len(f.args) == 2


def test_context_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = ContextCall(old_obj, new_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is old_obj
    assert len(f.args) == 2


def test_context_call_with_new_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_new_obj(f)

    c = ContextCall(old_obj, new_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_context_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ContextCall(old_obj, new_obj)
    c(f, ctx)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert f.args[3] is new_obj
    assert len(f.args) == 4


def test_validator_call():
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()

    c = ValidatorCall(ctx, old_value)
    c(f, new_value)

    assert f.args[0] is new_value
    assert len(f.args) == 1


def test_validator_call_with_context():
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = ValidatorCall(ctx, old_value)
    c(f, new_value)

    assert f.args[0] is ctx
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validator_call_with_call():
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ValidatorCall(ctx, old_value)
    c(f, new_value)

    assert f.args[0] is c
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validator_call_with_old_value():
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_old_value(f)

    c = ValidatorCall(ctx, old_value)
    c(f, new_value)

    assert f.args[0] is old_value
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validator_call_with_full():
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ValidatorCall(ctx, old_value)
    c(f, new_value)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_value
    assert f.args[3] is new_value
    assert len(f.args) == 4


def test_pre_validate_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()

    c = PreValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is new_obj
    assert len(f.args) == 1


def test_pre_validate_call_with_context():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = PreValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is ctx
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_pre_validate_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = PreValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is c
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_pre_validate_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = PreValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is old_obj
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_pre_validate_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = PreValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert f.args[3] is new_obj
    assert len(f.args) == 4


def test_validate_before_update_call():
    old_obj = object()
    ctx = {}
    f = MockFunction()

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(f)

    assert f.args[0] is old_obj
    assert len(f.args) == 1


def test_validate_before_update_call_with_context():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(f)

    assert f.args[0] is ctx
    assert f.args[1] is old_obj
    assert len(f.args) == 2


def test_validate_before_update_call_with_call():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(f)

    assert f.args[0] is c
    assert f.args[1] is old_obj
    assert len(f.args) == 2


def test_validate_before_update_call_with_full():
    old_obj = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(f)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert len(f.args) == 3


def test_validate_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()

    c = ValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is new_obj
    assert len(f.args) == 1


def test_validate_call_with_context():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = ValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is ctx
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_validate_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is c
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_validate_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = ValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is old_obj
    assert f.args[1] is new_obj
    assert len(f.args) == 2


def test_validate_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ValidateCall(ctx, old_obj)
    c(f, new_obj)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert f.args[3] is new_obj
    assert len(f.args) == 4


def test_validate_field_before_update_call():
    old_obj = object()
    old_value = object()
    ctx = {}
    f = MockFunction()

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(f)

    assert f.args[0] is old_value
    assert len(f.args) == 1


def test_validate_field_before_update_call_with_context():
    old_obj = object()
    old_value = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(f)

    assert f.args[0] is ctx
    assert f.args[1] is old_value
    assert len(f.args) == 2


def test_validate_field_before_update_call_with_call():
    old_obj = object()
    old_value = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(f)

    assert f.args[0] is c
    assert f.args[1] is old_value
    assert len(f.args) == 2


def test_validate_field_before_update_call_with_old_obj():
    old_obj = object()
    old_value = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(f)

    assert f.args[0] is old_obj
    assert f.args[1] is old_value
    assert len(f.args) == 2


def test_validate_field_before_update_call_with_full():
    old_obj = object()
    old_value = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(f)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert f.args[3] is old_value
    assert len(f.args) == 4


def test_validate_field_call():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is new_value
    assert len(f.args) == 1


def test_validate_field_call_with_context():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_context(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is ctx
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validate_field_call_with_call():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_call(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is c
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validate_field_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_old_obj(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is old_obj
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validate_field_call_with_new_obj():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_new_obj(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is new_obj
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validate_field_call_with_old_value():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_old_value(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is old_value
    assert f.args[1] is new_value
    assert len(f.args) == 2


def test_validate_field_call_with_full():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    f = MockFunction()
    pass_full(f)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(f, new_value)

    assert f.args[0] is ctx
    assert f.args[1] is c
    assert f.args[2] is old_obj
    assert f.args[3] is new_obj
    assert f.args[4] is old_value
    assert f.args[5] is new_value
    assert len(f.args) == 6
