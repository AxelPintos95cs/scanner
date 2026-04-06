import requests

def get(url):
    try:
        return requests.get(url, timeout=5)
    except requests.RequestException:
        return None