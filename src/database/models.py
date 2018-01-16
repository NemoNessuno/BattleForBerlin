# coding=utf-8
from __future__ import unicode_literals
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from db_handler import Base, db_session
from src.database.data_extraction_helper import get_description_json


class District:
    identifier = Column(String(5), unique=True, primary_key=True)
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
        candidates = db_session.query(Candidate).filter(Candidate.bwk == self.bwk)
        return {
            'identifier': self.identifier,
            'bezname': self.bezname,
            'bwk': self.bwk,
            'candidates': {candidate.party: candidate.get_json() for candidate in candidates},
            'result': self.get_result_dict()
        }

    def get_result_dict(self):
        return {
            'cdu': self.cdu,
            'spd': self.spd,
            'die_linke': self.die_linke,
            'gruene': self.gruene,
            'afd': self.afd,
            'fdp': self.fdp
        }

    def __repr__(self):
        return '<District %s bwk: %s result: %s>' % (self.identifier, self.bwk, self.get_result_dict())


class Neighbours(Base):
    __tablename__ = 'neighbours'
    identifier = Column(String(5), primary_key=True, unique=True)
    neighbours = Column(String(128))

    def __init__(self, identifier=None, neighbours=None):
        self.identifier = identifier
        self.neighbours = neighbours


class MergedDistrict(District, Base):
    __tablename__ = 'merged_districts'
    neighbours = None

    def fill_neighbours(self):
        neighbour = Neighbours.query.filter(Neighbours.identifier == self.identifier).first()
        self.neighbours = []
        for id in neighbour.neighbours.replace(' ', '').split(','):
            self.neighbours.append(MergedDistrict.query.filter(MergedDistrict.identifier == id).first())


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


class Candidate(Base):
    __tablename__ = 'candidates'
    identifier = Column(Integer, primary_key=True)
    name = Column(String(256))
    surname = Column(String(256))
    party = Column(String(10))
    bwk = Column(String(4))
    liste = Column(Integer)
    img_url = Column(String(256))
    profile_url = Column(String(256))
    description_url = Column(String(256))

    def get_json(self):
        return {
            "name": self.get_full_name(),
            "party": self.party,
            "list index": self.liste,
            "bwk": self.bwk,
            "image": self.img_url,
            "profile_url": self.profile_url,
            "description": self.description_url
        }

    def get_description(self):
        return get_description_json(self.description_url)

    def get_full_name(self):
        return "{} {}".format(self.surname, self.name)

    def __init__(self, name=None, surname=None, party=None, bwk=None, liste=-1,
                 img_url=None, profile_url=None, description_url=None):
        self.name = name
        self.surname = surname
        self.party = party
        self.bwk = bwk
        self.liste = liste
        self.img_url = img_url,
        self.profile_url=profile_url,
        self.description_url=description_url

    def __repr__(self):
        return '<Candidate {} {} of Party {}; BWK: {} Listenplatz: {}>'.format(
            self.name, self.surname, self.party, self.bwk, self.liste
        )
