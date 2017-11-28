# coding=utf-8
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from db_handler import Base


class District(Base):
    __tablename__ = 'districts'
    identifier = Column(String(4), unique=True, primary_key=True)
    bezname = Column(String(200))
    bwk = Column(String(3))
    geom = Column(Geometry('POLYGON'))
    bez_type = Column('type', String(8))

    def __init__(self, identifier=None, bezname=None,
                 bwk=None, geom=None, bez_type=None):
        self.identifier = identifier
        self.bezname = bezname
        self.bwk = bwk
        self.geom = geom
        self.bez_type = bez_type

    def __repr__(self):
        return '<District %s %s>' % (self.identifier, self.geom)


class Result(Base):
    __tablename__ = 'results'
    identifier = Column(String(5), unique=True, primary_key=True)
    bwk = Column(String(3))
    voters = Column(Integer)
    valid = Column(Integer)
    invalid = Column(Integer)
    cdu = Column(Integer)
    spd = Column(Integer)
    die_linke = Column(Integer)
    gruene = Column(Integer)
    afd = Column(Integer)
    fdp = Column(Integer)

    def __init__(self, identifier=None, bwk=None,
                 voters=0, valid=0, invalid=0,
                 cdu=0, spd=0, die_linke=0,
                 gruene=0, afd=0, fdp=0):
        self.identifier = identifier
        self.bwk = bwk
        self.voters = voters
        self.valid = valid
        self.invalid = invalid
        self.cdu = cdu
        self.spd = spd
        self.die_linke = die_linke
        self.gruene = gruene
        self.afd = afd
        self.fdp = fdp

    def __repr__(self):
        return '<Result %s CDU: %d  SPD: %d  Die Linke: %d  Grüne: %d FDP: %d AFD: %d>' % \
               (self.identifier, self.cdu, self.spd, self.die_linke, self.gruene, self.fdp, self.afd)
