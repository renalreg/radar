import json

from flask.testing import FlaskClient


class TestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.token = None

    def login(self, user, password='password'):
        response = self.post(
            '/login',
            data={
                'username': user.username,
                'password': password,
            }
        )

        assert response.status_code == 200

        self.token = json.loads(response.data)['token']

    def open(self, *args, **kwargs):
        content_type = kwargs.pop('content_type', None)
        data = kwargs.pop('data', None)

        if data is not None and content_type is None:
            content_type = 'application/json'

        if content_type == 'application/json':
            data = json.dumps(data)

        environ_base = kwargs.pop('environ_base', {})
        environ_base.setdefault('REMOTE_ADDR', '127.0.0.1')

        headers = kwargs.pop('headers', {})

        if self.token is not None:
            headers['x-auth-token'] = self.token

        return super(TestClient, self).open(
            *args,
            content_type=content_type,
            data=data,
            environ_base=environ_base,
            headers=headers,
            **kwargs
        )
