from utils.http import get

PAYLOAD = "<script>alert(1)</script>"

def test_xss(url):
    if "?" not in url:
        return None

    test_url = url + PAYLOAD
    response = get(test_url)

    if response and PAYLOAD in response.text:
        return {
            "type": "XSS",
            "url": url,
            "severity": "HIGH"
        }

    return None