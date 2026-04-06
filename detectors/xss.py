from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.http import get

PAYLOAD = "<script>alert(1)</script>"

def inject_payload(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        return None

    injected_params = {}

    for key in params:
        injected_params[key] = PAYLOAD

    new_query = urlencode(injected_params, doseq=True)

    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    return new_url


def test_xss(url):
    injected_url = inject_payload(url)

    if not injected_url:
        return None

    response = get(injected_url)

    if response and PAYLOAD in response.text:
        return {
            "type": "XSS",
            "url": url,
            "tested_url": injected_url,
            "severity": "HIGH"
        }

    return None