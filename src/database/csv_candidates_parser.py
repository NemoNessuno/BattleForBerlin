# coding=utf-8
import pandas as pd
import json

from src.database.data_extraction_helper import get_http_request, extract_afd_fraction, \
    extract_spd_neukoelln_fraction, extract_fdp_cw_fraction
from src.database.db_handler import engine, db_session
from src.database.models import Candidate


def retrieve_online_information(name, surname, aw_url, fall_back_extractors):
    trans = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ç': 'c'}
    search_name = "{}-{}".format(surname, name).lower()
    for k, v in trans.iteritems():
        search_name = search_name.replace(k, v)

    aw_request = get_http_request(aw_url.format(search_name))
    if aw_request.status == 200:
        aw_profile = json.loads(aw_request.data)['profile']
        return aw_profile['personal']['picture']['url'], aw_profile['meta']['url'], aw_url.format(search_name)
    else:
        for extractor in fall_back_extractors:
            (profile_url, img_url) = extractor(search_name)
            if profile_url is not None and img_url is not None:
                return img_url, profile_url, ''

    return 'https://www.abgeordnetenwatch.de/sites/abgeordnetenwatch.de/files/styles/' \
           'square_medium/public/default_images/profil_dummy_0.jpg', '', ''
    # TODO: Create extraction helper for the other candidates
    # raise Exception('No information found for {} {}'.format(surname, name))


def update_or_insert(path):
    party_list = 'Liste_ParteiKurzBez'
    party_county = 'Wahlkreis_ParteiKurzBez'
    county_index = 'Wahlkreis_Nr'
    list_index = 'Liste_Platz'

    # Delete the table if it exists
    if Candidate.__table__.exists(engine):
        Candidate.__table__.drop(engine)
    # Create a fresh candidate table
    Candidate.__table__.create(engine)

    # Set the seperator to ; and ignore the first seven lines
    candidates = pd.read_csv(path, sep=';', header=[7])

    # Get candidates in Berlin
    ber_candidates = candidates.loc[candidates['Liste_Land'].isin(['BE']) |
                                    candidates[county_index].isin(range(75, 86))]

    # Define the parties we want are interested in
    parties = ['CDU', 'SPD', 'GR\xc3\x9cNE', 'DIE LINKE', 'AfD', 'FDP']
    # Get candidates for the parties we are interested in
    par_candidates = ber_candidates.loc[ber_candidates[party_list].isin(parties) |
                                        ber_candidates[party_county].isin(parties)]

    aw_url = 'https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/{}/profile.json'
    fallback_urls = {
        parties[0]: [],  # CDU
        parties[1]: [extract_spd_neukoelln_fraction],#['https://www.spdfraktion-berlin.de/abgeordnete/{}',  # SPD
                      #'http://www.spd-fraktion.net/die-fraktion/fraktionsmitglieder/{}'],
        parties[2]: [],#['https://gruene.berlin/{}'],  # Grüne
        parties[3]: [],  # Die Linke
        parties[4]: [extract_afd_fraction],  # AfD
        parties[5]: [extract_fdp_cw_fraction],  # FDP
   }

    for index, candidate in par_candidates.iterrows():
        party = candidate[party_list] if pd.notna(candidate[party_list]) else candidate[party_county]
        bwk = '0' + str(int(candidate[county_index])) if pd.notna(candidate[county_index]) else None
        liste = candidate[list_index] if pd.notna(candidate[list_index]) else -1
        name = candidate['Name']
        surname = candidate['Vorname']
        if pd.notna(candidate['Namenszusatz']):
            name = candidate['Namenszusatz'] + ' ' + name
        img_url, profile_url, description_url = retrieve_online_information(name, surname, aw_url, fallback_urls[party])
        db_session.add(Candidate(name, surname, party, bwk, liste, img_url, profile_url, description_url))

    db_session.commit()


if __name__ == '__main__':
    update_or_insert('../../data/source/candidates/candidates.csv')
