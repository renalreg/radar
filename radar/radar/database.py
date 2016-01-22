from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionBase

# Session and SQLAlchemy that allow transactions to be rolled back in pytest
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

db = SQLAlchemy()
