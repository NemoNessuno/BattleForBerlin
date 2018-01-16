import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = os.environ.get('BFB_DB_URL', 'postgresql://postgres:postgres@172.17.0.2:5432/battle_for_berlin')
engine = create_engine(DB_URL)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
