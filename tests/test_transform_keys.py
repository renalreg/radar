from radar.utils import snake_case, camel_case


def test_snake_case():
    assert snake_case({
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


def test_camel_case():
    assert camel_case({
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