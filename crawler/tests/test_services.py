from crawler.services import crawl_url, validate_url_string


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
    urls = crawl_url(page_text)
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
