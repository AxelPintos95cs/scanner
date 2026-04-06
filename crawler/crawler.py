from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.http import get

def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""

def crawl(base_url, max_depth=2):
    visited = set()
    to_visit = [(base_url, 0)]
    results = []

    base_domain = urlparse(base_url).netloc

    while to_visit:
        url, depth = to_visit.pop()

        if url in visited or depth > max_depth:
            continue

        visited.add(url)
        results.append(url)

        response = get(url)
        if not response:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link["href"])

            if is_valid(href, base_domain):
                to_visit.append((href, depth + 1))

    return results