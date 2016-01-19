import pytest

from radar.app import create_app
from radar.database import db


@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgres://postgres@localhost/radar_test',
        'BASE_URL': 'http://localhost',
    })

    return app


@pytest.yield_fixture(scope='session')
def schema(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.drop_all()


@pytest.yield_fixture(scope='function', autouse=True)
def session(app, schema):
    with app.app_context():
        # Run each test inside a transaction so we can rollback any changes. A new connection is created
        # and a transaction started. The session is bound to the new connection and participates with the
        # transaction (it is free to call session.commit()). Once the test is complete the transaction is
        # rolled back.
        # http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.create_scoped_session(options=dict(bind=connection, binds={}))
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()
