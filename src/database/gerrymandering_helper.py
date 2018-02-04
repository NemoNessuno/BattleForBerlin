import Queue

from src.database.db_handler import db_session
from src.database.models import Diff


def create_search_step(candidates):
    return {'action': 'search', 'candidates': [district.identifier for district in candidates]}


def create_stop_step():
    return {'action': 'stop'}


def check_winning_party(voting_results, party):
    if any(value > 0 for value in voting_results.values()):
        return get_winning_party(voting_results) == party
    else:
        return False


def get_winning_party(voting_results):
    return sorted(voting_results.items(), key=lambda x: x[1], reverse=True)[0][0]


def get_new_results(district, sums, factor=1):
    nc_results = district.get_result_dict()
    new_sums = sums.copy()
    for key in sums.keys():
        new_sums[key] += nc_results[key] * factor
    return new_sums


def get_neighbours(district, diffs, filter_function):
    # Get all neighbours that are not in the current districts BWK
    d_neighbours = []
    if not district.neighbours:
        district.fill_neighbours()

    for n in district.neighbours:
        n_diff, n_bwk = get_bwk_and_diff(n, diffs)
        if filter_function(n, n_bwk):
            d_neighbours.append((n, n_diff, n_bwk))
    return d_neighbours


def add_district_to_bwk(target_district, target_bwk, diffs, district_diff=None):
    if not district_diff:
        district_diff = get_bwk_and_diff(target_district, diffs)[0]

    # Check if we got a diff already
    if district_diff:
        if target_bwk == target_district.bwk:
            diffs.remove(district_diff)
            db_session.delete(district_diff)
        else:
            district_diff.bwk = target_bwk

    # ... if not add one
    elif target_bwk != target_district.bwk:
        target_diff = Diff(target_district.identifier, target_bwk)
        db_session.add(target_diff)
        diffs.append(target_diff)

    db_session.commit()


# Returns the districts diff entry and current BWK
def get_bwk_and_diff(district_to_check, diffs):
    loc_diff = next((x for x in diffs if x.identifier == district_to_check.identifier), None)

    if loc_diff:
        loc_bwk = loc_diff.bwk
    else:
        loc_bwk = district_to_check.bwk

    return loc_diff, loc_bwk


class GerrymanderingQueue:

    def __init__(self, queue=[]):
        self.queue = queue

    def put(self, item):
        if isinstance(self.queue, Queue.Queue):
            self.queue.put(item)
        else:
            self.queue.append(item)

    def get(self):
        if isinstance(self.queue, Queue.Queue):
            return self.queue.get()
        else:
            return self.queue[0]

    def get_all(self):
        if isinstance(self.queue, Queue.Queue):
            result = []
            while not self.queue.empty():
                result.append(self.queue.get())

            return result
        else:
            return self.queue
