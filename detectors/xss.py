from utils.http import get

PAYLOAD = "<script>alert(1)</script>"

def test_xss(endpoint):
    url = endpoint["url"]
    method = endpoint["method"]
    params = endpoint["params"]

    if not params:
        return None

    injected = {k: PAYLOAD for k in params}

    if method == "GET":
        query = "&".join(f"{k}={v}" for k, v in injected.items())
        test_url = f"{url}?{query}"
        response = get(test_url)

    else:
        response = get(url)  # MVP: dejamos POST para después

    if response and PAYLOAD in response.text:
        return {
            "type": "XSS",
            "url": url,
            "method": method,
            "severity": "HIGH",
            "poc": test_url 
        }

    return None