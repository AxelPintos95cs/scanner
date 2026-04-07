from utils.http import get


SECURITY_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-Content-Type-Options"
]


async def check_headers(url):
    response, _ = await get(url) 

    if not response:
        return None

    missing = []

    for header in SECURITY_HEADERS:
        if header not in response.headers:
            missing.append(header)

    if missing:
        return {
            "type": "Missing Security Headers",
            "severity": "MEDIUM",
            "url": url,
            "details": f"Missing: {', '.join(missing)}"
        }

    return None