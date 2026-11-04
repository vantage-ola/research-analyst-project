"""Check that every quote a rater gives appears on the page it cites.

Usage: python3 -I check_citations.py

Reads data/scores/<rater>__<doc>.json and sources/text/<doc>/p###.txt.
Writes data/citation_check.csv: one row per quote with found_on_page / found_elsewhere.

Matching ignores case, whitespace, hyphens (PDFs split words like "monitor-/ing" and
"Well-/crafted" across lines), and curly vs straight quotes. Every letter must still match:
a paraphrase fails.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXT = ROOT / "sources" / "text"


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                                   "–": "-", "—": "-", "•": " "}))
    s = re.sub(r"-\s*\n\s*", "", s)          # words split across lines
    s = s.replace("-", "")                    # so "Well-crafted" and "Well-\ncrafted" match
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def pages(doc_id):
    return {int(p.stem[1:]): norm(p.read_text()) for p in (TEXT / doc_id).glob("p*.txt")}


def items(data):
    for k, v in data["scores"].items():
        yield "score", k, v.get("page"), v.get("quote")
    for i, v in enumerate(data.get("vague_commitments", [])):
        yield "vague", str(i), v.get("page"), v.get("quote")
    for k, v in data.get("safety", {}).items():
        yield "safety", k, v.get("page"), v.get("quote")


def main():
    rows, cache = [], {}
    for f in sorted((DATA / "scores").glob("*__*.json")):
        data = json.loads(f.read_text())
        doc = data["doc_id"]
        pg = cache.setdefault(doc, pages(doc))
        for kind, key, page, quote in items(data):
            if not quote:
                continue
            q = norm(quote).strip(' ."\'')
            on_page = page in pg and q in pg[page]
            elsewhere = [] if on_page else [p for p, t in pg.items() if q in t]
            rows.append({"rater": data["rater"], "doc_id": doc, "kind": kind, "key": key, "page": page,
                         "found_on_page": on_page, "found_on_other_pages": ";".join(map(str, elsewhere)),
                         "quote": quote})
    with open(DATA / "citation_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    ok = sum(r["found_on_page"] for r in rows)
    moved = sum(1 for r in rows if not r["found_on_page"] and r["found_on_other_pages"])
    print(f"{len(rows)} quotes: {ok} on the cited page, {moved} on a different page, {len(rows) - ok - moved} not found")
    for r in rows:
        if not r["found_on_page"]:
            print(f"  {r['rater']} {r['doc_id'][:12]} {r['kind']}:{r['key']} p{r['page']} "
                  f"{'-> p' + r['found_on_other_pages'] if r['found_on_other_pages'] else 'NOT FOUND'} | {r['quote'][:70]}")


if __name__ == "__main__":
    main()
