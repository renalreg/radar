from functools import update_wrapper

from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.orm.session import Session as SessionBase

# Session and SQLAlchemy classes that allow transactions to be rolled back in pytest
# TODO report flask_sqlalchemy bug


class Session(SessionBase):
    # Plain SQLAlchemy session (not flask_sqlalchemy.session.Session) so an explicit
    # ``bind`` (e.g. a test connection inside an outer transaction) is honoured.
    # Flask-SQLAlchemy 3's Session.get_bind() always routes to the app's engine.
    def __init__(self, db, autoflush=True, **options):
        bind = options.pop("bind", None) or db.engine
        binds = options.pop("binds", None) or {}

        super().__init__(
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

        # Test connections before use and transparently replace stale ones
        # (replaces the old engine_connect "ping_connection" recipe, whose
        # ``branch`` argument no longer exists in SQLAlchemy 2.0)
        engine_options = kwargs.setdefault("engine_options", {})
        engine_options.setdefault("pool_pre_ping", True)

        super().__init__(*args, **kwargs)

    def create_scoped_session(self, options=None):
        """Create a new scoped session using our Session class (used by tests)."""
        options = dict(options or {})
        options.setdefault("class_", Session)
        return self._make_scoped_session(options)


db = SQLAlchemy()


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
