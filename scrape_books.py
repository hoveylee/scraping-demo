#!/usr/bin/env python3
"""Scraping demo — books.toscrape.com -> books.csv

What it does: fetches the catalogue pages of books.toscrape.com
(a practice site built for learning scrapers), extracts title, price,
rating and stock status per book, and writes a CSV.

Why this site: it exists for scraping practice, so demoing against it
is fair game — no real site's terms are being bent for a portfolio demo.

Run:  python3 scrape_books.py            # page 1, 20 books
       python3 scrape_books.py --pages 3  # first 3 pages, 60 books
       python3 scrape_books.py --out my_books.csv

Only dependency: requests (pip install requests). Python 3.9+.
Politeness: 1 second between page requests, browser User-Agent,
stops on the first HTTP error instead of retrying aggressively.
"""

import argparse
import csv
import time
from html.parser import HTMLParser
from urllib.parse import urljoin

import requests

BASE = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-demo; contact via Upwork profile)"}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BookParser(HTMLParser):
    """Pulls one dict per <article class="product_pod">."""

    def __init__(self):
        super().__init__()
        self.books, self.current = [], None
        self._in_title, self._in_price, self._in_stock = False, False, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        if tag == "article" and "product_pod" in cls:
            self.current = {"title": "", "price": "", "rating": 0, "in_stock": ""}
        if self.current is None:
            return
        if tag == "a" and "title" in a:
            self.current["title"] = a["title"]
        if tag == "p" and "star-rating" in cls:
            self.current["rating"] = RATINGS.get(cls.split()[-1], 0)
        if tag == "p" and "price_color" in cls:
            self._in_price = True
        if tag == "p" and "instock" in cls:
            self._in_stock = True

    def handle_data(self, data):
        if self.current is None:
            return
        if self._in_price:
            self.current["price"] = data.strip()
        if self._in_stock and data.strip():
            self.current["in_stock"] = data.strip()

    def handle_endtag(self, tag):
        if tag == "article" and self.current:
            self.books.append(self.current)
            self.current = None
        if tag == "p":
            self._in_price = self._in_stock = False


def scrape_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    parser = BookParser()
    parser.feed(resp.text)
    return parser.books


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=1)
    ap.add_argument("--out", default="books.csv")
    args = ap.parse_args()

    all_books = []
    for page in range(1, args.pages + 1):
        url = BASE if page == 1 else urljoin(BASE, f"catalogue/page-{page}.html")
        books = scrape_page(url)
        print(f"page {page}: {len(books)} books")
        all_books.extend(books)
        time.sleep(1)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock"])
        w.writeheader()
        w.writerows(all_books)
    print(f"wrote {len(all_books)} rows -> {args.out}")


if __name__ == "__main__":
    main()
