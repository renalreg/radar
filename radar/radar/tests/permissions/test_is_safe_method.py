import pytest

from radar.permissions import is_safe_method


class MockRequest(object):
    def __init__(self, method):
        self.method = method


@pytest.mark.parametrize('method', ['GET', 'HEAD'])
def test_safe_requests(method):
    request = MockRequest(method)
    assert is_safe_method(request)


def test_unsafe_requests():
    for method in ['POST', 'PUT', 'DELETE']:
        request = MockRequest(method)
        assert not is_safe_method(request)
