import hashlib
import os
from collections import deque
from urllib.parse import urljoin, urlparse

from processor import proceseaza_pagina
from wordlist_probe import probeaza_wordlist


def _nume_pagina(url):
    
    return hashlib.md5(url.encode("utf-8")).hexdigest() + ".html"


def _logheaza(output_dir, mesaj):
    log_path = os.path.join(output_dir, "logs", "crawl.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(mesaj + "\n")


def crawleaza(start_url, output_dir, max_depth=2, wordlist_path="wordlist.txt"):
  
    vizitate = set([start_url])
    coada = deque([(start_url, 0)])
    domeniu = urlparse(start_url).netloc

    scheme = urlparse(start_url).scheme
    domeniu_url = f"{scheme}://{domeniu}"
    gasite = probeaza_wordlist(domeniu_url, wordlist_path)
    for url in gasite:
        if url not in vizitate:
            vizitate.add(url)
            coada.append((url, 0))

    while coada:
        url, depth = coada.popleft()

        nume_fisier = _nume_pagina(url)
        out_path, soup = proceseaza_pagina(url, output_dir, nume_fisier=nume_fisier)

        if out_path is None:
            _logheaza(output_dir, f" {url}")
            continue
        _logheaza(output_dir, f"{url} -> pages/{nume_fisier}")
        if depth < max_depth and soup is not None:
            a_rescrise = False
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if urlparse(link).netloc != domeniu:
                    continue 

                a["href"] = _nume_pagina(link)
                a_rescrise = True

                if link not in vizitate:
                    vizitate.add(link)
                    coada.append((link, depth + 1))

            if a_rescrise:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(str(soup))

    print(f"am salvat {len(vizitate)} pagini din domeniul {domeniu}")
    return vizitate
