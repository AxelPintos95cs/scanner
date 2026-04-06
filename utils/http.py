import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9"
}

def get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=5)
    except requests.RequestException:
        return None