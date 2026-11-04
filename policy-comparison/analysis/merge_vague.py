"""Merge both raters' vague-commitment lists into one de-duplicated list per document.

Usage: python3 -I merge_vague.py

Two items are the same commitment when they cite the same page and share at least half of
their words. Items both raters flagged are marked "both"; the rest "rater_a" or "rater_b".
Writes data/vague_commitments.csv.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def words(s):
    return set(re.findall(r"[a-z]{3,}", s.lower()))


def same(x, y):
    if x["page"] != y["page"]:
        return False
    a, b = words(x["quote"]), words(y["quote"])
    return bool(a and b) and len(a & b) / min(len(a), len(b)) >= 0.5


def main():
    titles = {r["doc_id"]: r["country"] for r in csv.DictReader(open(ROOT / "sources" / "sources.csv", newline=""))}
    out = []
    for fa in sorted((DATA / "scores").glob("rater_a__*.json")):
        a = json.loads(fa.read_text())
        b = json.loads((DATA / "scores" / fa.name.replace("rater_a", "rater_b")).read_text())
        merged = [dict(v, flagged_by="rater_a") for v in a["vague_commitments"]]
        for v in b["vague_commitments"]:
            hit = next((m for m in merged if same(m, v)), None)
            if hit:
                hit["flagged_by"] = "both"
                hit["missing"] = sorted(set(hit["missing"]) | set(v["missing"]))
            else:
                merged.append(dict(v, flagged_by="rater_b"))
        for m in sorted(merged, key=lambda m: (m["flagged_by"] != "both", m["page"])):
            out.append({"doc_id": a["doc_id"], "country": titles[a["doc_id"]], "page": m["page"],
                        "quote": m["quote"], "missing": ";".join(sorted(m["missing"])), "flagged_by": m["flagged_by"]})
    with open(DATA / "vague_commitments.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for c in dict.fromkeys(o["country"] for o in out):
        rows = [o for o in out if o["country"] == c]
        print(f"{c}: {len(rows)} items, {sum(o['flagged_by'] == 'both' for o in rows)} flagged by both")


if __name__ == "__main__":
    main()
