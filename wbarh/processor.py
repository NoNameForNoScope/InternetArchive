import os

from downloader import descarca_resursa
from extractor import gaseste_resurse
from fetcher import fetch
from rewriter import rescrie_linkuri


def proceseaza_pagina(url, output_dir, nume_fisier="index.html"):
    status, html = fetch(url)
    if status != 200 or html is None:
        print(f"nu am putut descarca {url} (status: {status})")
        return None, None

    html_text = html.decode("utf-8", errors="ignore")
    resurse, soup = gaseste_resurse(html_text, url)

    url_to_local = {}
    for resurs_url in resurse:
        local_path = descarca_resursa(resurs_url, output_dir)
        if local_path:
            url_to_local[resurs_url] = local_path
        else:
            print(f"nu am putut descarca resursa: {resurs_url}")

    html_rescris = rescrie_linkuri(soup, url_to_local, url)

    out_path = os.path.join(output_dir, "pages", nume_fisier)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_rescris)

    print(f"pagina salvata in {out_path}")
    print(f"{len(url_to_local)}/{len(resurse)} resurse descarcate cu succes")
    return out_path, soup
