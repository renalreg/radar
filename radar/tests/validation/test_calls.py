from radar.validation.core import ContextBeforeUpdateCall, pass_call, pass_full, pass_old_obj, ContextCall, pass_new_obj, \
    pass_context, ValidatorCall, pass_old_value, PreValidateCall, ValidateBeforeUpdateCall, ValidateCall, \
    ValidateFieldBeforeUpdateCall, ValidateFieldCall


class Dummy(object):
    def __init__(self):
        self.args = []

    def __call__(self, *args):
        self.args = args


def test_context_before_update_call():
    old_obj = object()
    ctx = {}
    d = Dummy()

    c = ContextBeforeUpdateCall(old_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert len(d.args) == 1


def test_context_before_update_call_with_call():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ContextBeforeUpdateCall(old_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert len(d.args) == 2


def test_context_before_update_call_with_old_obj():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = ContextBeforeUpdateCall(old_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is old_obj
    assert len(d.args) == 2


def test_context_before_update_call_with_full():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ContextBeforeUpdateCall(old_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert len(d.args) == 3


def test_context_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()

    c = ContextCall(old_obj, new_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert len(d.args) == 1


def test_context_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ContextCall(old_obj, new_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert len(d.args) == 2


def test_context_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = ContextCall(old_obj, new_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is old_obj
    assert len(d.args) == 2


def test_context_call_with_new_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_new_obj(d)

    c = ContextCall(old_obj, new_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_context_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ContextCall(old_obj, new_obj)
    c(d, ctx)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert d.args[3] is new_obj
    assert len(d.args) == 4


def test_validator_call():
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()

    c = ValidatorCall(ctx, old_value)
    c(d, new_value)

    assert d.args[0] is new_value
    assert len(d.args) == 1


def test_validator_call_with_context():
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = ValidatorCall(ctx, old_value)
    c(d, new_value)

    assert d.args[0] is ctx
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validator_call_with_call():
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ValidatorCall(ctx, old_value)
    c(d, new_value)

    assert d.args[0] is c
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validator_call_with_old_value():
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_old_value(d)

    c = ValidatorCall(ctx, old_value)
    c(d, new_value)

    assert d.args[0] is old_value
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validator_call_with_full():
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ValidatorCall(ctx, old_value)
    c(d, new_value)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_value
    assert d.args[3] is new_value
    assert len(d.args) == 4


def test_pre_validate_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()

    c = PreValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is new_obj
    assert len(d.args) == 1


def test_pre_validate_call_with_context():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = PreValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is ctx
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_pre_validate_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = PreValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is c
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_pre_validate_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = PreValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is old_obj
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_pre_validate_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = PreValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert d.args[3] is new_obj
    assert len(d.args) == 4


def test_validate_before_update_call():
    old_obj = object()
    ctx = {}
    d = Dummy()

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(d)

    assert d.args[0] is old_obj
    assert len(d.args) == 1


def test_validate_before_update_call_with_context():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(d)

    assert d.args[0] is ctx
    assert d.args[1] is old_obj
    assert len(d.args) == 2


def test_validate_before_update_call_with_call():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(d)

    assert d.args[0] is c
    assert d.args[1] is old_obj
    assert len(d.args) == 2


def test_validate_before_update_call_with_full():
    old_obj = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ValidateBeforeUpdateCall(ctx, old_obj)
    c(d)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert len(d.args) == 3


def test_validate_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()

    c = ValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is new_obj
    assert len(d.args) == 1


def test_validate_call_with_context():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = ValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is ctx
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_validate_call_with_call():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is c
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_validate_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = ValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is old_obj
    assert d.args[1] is new_obj
    assert len(d.args) == 2


def test_validate_call_with_full():
    old_obj = object()
    new_obj = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ValidateCall(ctx, old_obj)
    c(d, new_obj)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert d.args[3] is new_obj
    assert len(d.args) == 4


def test_validate_field_before_update_call():
    old_obj = object()
    old_value = object()
    ctx = {}
    d = Dummy()

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(d)

    assert d.args[0] is old_value
    assert len(d.args) == 1


def test_validate_field_before_update_call_with_context():
    old_obj = object()
    old_value = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(d)

    assert d.args[0] is ctx
    assert d.args[1] is old_value
    assert len(d.args) == 2


def test_validate_field_before_update_call_with_call():
    old_obj = object()
    old_value = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(d)

    assert d.args[0] is c
    assert d.args[1] is old_value
    assert len(d.args) == 2


def test_validate_field_before_update_call_with_old_obj():
    old_obj = object()
    old_value = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(d)

    assert d.args[0] is old_obj
    assert d.args[1] is old_value
    assert len(d.args) == 2


def test_validate_field_before_update_call_with_full():
    old_obj = object()
    old_value = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ValidateFieldBeforeUpdateCall(ctx, old_obj, old_value)
    c(d)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert d.args[3] is old_value
    assert len(d.args) == 4


def test_validate_field_call():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is new_value
    assert len(d.args) == 1


def test_validate_field_call_with_context():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_context(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is ctx
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validate_field_call_with_call():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_call(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is c
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validate_field_call_with_old_obj():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_old_obj(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is old_obj
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validate_field_call_with_new_obj():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_new_obj(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is new_obj
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validate_field_call_with_old_value():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_old_value(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is old_value
    assert d.args[1] is new_value
    assert len(d.args) == 2


def test_validate_field_call_with_full():
    old_obj = object()
    new_obj = object()
    old_value = object()
    new_value = object()
    ctx = {}
    d = Dummy()
    pass_full(d)

    c = ValidateFieldCall(ctx, old_obj, new_obj, old_value)
    c(d, new_value)

    assert d.args[0] is ctx
    assert d.args[1] is c
    assert d.args[2] is old_obj
    assert d.args[3] is new_obj
    assert d.args[4] is old_value
    assert d.args[5] is new_value
    assert len(d.args) == 6
