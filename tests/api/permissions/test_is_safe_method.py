import pytest

from radar.api.permissions import is_safe_method
from tests.api.permissions.helpers import MockRequest


@pytest.mark.parametrize('method', ['GET', 'HEAD'])
def test_safe_requests(method):
    request = MockRequest(method)
    assert is_safe_method(request)


def test_unsafe_requests():
    for method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        request = MockRequest(method)
        assert not is_safe_method(request)
