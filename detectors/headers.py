from utils.http import get

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options"
]

def check_headers(url):
    response = get(url)
    if not response:
        return []

    missing = []

    for header in SECURITY_HEADERS:
        if header not in response.headers:
            missing.append(header)

    if missing:
        return {
            "type": "Missing Security Headers",
            "url": url,
            "severity": "MEDIUM",
            "details": missing
        }

    return None