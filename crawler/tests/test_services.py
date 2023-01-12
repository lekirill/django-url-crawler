import os
from django.test import override_settings
from unittest import mock
from requests.status_codes import codes

from crawler.services import crawl_page, validate_url_string, make_get_http_request


def test_crawl_url_base():
    page_text = """
    <!DOCTYPE html>
    <html>
    <body>
    
    <h1>My First Heading</h1>
    <a href="link1">link1</a>
    <a href="link2">link2</a>
    <a href="link3">link3</a>
    
    </body>
    </html>
    """
    urls = crawl_page(page_text)
    assert len(urls) == 3


def test_validate_url_string_valid():
    url_str = 'https://en.wikipedia.org/wiki/Django_(web_framework)'
    errors = validate_url_string(url_str)
    assert not errors


def test_validate_url_string_empty():
    url_str = ''
    errors = validate_url_string(url_str)
    assert errors


def test_validate_url_string_not_url():
    url_str = 'absd'
    errors = validate_url_string(url_str)
    assert errors


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test',
        }
    }
)
def test_make_get_http_request_ok():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
    with mock.patch('requests.get') as mocked_requests:
        url = "https://www.example.com/"
        mocked_requests.return_value.status_code = 200
        mocked_requests.return_value.text = """
        <!DOCTYPE html>
        <html>
        <body>
        
        <h1>My First Heading</h1>
        <a href="link1">link1</a>
        <a href="link2">link2</a>
        <a href="link3">link3</a>
        
        </body>
        </html>
        """
        urls, response_status_code, error = make_get_http_request(url)
        assert len(urls) == 3
        assert not error
        assert response_status_code == codes.ok


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test',
        }
    }
)
def test_make_get_http_request_not_200_from_url():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
    with mock.patch('requests.get') as mocked_requests:
        url = "https://www.example.com/"
        mocked_requests.return_value.status_code = 400
        mocked_requests.return_value.text = """
        <!DOCTYPE html>
        <html>
        <body>

        <h1>My First Heading</h1>
        <a href="link1">link1</a>
        <a href="link2">link2</a>
        <a href="link3">link3</a>

        </body>
        </html>
        """
        urls, response_status_code, error = make_get_http_request(url)
        assert len(urls) == 0
        assert error == 'Error response from passed URL. Status: 400.'
        assert response_status_code == codes.bad_request


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test',
        }
    }
)
def test_make_get_http_request_not_200_from_url():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
    with mock.patch('requests.get') as mocked_requests:
        url = "https://www.example.com/"
        mocked_requests.return_value.status_code = 400
        mocked_requests.return_value.text = """
        <!DOCTYPE html>
        <html>
        <body>

        <h1>My First Heading</h1>
        <a href="link1">link1</a>
        <a href="link2">link2</a>
        <a href="link3">link3</a>

        </body>
        </html>
        """
        urls, response_status_code, error = make_get_http_request(url)
        assert len(urls) == 0
        assert error == 'Error response from passed URL. Status: 400.'
        assert response_status_code == codes.bad_request
