from functools import update_wrapper

from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy import exc, event, select


# Session and SQLAlchemy classes that allow transactions to be rolled back in pytest
# TODO report flask_sqlalchemy bug


class Session(SessionBase):
    def __init__(self, db, autocommit=False, autoflush=True, **options):
        app = db.get_app()
        bind = options.pop('bind', None) or db.engine
        binds = options.pop('binds', None)

        if binds is None:
            db.get_binds(app)

        super(Session, self).__init__(
            autocommit=autocommit,
            autoflush=autoflush,
            bind=bind,
            binds=binds,
            **options
        )


class SQLAlchemy(SQLAlchemyBase):
    def create_session(self, options):
        # Use our custom session
        return sessionmaker(class_=Session, db=self, **options)

    # Overridden so we can listen for events on the engine
    def make_connector(self, app=None, bind=None):
        connector = super(SQLAlchemy, self).make_connector(app, bind)
        engine = connector.get_engine()
        event.listens_for(engine, 'engine_connect')(ping_connection)
        return connector


db = SQLAlchemy()


# http://docs.sqlalchemy.org/en/latest/core/pooling.html#disconnect-handling-pessimistic
def ping_connection(connection, branch):
    if branch:
        # Don't ping sub-connections
        return

    try:
        # Test the connection
        connection.scalar(select([1]))
    except exc.DBAPIError as e:
        if e.connection_invalidated:
            # Establish a new connection
            connection.scalar(select([1]))
        else:
            raise


def no_autoflush(f):
    """
    Decorator to disable autoflush for the duration of the function.
    """

    def wrapper(*args, **kwargs):
        with db.session.no_autoflush:
            return f(*args, **kwargs)

    return update_wrapper(wrapper, f)


def do_drop():
    # Reflect will discover tables that aren't mapped - useful when switching branches
    db.reflect()
    db.drop_all()


def do_create():
    db.create_all()
