import csv
import os

from src.database.db_handler import db_session
from src.database.models import Result


def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, delimiter=',', quotechar='"', **kwargs)
    for row in csv_reader:
        yield [cell.replace('\n', '').replace('\r', '').replace('-', '') for cell in row]


if __name__ == '__main__':
    filename = '../../data/source/voting/vote_1.csv'
    reader = unicode_csv_reader(open(filename))
    parties = [17, 18, 19, 20, 21, 23]
    metadata = [0, 7, 9, 13, 15, 16]
    all_results = list(reader)
    header = [all_results[0][index] for index in metadata + parties]

    # Result.__table__.create(bind=engine)
    for parties_results in all_results[1:]:
        parties_result = [parties_results[index] for index in metadata + parties]

        result = Result(identifier=parties_result[0][:2] + parties_result[0][3:],
                        bwk=parties_result[1],
                        voters=int(parties_result[2]),
                        valid=int(parties_result[3]),
                        invalid=int(parties_result[4]),
                        cdu=int(parties_result[6]),
                        spd=int(parties_result[7]),
                        die_linke=int(parties_result[8]),
                        gruene=int(parties_result[9]),
                        afd=int(parties_result[10]),
                        fdp=int(parties_result[11]))

        db_session.add(result)

    db_session.commit()
