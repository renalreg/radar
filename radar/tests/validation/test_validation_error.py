from collections import OrderedDict

from radar.validation.core import ValidationError


def test_normalise_string():
    e = ValidationError('hello')
    assert e.errors == ['hello']


def test_normalise_list():
    errors = ['foo', 'bar', 'baz']
    e = ValidationError(errors)
    assert e.errors == errors


def test_normalise_dict():
    errors = {'foo': ['1', '2', '3'], 'bar': ['4', '5', '6']}
    e = ValidationError(errors)
    assert e.errors == errors


def test_normalise_empty_list():
    e = ValidationError([])
    assert e.errors == []


def test_normalise_empty_dict():
    e = ValidationError({})
    assert e.errors == {}


def test_normalise_list_complex():
    errors = [
        {
            'foo': ['1', '2', '3'],
            'bar': '4',
        },
        ['foo', 'bar', 'baz'],
        'foo'
    ]

    e = ValidationError(errors)

    assert e.errors == [
        {
            'foo': ['1', '2', '3'],
            'bar': ['4'],
        },
        ['foo', 'bar', 'baz'],
        'foo'
    ]


def test_normalise_dict_complex():
    errors = {
        'foo': [
            {
                'foo': '1',
                'bar': '2',
            }
        ],
        'bar': '1',
        'baz': ['1', '2', '3'],
    }

    e = ValidationError(errors)

    assert e.errors == {
        'foo': [
            {
                'foo': ['1'],
                'bar': ['2'],
            }
        ],
        'bar': ['1'],
        'baz': ['1', '2', '3'],
    }


def test_str():
    e = ValidationError(['foo', 'bar', 'baz'])
    assert str(e) == "['foo', 'bar', 'baz']"


def test_first_empty_list():
    e = ValidationError([])
    assert e.first() is None


def test_first_list():
    e = ValidationError(['error @ 0', 'error @ 1', 'error @ 2'])
    assert e.first() == (None, 'error @ 0')


def test_first_dict():
    e = ValidationError(OrderedDict([
        ('foo', 'error @ foo'),
        ('bar', 'error @ bar'),
        ('baz', 'error @ baz')
    ]))
    assert e.first() == (('foo',), 'error @ foo')


def test_first_nested_dict():
    e = ValidationError(OrderedDict([
        ('foo', OrderedDict([
            ('hello', 'error @ foo.hello'),
            ('world', 'error @ foo.world'),
        ])),
        ('bar', 'error @ bar'),
        ('baz', 'error @ baz')
    ]))
    assert e.first() == (('foo', 'hello'), 'error @ foo.hello')


def test_first_list_in_dict():
    e = ValidationError(OrderedDict([
        ('foo', ['error @ foo.0', 'error @ foo.1', 'error @ foo.2']),
        ('bar', 'error @ bar'),
        ('baz', 'error @ baz')
    ]))
    assert e.first() == (('foo',), 'error @ foo.0')


def test_first_list_in_dict():
    e = ValidationError([
        OrderedDict([
            ('foo', 'error @ 0.foo'),
            ('bar', 'error @ 0.bar'),
            ('baz', 'error @ 0.baz')
        ]),
        OrderedDict([
            ('foo', 'error @ 1.foo'),
            ('bar', 'error @ 1.bar'),
            ('baz', 'error @ 1.baz')
        ])
    ])
    assert e.first() == (('foo',), 'error @ 0.foo')
