from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from typing import List


def crawl_url(page_text: str) -> List[str] | None:
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
