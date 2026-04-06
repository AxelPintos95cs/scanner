from crawler.crawler import crawl
from detectors.xss import test_xss
from detectors.headers import check_headers
from detectors.sqli import test_sqli

def run_scan(url: str, depth: int) -> list:
    print("[+] Crawling...")
    urls = crawl(url, depth)

    print(f"[+] Found {len(urls)} URLs")

    findings = []

    for u in urls:
        print(f"[+] Scanning {u}")

        xss = test_xss(u)
        if xss:
            findings.append(xss)

        headers = check_headers(u)
        if headers:
            findings.append(headers)

        sqli = test_sqli(u)
        if sqli:
            findings.append(sqli)

    return findings