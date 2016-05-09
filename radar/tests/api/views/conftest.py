import pytest

from radar.database import db
from radar.tests.api.views.fixtures import create_fixtures


@pytest.yield_fixture(scope='session')
def tables(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        # TODO UnboundExecutionError without this
        db.session = db.create_scoped_session(options=dict(bind=db.engine))

        # Create fixtures here so the tests run faster
        # TODO should probably be changed so tests can have different fixtures
        create_fixtures()
        db.session.commit()

        yield db

        db.drop_all()


@pytest.yield_fixture(scope='function', autouse=True)
def session(app, tables):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.create_scoped_session(options=dict(bind=connection, binds={}))
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()
