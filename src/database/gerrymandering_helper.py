import functools

from src.database.db_handler import db_session
from src.database.db_helper import get_results
from src.database.models import MergedDistrict, Diff


def get_gerrymandering_steps(bwk, party):
    districts = MergedDistrict.query.all()
    diffs = Diff.query.all()
    results = get_results()['diff']

    bwk_districts = [district for district in districts if district.bwk == bwk]

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

    # Sort by highest delta
    bwk_districts = sorted(bwk_districts, key=functools.cmp_to_key(district_comparator))

    new_county = []
    sums = {key: 0 for key in bwk_districts[0].get_result_dict().keys()}

    while True:
        # Take the first district and put it into our new county
        new_county.append(bwk_districts[0])

        # And remove it from the old county
        bwk_districts = bwk_districts[1:]
        # Calculate the new result
        nc_results = new_county[-1].get_result_dict()
        for key in sums.keys():
            sums[key] += nc_results[key]

        nd_sorted = sorted(sums.items(), key=lambda x: x[1], reverse=True)
        # And make sure that our designated winner is still winning
        # Or the old district is empty
        if nd_sorted[0][0] != party or len(bwk_districts) < 1:
            break

    def in_different_bwk(check_district, check_bwk):
        loc_diff = next((x for x in diffs if x.identifier == check_district.identifier), None)
        if loc_diff:
            "Diff: {} {}".format(loc_diff.bwk, check_bwk)
            return loc_diff.bwk != check_bwk
        else:
            return check_district.bwk != check_bwk

    # If we found a working solution
    if len(new_county) > 0:
        # Check if we are still winning
        nd_sorted = sorted(sums.items(), key=lambda x: x[1], reverse=True)
        if nd_sorted[0][0] != party:
            # If not remove the last entry
            bwk_districts.append(new_county[-1])

        forced = False

        # Now check if we still have districts we have to move around
        while len(bwk_districts) > 0:
            changed = False
            for district in bwk_districts:
                # Get all bwks that are not ours and are a neighbour of the current district
                if district.neighbours is None:
                    district.fill_neighbours()

                d_neighbours = [neighbour for neighbour in district.neighbours
                                if in_different_bwk(neighbour, district.bwk)]
                for neighbour in d_neighbours:
                    neighbour_diff = next((x for x in diffs if x.identifier == neighbour.identifier), None)
                    new_bwk = neighbour_diff.bwk if neighbour_diff else neighbour.bwk
                    old_winner = sorted(results[new_bwk], key=lambda x: x[1], reverse=True)[0][0]
                    n_results = neighbour.get_result_dict()
                    for key in n_results.keys():
                        results[neighbour.bwk][key] += n_results[key]

                    if forced or sorted(results[new_bwk], key=lambda x: x[1], reverse=True)[0][0] == old_winner:
                        own_diff = next((x for x in diffs if x.identifier == district.identifier), None)
                        if own_diff:
                            own_diff.bwk = new_bwk
                        else:
                            new_diff = Diff(district.identifier, new_bwk)
                            db_session.add(new_diff)
                            diffs.append(new_diff)

                        bwk_districts.remove(district)
                        changed = True
                        forced = False

                        break
                    else:
                        for key in n_results.keys():
                            results[neighbour.bwk][key] -= n_results[key]
            # If we didn't find the perfect candidate just force it
            if not changed:
                forced = True

    db_session.commit()


if __name__ == '__main__':
    get_gerrymandering_steps('078', 'cdu')
