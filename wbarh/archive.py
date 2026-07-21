import argparse

from crawler import crawleaza
from downloader import seteaza_foldere
from processor import proceseaza_pagina


def main():
    parser = argparse.ArgumentParser(description="salveaza o pagina sau un domeniu ca sa poata fi deschis offline")
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-m", "--mode", choices=["page", "domain"], default="page")
    parser.add_argument("-o", "--output", default="snapshot")
    parser.add_argument("-d", "--depth", type=int, default=2) 
    parser.add_argument("-w", "--wordlist", default="wordlist.txt")  

    args = parser.parse_args()
    seteaza_foldere(args.output)

    if args.mode == "page":
        proceseaza_pagina(args.url, args.output)
        return

    crawleaza(args.url, args.output, max_depth=args.depth, wordlist_path=args.wordlist)


if __name__ == "__main__":
    main()
