import hashlib
import os
from urllib.parse import urlparse

from fetcher import fetch


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
    status, continut = fetch(url)
    if status != 200 or continut is None:
        return None

    subfolder = _folder_pentru(url)
    nume_fisier = _nume_local(url)
    path_local = os.path.join("assets", subfolder, nume_fisier)
    path_complet = os.path.join(output_dir, path_local)

    with open(path_complet, "wb") as f:
        f.write(continut)

    return os.path.join("..", path_local).replace("\\", "/")
