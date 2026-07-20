from urllib.parse import urljoin


def rescrie_linkuri(soup, url_to_local, base_url):
    for tag, attr in [("img", "src"), ("script", "src"), ("link", "href")]:
        for el in soup.find_all(tag):
            val = el.get(attr)
            if not val:
                continue
            abs_url = urljoin(base_url, val)
            if abs_url in url_to_local:
                el[attr] = url_to_local[abs_url]
    return str(soup)
