# coding=utf-8
import pandas as pd

from src.database.db_handler import db_session, engine
from src.database.models import UrnDistrict, LetterDistrict


def update_or_insert(file_name):
    IDENTIFIER = 'Adresse'
    CDU = 'CDU'
    SPD = 'SPD'
    LINKE = 'DIE LINKE'
    AFD = 'AfD'
    FDP = 'FDP'

    # Load Excel
    excel = pd.ExcelFile(file_name)
    votes = excel.parse('BE_W1')
    # Fucking UTF-8
    GRUNE = votes.columns[20]
    NAME = votes.columns[3]
    BWK = votes.columns[7]

    # Query Database
    urn_districts = dict((urn_district.identifier, urn_district) for urn_district in UrnDistrict.query.all())
    letter_districts = dict(
        (letter_district.identifier, letter_district) for letter_district in LetterDistrict.query.all())

    for index, row in votes.iterrows():
        adresse = row[IDENTIFIER][0:2] + row[IDENTIFIER][3:]
        if adresse in urn_districts:
            update(urn_districts[adresse], row[CDU], row[SPD], row[LINKE], row[GRUNE], row[AFD], row[FDP])
        elif adresse in letter_districts:
            update(letter_districts[adresse], row[CDU], row[SPD], row[LINKE], row[GRUNE], row[AFD], row[FDP])
        else:
            if row[IDENTIFIER][2] == 'B':
                district = LetterDistrict(identifier=adresse, bwk=row[BWK], bezname=row[NAME])
            else:
                district = UrnDistrict(identifier=adresse, bwk=row[BWK], bezname=row[NAME])

            update(district, row[CDU], row[SPD], row[LINKE], row[GRUNE], row[AFD], row[FDP])
            db_session.add(district)

    db_session.commit()


def update(district, cdu, spd, linke, gruene, afd, fdp):
    district.cdu = cdu
    district.spd = spd
    district.gruene = gruene
    district.linke = linke
    district.afd = afd
    district.fdp = fdp


if __name__ == '__main__':
    update_or_insert('../../data/source/voting/DL_BE_EE_WB_BU2017.xlsx')
