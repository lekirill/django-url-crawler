import requests

from django.shortcuts import render
from requests import status_codes

from crawler.services import crawl_url, validate_url_string


def crawl_urls(request):
    urls = None
    if request.method == 'POST':
        url = request.POST['url']
        errors = validate_url_string(url)
        if errors:
            return render(
                request, 'go_form.html', {'error': ', '.join(err for err in errors)},
                status=status_codes.codes.bad_request
            )

        response = requests.get(url)

        if response.status_code == status_codes.codes.ok:
            urls = crawl_url(response.text)
            return render(request, 'go_form.html', {'urls': urls})
        else:
            return render(request, 'go_form.html',
                          {'error': f'Error response from passed URL. '
                                    f'Status {response.status_code}. Response: {response.json()}'},
                          status=response.status_code)

    else:
        return render(request, 'go_form.html', {'urls': urls})
