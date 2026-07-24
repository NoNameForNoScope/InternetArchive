import requests


def fetch(url, timeout=10):
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code, resp.content
    except requests.RequestException as e:
        print(f"fetch a esuat pentru {url}: {e}")
        return None, None