from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.http import get

def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""

def crawl(base_url):
    visited = set()
    to_visit = [base_url]
    results = []

    base_domain = urlparse(base_url).netloc

    while to_visit:
        url = to_visit.pop()
        
        if url in visited:
            continue
        
        visited.add(url)

        response = get(url)
        if not response:
            continue

        results.append(url)

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link["href"])

            if is_valid(href, base_domain) and href not in visited:
                to_visit.append(href)

    return results