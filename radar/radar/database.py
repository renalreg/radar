from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionBase
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

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
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select([1]))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select([1]))
        else:
            raise
