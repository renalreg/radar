import json

import pytest
from flask.testing import FlaskClient

from radar_api.app import create_app
from radar.database import db


@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://postgres@localhost/radar_test',
        'BASE_URL': 'http://localhost',
    })

    app.test_client_class = TestClient

    return app


@pytest.yield_fixture(scope='session')
def tables(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()


@pytest.yield_fixture(scope='function', autouse=True)
def session(app, tables):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.create_scoped_session(options=dict(bind=connection))
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()


class TestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.token = None

    def login(self, user):
        response = self.post(
            '/login',
            data={
                'username': user.username,
                'password': 'password',
            }
        )

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
