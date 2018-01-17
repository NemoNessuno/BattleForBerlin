from __future__ import unicode_literals

import json

import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

http = urllib3.PoolManager()
ua = UserAgent()


def get_http_request(url):
    # TODO: Nice encoding error!
    return http.request('GET', url)


def get_description_json(url):
    result = {}
    try:
        if url:
            request = get_http_request(url)
            if request.status == 200:
                result = json.loads(request.data)
    finally:
        return result
