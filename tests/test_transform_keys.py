from radar.utils import (
    camel_case,
    camel_case_keys,
    snake_case,
    snake_case_keys,
)


def test_snake_case():
    return snake_case('fooBar') == 'foo_bar'


def test_camel_case():
    return camel_case('foo_bar') == 'fooBar'


def test_snake_case_keys():
    assert snake_case_keys({
        'fooBar': [
            {
                'fooBar': 'helloWorld'
            }
        ]
    }) == {
        'foo_bar': [
            {
                'foo_bar': 'helloWorld'
            }
        ]
    }


def test_camel_case_keys():
    assert camel_case_keys({
        'foo_bar': [
            {
                'foo_bar': 'hello_world'
            }
        ]
    }) == {
        'fooBar': [
            {
                'fooBar': 'hello_world'
            }
        ]
    }
