import requests
import traceback

from bs4 import BeautifulSoup
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from requests.status_codes import codes
from typing import List

from crawler.settings import CACHE_TTL_SEC


def crawl_page(page_text: str) -> List[str] | None:
    soup = BeautifulSoup(page_text, 'html.parser')
    links = soup.find_all('a')
    urls = [link.get('href') for link in links]
    return urls


def validate_url_string(url: str) -> List[str]:
    errors = []
    if not url:
        errors.append("Please enter URL to be parsed")

    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        errors.append("Invalid URL format has passed")

    return errors


def make_get_http_request(url: str) -> (List[str], str, str):
    urls = []
    error = None
    response_status_code = codes.ok
    try:
        response = requests.get(url)
    except Exception:
        error = f'Connection error: {traceback.print_exc()}'
        response_status_code = codes.bad_request
    else:
        if response.status_code == codes.ok:
            urls = crawl_page(response.text)
            cache.set(url, urls, CACHE_TTL_SEC)
        else:
            error = f'Error response from passed URL. Status: {response.status_code}.'
            response_status_code = codes.bad_request
    return urls, response_status_code, error
