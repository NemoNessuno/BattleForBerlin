# pylint: disable=missing-docstring
import functools
from threading import Thread

from src.database.db_helper import get_results_from_table, get_county_geojson
from src.database.gerrymandering_helper import create_search_step, get_bwk_and_diff, get_neighbours, get_new_results, \
    get_winning_party, check_winning_party, add_district_to_bwk, GerrymanderingQueue, create_stop_step
from src.database.models import Diff, MergedDistrictDiff, MergedDistrict


def gerrymander(party, bwk, new_county, old_county, original_size, diffs, county_result, results, steps):
    # We try to expand our new county to a reasonable size...
    counter = 1
    while new_county and counter < original_size:
        new_new_county = []
        for district in new_county:
            if not district.neighbours:
                district.fill_neighbours()
            # ...by searching the neighbours of our glorious new county
            own_diff, own_bwk = get_bwk_and_diff(district, diffs)
            d_neighbours = get_neighbours(district, diffs,
                                          lambda n_district, n_bwk:
                                          any(b_d.identifier == n_district.identifier for b_d in old_county)
                                          or own_bwk != n_bwk)
            for neighbour, neighbour_diff, neighbour_bwk in d_neighbours:
                # Calculate the new result
                new_county_result = get_new_results(neighbour, county_result)
                new_neighbour_county_result = get_new_results(neighbour, results[neighbour_bwk], factor=-1)
                neighbour_county_winner = get_winning_party(results[neighbour_bwk])

                # Check if still win with this new district and that the old county's result is not changed
                if check_winning_party(new_county_result, party) and \
                        (neighbour_bwk == bwk or
                         check_winning_party(new_neighbour_county_result, neighbour_county_winner)):
                    counter += 1
                    add_district_to_bwk(neighbour, bwk, diffs, neighbour_diff)
                    steps.put({'action': 'grow', 'targets': get_county_geojson({neighbour_bwk, bwk})})
                    new_new_county.append(neighbour)
                    county_result = new_county_result
                    if neighbour_bwk != bwk:
                        results[neighbour_bwk] = new_neighbour_county_result

                    oc_district = next((x for x in old_county if x.identifier == neighbour.identifier), None)
                    if oc_district:
                        old_county.remove(oc_district)

        new_county = new_new_county

    forced = False

    # Check if we still have districts we have to move around
    while old_county:
        changed = False
        for district in old_county:

            if district.neighbours is None:
                district.fill_neighbours()

            # Check if we got a diff for the current district to check our districts current BWK
            own_diff, own_bwk = get_bwk_and_diff(district, diffs)

            # Search for neighbours who are in a different BWK
            d_neighbours = get_neighbours(district, diffs, lambda _, n_bwk: own_bwk != n_bwk)

            for neighbour, neighbour_diff, neighbour_bwk in d_neighbours:
                # Try to make sure that the result in the neighbours BWK is unchanged when we add this district
                old_winner = sorted(results[neighbour_bwk], key=lambda x: x[1], reverse=True)[0][0]
                n_results = neighbour.get_result_dict()
                # Add the votes of this district to the total result of the bwk
                for key in n_results.keys():
                    results[neighbour_bwk][key] += n_results[key]
                # If the result in the BWK is unchanged
                if forced or sorted(results[neighbour_bwk], key=lambda x: x[1], reverse=True)[0][0] == old_winner:
                    add_district_to_bwk(district, neighbour_bwk, diffs, own_diff)
                    old_county.remove(district)
                    steps.put({'action': 'cleanup', 'targets': get_county_geojson({neighbour_bwk, bwk})})
                    changed = True
                    forced = False

                    break
                else:
                    for key in n_results.keys():
                        results[neighbour.bwk][key] -= n_results[key]
        # If we didn't find the perfect candidate just force the addition to the
        # first potential BWK and try again
        if not changed:
            forced = True

    steps.put(create_stop_step())
    return steps


def get_gerrymandering_steps(bwk, party, steps=GerrymanderingQueue()):
    # Yay for local functions!
    # Sort bwk districts by their results
    def district_comparator(d1, d2):
        d1_party_result = d1.get_result_dict()[party]
        d2_party_result = d2.get_result_dict()[party]
        sorted_d1_tuples = sorted(d1.get_result_dict().items(), key=lambda d: d[1], reverse=True)
        sorted_d2_tuples = sorted(d2.get_result_dict().items(), key=lambda d: d[1], reverse=True)
        d1_to_first = sorted_d1_tuples[0][1] - d1_party_result
        d1_to_second = sorted_d1_tuples[1][1] - d1_party_result
        d2_to_first = sorted_d2_tuples[0][1] - d2_party_result
        d2_to_second = sorted_d2_tuples[1][1] - d2_party_result

        if d1_to_first > d2_to_first:
            return 1
        elif d1_to_first < d2_to_first:
            return -1
        else:  # When the party we look at has the most votes
            # Look at the distance to the second place
            if d1_to_second > d2_to_second:
                return 1
            elif d1_to_second < d2_to_second:
                return -1
            else:  # If this should be miraculously the same check for the largest value
                if d1_party_result > d2_party_result:
                    return -1
                elif d1_party_result < d2_party_result:
                    return 1
                else:
                    return 0

    districts = MergedDistrictDiff.query.all()
    original_bwk_districts = MergedDistrict.query.filter(MergedDistrict.bwk == bwk).all()
    diffs = Diff.query.all()
    results = get_results_from_table(MergedDistrictDiff)
    old_county = [district for district in districts if district.bwk == bwk]
    county_result = {key: 0 for key in districts[0].get_result_dict().keys()}
    if old_county:
        # Sort by highest delta
        old_county = sorted(old_county, key=functools.cmp_to_key(district_comparator))
        search_step = create_search_step(old_county)
        new_county_result = get_new_results(old_county[0], county_result)
        if check_winning_party(new_county_result, party):
            search_step['winner'] = old_county[0].identifier
            steps.put(search_step)
            return gerrymander(party, bwk, [old_county[0]], old_county[1:], len(original_bwk_districts), diffs,
                               new_county_result, results, steps)
        else:
            steps.put(search_step)

    # If we found no working solution
    # check if we find a good seed in the original district
    original_bwk_districts = sorted(original_bwk_districts, key=functools.cmp_to_key(district_comparator))
    search_step = create_search_step(original_bwk_districts)
    new_county_result = get_new_results(original_bwk_districts[0], county_result)
    if check_winning_party(new_county_result, party):
        original_district_bwk = get_bwk_and_diff(original_bwk_districts[0], diffs)[1]
        results[original_district_bwk] = get_new_results(districts[0], results[original_district_bwk], factor=-1)
        add_district_to_bwk(original_bwk_districts[0], bwk, diffs)
        search_step['winner'] = original_bwk_districts[0].identifier
        steps.put(search_step)
        return gerrymander(party, bwk, [original_bwk_districts[0]], old_county, len(original_bwk_districts),
                           diffs, new_county_result, results, steps)
    else:
        steps.put(search_step)

    # If this does not work either check if we find any district anywhere
    # By checking the neighbours of the original district and then branching outward
    alreadychecked = set([district.identifier for district in original_bwk_districts])
    check_for_neighbours = original_bwk_districts
    while check_for_neighbours:
        districts_to_check = []
        for district in check_for_neighbours:
            districts_to_check += get_neighbours(district, diffs,
                                                 lambda neighbour, _:
                                                 neighbour not in districts_to_check
                                                 and neighbour.identifier not in alreadychecked)

        search_step = create_search_step(districts)
        for district, _, district_bwk in districts_to_check:
            new_county_result = get_new_results(district, county_result)
            if check_winning_party(new_county_result, party):
                results[district_bwk] = get_new_results(district, results[district_bwk], factor=-1)
                add_district_to_bwk(district, bwk, diffs)
                search_step['winner'] = district.identifier
                steps.put(search_step)
                return gerrymander(party, bwk, [district], old_county, len(original_bwk_districts), diffs,
                                   new_county_result, results, steps)

        check_for_neighbours = [district[0] for district in districts_to_check]

    # If we haven't found any suitable candidate return
    # the search steps we have taken
    steps.put(create_stop_step())
    return steps


class GerrymanderingThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, queue=None, bwk=None, party=None):
        super(GerrymanderingThread, self).__init__()
        self.target = target
        self.name = name
        self.queue = queue
        self.bwk = bwk
        self.party = party

    def run(self):
        get_gerrymandering_steps(self.bwk, self.party, self.queue)


if __name__ == '__main__':
    get_gerrymandering_steps('083', 'gruene')
