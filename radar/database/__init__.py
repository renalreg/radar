from functools import update_wrapper

from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy import event, exc, select
from sqlalchemy.orm.session import Session as SessionBase

# Session and SQLAlchemy classes that allow transactions to be rolled back in pytest
# TODO report flask_sqlalchemy bug


class Session(SessionBase):
    # Plain SQLAlchemy session (not flask_sqlalchemy.session.Session) so an explicit
    # ``bind`` (e.g. a test connection inside an outer transaction) is honoured.
    # Flask-SQLAlchemy 3's Session.get_bind() always routes to the app's engine.
    def __init__(self, db, autocommit=False, autoflush=True, **options):
        bind = options.pop("bind", None) or db.engine
        binds = options.pop("binds", None) or {}

        super().__init__(
            autocommit=autocommit,
            autoflush=autoflush,
            bind=bind,
            binds=binds,
            **options,
        )


class SQLAlchemy(SQLAlchemyBase):
    def __init__(self, *args, **kwargs):
        # Use our custom session (replaces the create_session() override from
        # Flask-SQLAlchemy 2.x)
        session_options = kwargs.setdefault("session_options", {})
        session_options.setdefault("class_", Session)
        super().__init__(*args, **kwargs)

    # Overridden so we can listen for events on the engine
    # (replaces the make_connector() override from Flask-SQLAlchemy 2.x)
    def _make_engine(self, bind_key, options, app):
        engine = super()._make_engine(bind_key, options, app)
        event.listens_for(engine, "engine_connect")(ping_connection)
        return engine

    def create_scoped_session(self, options=None):
        """Create a new scoped session using our Session class (used by tests)."""
        options = dict(options or {})
        options.setdefault("class_", Session)
        return self._make_scoped_session(options)


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
    """Decorator to disable autoflush for the duration of the function."""

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
