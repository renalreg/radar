from radar.validation.core import CleanObject


def test_clean_object():
    data = {'foo': 1, 'bar': 2, 'baz': 3}

    o = CleanObject(data)

    for k, v in data.items():
        assert getattr(o, k) == v
        assert o[k] == v
