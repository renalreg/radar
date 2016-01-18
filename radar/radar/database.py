from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy.orm import sessionmaker


class SQLAlchemy(_SQLAlchemy):
    def create_session(self, options):
        return sessionmaker(autocommit=False, autoflush=True, **options)

db = SQLAlchemy()
