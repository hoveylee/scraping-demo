# Scraping demo — books.toscrape.com → CSV

A small, real scraper 李浩 can link from Upwork proposals for
scraping / data-extraction jobs. It is a portfolio starter, not client
work — review it before linking, and swap in the client's own target
site when a job lands.

## What it proves

- Fetches catalogue pages, parses title / price / star rating / stock
  status per book, writes a clean CSV.
- Polite by default: 1s between requests, browser User-Agent, fails
  fast on HTTP errors instead of hammering.
- One dependency (`requests`), plain Python 3.9+.

## Run it

```
pip install requests
python3 scrape_books.py            # page 1 → books.csv (20 rows)
python3 scrape_books.py --pages 3  # first 3 pages → 60 rows
```

## Files

- `scrape_books.py` — the scraper (stdlib HTML parser + requests)
- `sample_books.csv` — real output from 2026-11-20: 40 rows, pages 1–2

## How to use it in a proposal

Link the repo/folder, or paste one line: "Sample: 40 books scraped
to CSV in ~5s, script + output here: [link]". For a live job, the
same pattern adapts to the client's site — pagination, fields and
output format change, the pipeline stays the same.

## Honest limits

- Demo target is books.toscrape.com, a practice site built for
  scrapers. Real sites need per-site handling (login, JS rendering,
  rate limits, terms) — say so in the proposal, don't oversell.
- No proxy rotation / headless browser in this version; add
  Playwright only if the job actually needs JS rendering.
