import json

import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()


def get_http_request(url):
    return http.request('GET', url)


def get_description_json(url):
    result = {}

    request = get_http_request(url)
    if request.status == 200:
        result = json.loads(request.data)

    return result


def extract_afd_fraction(search_name):
    base_profile_url = 'https://www.afd-fraktion.berlin/{}'
    base_image_url = 'https://static.wixstatic.com/media/{}'

    # Parse the AfD profile page
    html_request = get_http_request(base_profile_url.format(search_name))

    if html_request.status == 200:
        bs_html = BeautifulSoup(html_request.data, 'html.parser')
        # Extract the links that get loaded asynchronously
        fetches = bs_html.find_all('link', {"as": "fetch"})

        # Iterate over each link
        for fetch in fetches:
            # Load the json if it its a valid url
            fetch_json_request = get_http_request(fetch['href'])
            if fetch_json_request.status == 200:
                data_items = json.loads(fetch_json_request.data)['data']['document_data']

                # Find and extract the link to the image url
                for _, v in data_items.iteritems():
                    if 'uri' in v.keys() and 'jpg' in v['uri']:
                            return base_profile_url.format(search_name), base_image_url.format(v['uri'])

    return None, None


def extract_spd_neukoelln_fraction(search_name):
    base_profile_url = 'https://spd-neukoelln.de/text-blocks/{}'
    request = get_http_request(base_profile_url.format(search_name))

    if request.status == 200:
        html = BeautifulSoup(request.data, 'html.parser')
        return base_profile_url.format(search_name), html.img['src']

    return None, None


def extract_fdp_cw_fraction(search_name):
    base_profile_url = 'http://www.fdp-cw.de/{}'
    request = get_http_request(base_profile_url.format(search_name))

    if request.status == 200:
        html = BeautifulSoup(request.data, 'html.parser')
        return base_profile_url.format(search_name), html.find_all('img')[2]['src']

    return None, None
