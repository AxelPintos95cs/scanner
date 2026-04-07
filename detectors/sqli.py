from utils.http import get

PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1"
]

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "syntax error",
    "unclosed quotation",
    "quoted string not properly terminated",
    "pg_query",
    "ora-",
    "sqlite",
    "odbc",
    "jdbc"
]


async def test_sqli(endpoint):
    url = endpoint["url"]
    method = endpoint["method"]
    params = endpoint["params"]

    if not params:
        return None

    for payload in PAYLOADS:
        test_params = {k: payload for k in params}

        if method == "GET":
            query = "&".join([f"{k}={v}" for k, v in test_params.items()])
            test_url = f"{url}?{query}"

            response, html = await get(test_url)

            if not response or not html:
                continue

            content = html.lower()

            for error in SQL_ERRORS:
                if error in content:
                    return {
                        "type": "SQL Injection",
                        "severity": "HIGH",
                        "url": url,
                        "method": method,
                        "poc": test_url,
                        "details": f"SQL error detected: {error}"
                    }

        elif method == "POST":
            response, html = await get(url)

            if not response or not html:
                continue

            content = html.lower()

            for error in SQL_ERRORS:
                if error in content:
                    return {
                        "type": "SQL Injection",
                        "severity": "HIGH",
                        "url": url,
                        "method": method,
                        "poc": f"{url} (POST)",
                        "details": f"SQL error detected: {error}"
                    }

    return None