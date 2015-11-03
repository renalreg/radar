from radar.permissions import is_write_request


class MockRequest(object):
    def __init__(self, method):
        self.method = method


def test_read_requests():
    for method in ['GET', 'HEAD']:
        request = MockRequest(method)
        assert not is_write_request(request)


def test_write_requests():
    for method in ['POST', 'PUT', 'DELETE']:
        request = MockRequest(method)
        assert is_write_request(request)
