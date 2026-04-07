from utils.http import get

PAYLOAD = "<script>alert(1)</script>"

async def test_xss(endpoint):
    url = endpoint["url"]
    method = endpoint["method"]
    params = endpoint["params"]

    if not params:
        return None

    test_params = {k: PAYLOAD for k in params}

    if method == "GET":
        query = "&".join([f"{k}={v}" for k, v in test_params.items()])
        test_url = f"{url}?{query}"

        response, html = await get(test_url)

        if not response or not html:
            return None

        if PAYLOAD in html:
            return {
                "type": "XSS",
                "severity": "HIGH",
                "url": url,
                "method": method,
                "poc": test_url,
                "details": "Payload reflected in response"
            }

    elif method == "POST":
        response, html = await get(url) 

        if not response or not html:
            return None

        if PAYLOAD in html:
            return {
                "type": "XSS",
                "severity": "HIGH",
                "url": url,
                "method": method,
                "poc": f"{url} (POST)",
                "details": "Payload reflected in POST response"
            }

    return None