from radar.validation.core import Field, Validation


class FooValidation(Validation):
    foo = Field()
    foo._tag = 'foo_foo'
    bar = Field()
    bar._tag = 'foo_bar'
    baz = Field()
    baz._tag = 'foo_baz'


class BarValidation(Validation):
    hello = Field()
    hello._tag = 'bar_hello'
    bar = Field()
    bar._tag = 'bar_bar'


class QuxMixin(object):
    qux = Field()
    qux._tag = 'qux_qux'
    norf = Field()
    norf._tag = 'qux_norf'


class XMixin(object):
    x = Field()
    x._tag = 'x_x'
    y = Field()
    y._tag = 'x_y'
    z = Field()
    z._tag = 'x_z'
    norf = Field()
    norf._tag = 'x_norf'


class YMixin(object):
    y = Field()
    y._tag = 'y_y'
    z = Field()
    z._tag = 'y_z'
    norf = Field()
    norf._tag = 't_norf'


class NorfMixin(YMixin, XMixin):
    norf = Field()
    norf._tag = 'norf_norf'


class BazValidation(NorfMixin, BarValidation, QuxMixin, FooValidation):
    baz = Field()
    baz._tag = 'baz_baz'
    world = Field()
    world._tag = 'baz_world'



def test_validation_fields():
    v = BazValidation()
    v.get_fields()

    expected = [
        ('foo', 'foo_foo'),
        ('qux', 'qux_qux'),
        ('hello', 'bar_hello'),
        ('bar', 'bar_bar'),
        ('x', 'x_x'),
        ('y', 'y_y'),
        ('y', 'y_z'),
        ('norf', 'norf_norf'),
        ('baz', 'baz_baz'),
        ('world', 'baz_world'),
    ]

    for name, tag in expected:
        field = getattr(v, name)
        assert field._tag == tag
        assert field.field_name == name

    fields = v.get_fields()

    assert expected == [(x.field_name, x._tag) for x in fields.values()]
    assert [x[0] for x in expected] == fields.keys()
