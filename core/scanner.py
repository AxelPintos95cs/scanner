from crawler.crawler import crawl
from detectors.xss import test_xss
from detectors.headers import check_headers
from detectors.sqli import test_sqli

import asyncio

async def test_endpoint(e):
    results = []

    xss = await test_xss(e)
    if xss:
        results.append(xss)

    sqli = await test_sqli(e)
    if sqli:
        results.append(sqli)

    headers = await check_headers(e["url"])
    if headers:
        results.append(headers)

    return results


async def run_scan(url: str, depth: int) -> list:
    print("[+] Crawling...")
    endpoints = await crawl(url, depth)

    print(f"[+] Found {len(endpoints)} endpoints")

    seen_endpoints = set()
    unique_endpoints = []

    for e in endpoints:
        key = (
            e["method"],
            e["url"],
            tuple(sorted(e["params"].keys()))
        )

        if key not in seen_endpoints:
            seen_endpoints.add(key)
            unique_endpoints.append(e)

    print(f"[+] Testing {len(unique_endpoints)} unique endpoints")

    tasks = [test_endpoint(e) for e in unique_endpoints]

    results = await asyncio.gather(*tasks)

    findings = [f for sublist in results for f in sublist if f]

    unique_findings = []
    seen_findings = set()

    for f in findings:
        key = (f["type"], f["url"], f.get("method"))

        if key not in seen_findings:
            seen_findings.add(key)
            unique_findings.append(f)

    return unique_findings