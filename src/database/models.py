# coding=utf-8
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from db_handler import Base


class District:
    identifier = Column(String(4), unique=True, primary_key=True)
    bezname = Column(String(200))
    bwk = Column(String(3))
    geom = Column(Geometry('POLYGON'))
    cdu = Column(Integer)
    spd = Column(Integer)
    die_linke = Column(Integer)
    gruene = Column(Integer)
    afd = Column(Integer)
    fdp = Column(Integer)

    def __init__(self, identifier=None, bezname=None,
                 bwk=None, geom=None,
                 cdu=0, spd=0, die_linke=0,
                 gruene=0, afd=0, fdp=0):
        self.identifier = identifier
        self.bezname = bezname
        self.bwk = bwk
        self.geom = geom
        self.cdu = cdu
        self.spd = spd
        self.die_linke = die_linke
        self.gruene = gruene
        self.afd = afd
        self.fdp = fdp

    def get_geojson_dict(self):
        return {
            "identifier": self.identifier,
            "bezname": self.bezname,
            "bwk": self.bwk,
            "result": self.get_result_dict()
        }

    def get_result_dict(self):
        return {
            "cdu": self.cdu,
            "spd": self.spd,
            "die_linke": self.die_linke,
            "gruene": self.gruene,
            "afd": self.afd,
            "fdp": self.fdp
        }

    def __repr__(self):
        return '<District %s %s>' % (self.identifier, self.geom)


class UrnDistrict(District, Base):
    __tablename__ = 'urn_districts'


class LetterDistrict(District, Base):
    __tablename__ = 'letter_districts'

class MergedDistrict(District, Base):
    __tablename__ = 'merged_districts'

class MergedDistrictDiff(District, Base):
    __tablename__ = 'merged_districts_diff'

class Diff(Base):
    __tablename__ = 'diffs'
    identifier = Column(String(4), primary_key=True)
    bwk = Column(String(4))

    def __init__(self, identifier=None, bwk=None):
        self.identifier = identifier
        self.bwk = bwk

    def __repr__(self):
        return '<Diff %s %s>' % (self.identifier, self.bwk)
