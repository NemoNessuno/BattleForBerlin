from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, text

from db_handler import Base


class District(Base):
    __tablename__ = 'districts'

    to_geojson = text('ST_AsGeoJSON(districts.geom)')
    gid = Column(Integer, unique=True, primary_key=True)

    fid_1 = Column(String(200))
    uwb = Column(String(200))
    uwb3 = Column(String(3))
    bwb = Column(String(4))
    bwb2 = Column(String(200))
    awk = Column(String(4))
    bez = Column(String(2))
    bezname = Column(String(200))
    bwk = Column(String(3))
    ow = Column(String(200))
    geom = Column(Geometry('POLYGON'))

    def get_id(self):
        return self.gid

    def __init__(self, did=0, fid_1=None, uwb=None, uwb3=None,
                 bwb=None, bwb2=None, awk=None, bez=None, bezname=None,
                 bwk=None, ow=None, geom=None):
        self.gid = did
        self.fid_1 = fid_1
        self.uwb = uwb
        self.uwb3 = uwb3
        self.bwb = bwb
        self.bwb2 = bwb2
        self.awk = awk
        self.bez = bez
        self.bezname = bezname
        self.bwk = bwk
        self.ow = ow
        self.geom = geom

    def __repr__(self):
        return '<District %d %s>' % (self.gid, self.geom)
