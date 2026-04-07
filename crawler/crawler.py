from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urldefrag
from utils.http import get


def is_valid(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""


def is_interesting(url):
    blacklist = (".jpg", ".png", ".gif", ".css", ".js", ".pdf", ".xls", ".zip")
    return not url.lower().endswith(blacklist)


def extract_params_from_url(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return {k: "test" for k in params}


async def crawl(base_url, max_depth=2):
    visited = set()
    seen_endpoints = set()
    to_visit = [(base_url, 0)]
    endpoints = []

    base_domain = urlparse(base_url).netloc

    while to_visit:
        url, depth = to_visit.pop()

        if url in visited or depth > max_depth:
            continue

        visited.add(url)

        print(f"[DEBUG] Visiting: {url}")

        response, html = await get(url)
        if not response or not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        base_endpoint = (
            "GET",
            url,
            tuple(sorted(extract_params_from_url(url).keys()))
        )

        if base_endpoint not in seen_endpoints:
            seen_endpoints.add(base_endpoint)

            endpoints.append({
                "url": url,
                "method": "GET",
                "params": extract_params_from_url(url)
            })

        for link in soup.find_all("a", href=True):
            href = urljoin(url, link["href"])

            href, _ = urldefrag(href)

            if not is_valid(href, base_domain):
                continue

            if not is_interesting(href):
                continue

            print(f"[DEBUG] Found link: {href}")

            params = extract_params_from_url(href)

            endpoint_key = (
                "GET",
                href.split("?")[0],
                tuple(sorted(params.keys()))
            )

            if endpoint_key not in seen_endpoints:
                seen_endpoints.add(endpoint_key)

                endpoints.append({
                    "url": href.split("?")[0],
                    "method": "GET",
                    "params": params
                })

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

            endpoint_key = (
                method,
                form_url,
                tuple(sorted(params.keys()))
            )

            if endpoint_key not in seen_endpoints:
                seen_endpoints.add(endpoint_key)

                print(f"[DEBUG] Found form: {form_url} [{method}]")

                endpoints.append({
                    "url": form_url,
                    "method": method,
                    "params": params
                })

    return endpoints