class PermissionDenied(Exception):
    def __init__(self, detail=None):
        self.detail = detail


class NotFound(Exception):
    def __init__(self, detail=None):
        self.detail = detail


class BadRequest(Exception):
    def __init__(self, detail=None):
        self.detail = detail
