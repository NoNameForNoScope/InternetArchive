import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def gaseste_resurse(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    resurse = []
    for tag, attr in [("img", "src"), ("script", "src"), ("link", "href")]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val:
                resurse.append(urljoin(base_url, val))
    return resurse, soup


def gaseste_urls_css(css_text, base_url):
    urls = re.findall(r'url\((["\']?)(.*?)\1\)', css_text)
    return [urljoin(base_url, u[1]) for u in urls]
