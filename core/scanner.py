from crawler.crawler import crawl
from detectors.xss import test_xss
from detectors.headers import check_headers
from detectors.sqli import test_sqli


def run_scan(url: str, depth: int) -> list:
    print("[+] Crawling...")
    endpoints = crawl(url, depth)

    print(f"[+] Found {len(endpoints)} endpoints")

    findings = []
    seen_endpoints = set()

    for e in endpoints:
        key = (
            e["method"],
            e["url"],
            tuple(sorted(e["params"].keys()))
        )

        if key in seen_endpoints:
            continue

        seen_endpoints.add(key)

        print(f"[+] Testing {e['method']} {e['url']}")

        xss = test_xss(e)
        if xss:
            findings.append(xss)

        sqli = test_sqli(e)
        if sqli:
            findings.append(sqli)

        headers = check_headers(e["url"])
        if headers:
            findings.append(headers)

    unique_findings = []
    seen_findings = set()

    for f in findings:
        key = (f["type"], f["url"], f.get("method"))

        if key not in seen_findings:
            seen_findings.add(key)
            unique_findings.append(f)

    return unique_findings