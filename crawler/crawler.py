from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from utils.http import get


def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""


def extract_params_from_url(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    return {k: "test" for k in params}


def crawl(base_url, max_depth=2):
    visited = set()
    to_visit = [(base_url, 0)]
    endpoints = []

    base_domain = urlparse(base_url).netloc

    while to_visit:
        url, depth = to_visit.pop()

        if url in visited or depth > max_depth:
            continue

        visited.add(url)

        print(f"[DEBUG] Visiting: {url}")

        response = get(url)
        if not response or not response.text:
            continue

        # print(response.status_code)
        # print(response.text[:500])

        soup = BeautifulSoup(response.text, "html.parser")

        endpoints.append({
            "url": url,
            "method": "GET",
            "params": extract_params_from_url(url)
        })

        for link in soup.find_all("a", href=True):
            href = urljoin(url, link["href"])

            if not is_valid(href, base_domain):
                continue

            print(f"[DEBUG] Found link: {href}")

            params = extract_params_from_url(href)

            endpoint = {
                "url": href.split("?")[0],
                "method": "GET",
                "params": params
            }

            endpoints.append(endpoint)
            to_visit.append((href, depth + 1))

        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "get").upper()

            if not action:
                continue

            form_url = urljoin(url, action)

            params = {}

            for input_tag in form.find_all("input"):
                name = input_tag.get("name")
                if name:
                    params[name] = "test"

            print(f"[DEBUG] Found form: {form_url} [{method}]")

            endpoint = {
                "url": form_url,
                "method": method,
                "params": params
            }

            endpoints.append(endpoint)

    return endpoints

