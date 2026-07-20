from fetcher import fetch


def probeaza_wordlist(base_url, wordlist_path="wordlist.txt"):
    gasite = []
    try:
        with open(wordlist_path, encoding="utf-8") as f:
            paths = [linie.strip() for linie in f if linie.strip()]
    except FileNotFoundError:
        print(f"nu am gasit fisierul {wordlist_path}")
        return gasite

    for path in paths:
        url = base_url.rstrip("/") + path
        status, _ = fetch(url)
        if status == 200:
            gasite.append(url)
    return gasite
