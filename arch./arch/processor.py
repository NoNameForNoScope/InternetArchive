import os

from downloader import descarca_resursa
from extractor import gaseste_resurse, gaseste_urls_css
from fetcher import fetch
from rewriter import rescrie_css, rescrie_linkuri


def proceseaza_pagina(url, output_dir, nume_fisier="index.html"):
    status, html = fetch(url)
    if status != 200 or html is None:
        print(f"nu am putut descarca {url} (status: {status})")
        return None, None

    html_text = html.decode("utf-8", errors="ignore")
    resurse, soup = gaseste_resurse(html_text, url)

    url_to_local = {}
    for resurs_url in resurse:
        path_assets, continut = descarca_resursa(resurs_url, output_dir)
        if not path_assets:
            print(f"nu am putut descarca resursa: {resurs_url}")
            continue

        url_to_local[resurs_url] = "../assets/" + path_assets

        if resurs_url.endswith(".css") and continut is not None:
            css_text = continut.decode("utf-8", errors="ignore")
            css_raw_to_local = {}
            for raw, css_url in gaseste_urls_css(css_text, resurs_url):
                css_path_assets, _ = descarca_resursa(css_url, output_dir)
                if css_path_assets:
                    css_raw_to_local[raw] = "../" + css_path_assets

            if css_raw_to_local:
                css_rescris = rescrie_css(css_text, css_raw_to_local)
                css_local_path = os.path.join(output_dir, "assets", path_assets)
                with open(css_local_path, "w", encoding="utf-8") as f:
                    f.write(css_rescris)

    for style_tag in soup.find_all("style"):
        css_text = style_tag.string
        if not css_text:
            continue
        inline_raw_to_local = {}
        for raw, css_url in gaseste_urls_css(css_text, url):
            path_assets, _ = descarca_resursa(css_url, output_dir)
            if path_assets:
                inline_raw_to_local[raw] = "../assets/" + path_assets
        if inline_raw_to_local:
            style_tag.string = rescrie_css(css_text, inline_raw_to_local)

    html_rescris = rescrie_linkuri(soup, url_to_local, url)

    out_path = os.path.join(output_dir, "pages", nume_fisier)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_rescris)

    print(f"pagina salvata in {out_path}")
    print(f"{len(url_to_local)}/{len(resurse)} resurse descarcate cu succes")
    return out_path, soup
