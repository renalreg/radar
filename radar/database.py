from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, create_session

engine = None
db_session = scoped_session(lambda: create_session(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def configure_engine(url):
    global engine
    engine = create_engine(url, echo=True)
    return engine