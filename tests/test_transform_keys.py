from radar.utils import snake_case_keys, camel_case_keys


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