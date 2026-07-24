import hashlib
import os
import threading
from urllib.parse import urlparse

from fetcher import fetch

_cache_lock = threading.Lock()
_cache = {}


def seteaza_foldere(output_dir):
    for sub in ["pages", "assets/img", "assets/css", "assets/js", "assets/doc", "logs"]:
        os.makedirs(os.path.join(output_dir, sub), exist_ok=True)


def _nume_local(url):
    ext = os.path.splitext(urlparse(url).path)[1] or ""
    hash_url = hashlib.md5(url.encode("utf-8")).hexdigest()
    return f"{hash_url}{ext}"


def _folder_pentru(url):
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"]:
        return "img"
    if ext == ".css":
        return "css"
    if ext == ".js":
        return "js"
    return "doc"


def descarca_resursa(url, output_dir):
    with _cache_lock:
        if url in _cache:
            return _cache[url], None

    status, continut = fetch(url)
    if status != 200 or continut is None:
        return None, None

    subfolder = _folder_pentru(url)
    nume_fisier = _nume_local(url)
    path_local = os.path.join(subfolder, nume_fisier).replace("\\", "/")
    path_complet = os.path.join(output_dir, "assets", path_local)

    with open(path_complet, "wb") as f:
        f.write(continut)

    with _cache_lock:
        _cache[url] = path_local

    return path_local, continut
