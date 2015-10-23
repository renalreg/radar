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
