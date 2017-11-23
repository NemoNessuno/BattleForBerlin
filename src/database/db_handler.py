from geoalchemy2 import functions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:postgres@localhost:5432/battle_for_berlin')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# This is only here to have a crude method of simple testing
if __name__ == '__main__':
    from models import District
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.

    for district, geom in db_session.query(District, functions.ST_AsGeoJSON(functions.ST_Transform(District.geom, 4326))):
        print district.geom
