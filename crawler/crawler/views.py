from django.shortcuts import render
from django.core.cache import cache
from requests import status_codes

from crawler.services import validate_url_string, make_get_http_request


def crawl_urls(request):
    template_params = {}
    response_status_code = status_codes.codes.ok

    if request.method == 'POST':
        url = request.POST['url']
        if cache.get(url):
            template_params['urls'] = cache.get(url)
        else:
            errors = validate_url_string(url)
            if errors:
                template_params['error'] = ', '.join(err for err in errors)
                response_status_code = status_codes.codes.bad_request
            else:
                template_params['urls'], response_status_code, template_params['error'] = make_get_http_request(url)

    return render(request, 'go_form.html', template_params, status=response_status_code)
