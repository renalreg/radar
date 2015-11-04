from radar.validation.core import pass_context, pass_call, pass_old_obj, pass_new_obj, pass_old_value, pass_new_value, \
    pass_full


class Dummy(object):
    def __init__(self):
        self._pass_context = True
        self._pass_call = True
        self._pass_old_obj = True
        self._pass_new_obj = True
        self._pass_old_value = True
        self._pass_new_value = True

    def __call__(self):
        pass


def test_pass_context():
    d = Dummy()
    pass_context(d)
    assert d._pass_context


def test_pass_call():
    d = Dummy()
    pass_call(d)
    assert d._pass_call


def test_pass_old_obj():
    d = Dummy()
    pass_old_obj(d)
    assert d._pass_old_obj


def test_pass_new_obj():
    d = Dummy()
    pass_new_obj(d)
    assert d._pass_new_obj


def test_pass_old_value():
    d = Dummy()
    pass_old_value(d)
    assert d._pass_old_value


def test_pass_new_value():
    d = Dummy()
    pass_new_value(d)
    assert d._pass_new_value


def test_full():
    d = Dummy()
    pass_full(d)
    assert d._pass_context
    assert d._pass_call
    assert d._pass_old_obj
    assert d._pass_new_obj
    assert d._pass_old_value
    assert d._pass_new_value
