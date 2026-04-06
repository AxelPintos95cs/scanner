from crawler.crawler import crawl
from detectors.xss import test_xss
from detectors.headers import check_headers

def run_scan(url):
    print("[+] Crawling...")
    urls = crawl(url)

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

    return findings