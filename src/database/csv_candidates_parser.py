# coding=utf-8
import pandas as pd
import json

from src.database.data_extraction_helper import get_http_request
from src.database.db_handler import engine, db_session
from src.database.models import Candidate


def retrieve_online_information(name, surname, title, aw_url):

    # WTF a typo in the table for Inka?
    if name == 'Seidel-Grothe' and surname == 'Ina':
        surname = 'Inka'

    trans = {'ä': 'a', 'ö': 'o', 'Ö': 'o', 'ü': 'u', 'ç': 'c', 'ş': 's'}
    name = name.replace(" ", "-")
    surname = surname.replace(" ", "-")
    search_name = "{}-{}".format(surname, name).lower()
    for k, v in trans.iteritems():
        search_name = search_name.replace(k, v)

    # Yay we got some very special guys here!
    if search_name == 'hartmut-heinrich-wilhelm-ebbing':
        search_name = 'hartmut-ebbing'
    elif search_name == 'ralf-henze':
        search_name = 'ralf-ewald-henze'
    elif search_name == 'daniela-kluckert':
        search_name = 'daniela-langer'  # Marriage?
    elif search_name == 'niels-korte':
        search_name = 'prof-dr-niels-korte'  # I am a professor gosh darnit!
    elif search_name == 'elisabeth-(lisa)-paus':  # WTF is this lisa?
        search_name = 'lisa-paus'
    elif search_name == 'stephan-rauhut':
        search_name = 'steve-rauhut'  # WTF is wrong with you people?
    elif search_name == 'paul-fresdorf':
        search_name = 'paul-fresdorf-2'  # Sure abgeordnetenwatch. Why don't we just add a 2?!

    aw_request = get_http_request(aw_url.format(search_name))
    if aw_request.status == 200:
        aw_profile = json.loads(aw_request.data)['profile']
        return aw_profile['personal']['picture']['url'], aw_profile['meta']['url'], aw_url.format(search_name)
    # Some people want you to know that they got a PhD others don't
    elif title and pd.notna(title):
        search_name = '{}-{}'.format(title[0:2].lower(), search_name)
        aw_request = get_http_request(aw_url.format(search_name))
        if aw_request.status == 200:
            aw_profile = json.loads(aw_request.data)['profile']
            return aw_profile['personal']['picture']['url'], aw_profile['meta']['url'], aw_url.format(search_name)

    raise Exception('No information found for {} {} and search name: {}'.format(surname, name, search_name))


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

    # Get candidates in first votes in Berlin
    ber_candidates = candidates.loc[candidates[county_index].isin(range(75, 86))]

    # Define the parties we want are interested in
    parties = ['CDU', 'SPD', 'GR\xc3\x9cNE', 'DIE LINKE', 'AfD', 'FDP']
    # Get candidates for the parties we are interested in
    par_candidates = ber_candidates.loc[ber_candidates[party_list].isin(parties) |
                                        ber_candidates[party_county].isin(parties)]

    aw_url = 'https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/{}/profile.json'

    for index, candidate in par_candidates.iterrows():
        party = candidate[party_list] if pd.notna(candidate[party_list]) else candidate[party_county]
        bwk = '0' + str(int(candidate[county_index])) if pd.notna(candidate[county_index]) else None
        liste = candidate[list_index] if pd.notna(candidate[list_index]) else -1
        title = candidate['Titel']
        name = candidate['Name']
        surname = candidate['Vorname']
        if pd.notna(candidate['Namenszusatz']):
            name = candidate['Namenszusatz'] + ' ' + name
        img_url, profile_url, description_url = retrieve_online_information(name, surname, title, aw_url)
        img_url = img_url.replace("_146", "")  # Yep abgeordnetenwatch doesn't keep track of their image urls
        db_session.add(Candidate(name, surname, party, bwk, liste, img_url, profile_url, description_url))

    db_session.commit()


if __name__ == '__main__':
    update_or_insert('../../data/source/candidates/candidates.csv')
