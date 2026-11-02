"""Extract ILO Working Paper 140 Table A1 (GenAI exposure by 4-digit ISCO-08) and join our categories.

Usage: python3 -I extract_ilo.py <path to saved wp140 index.html>
Source: Gmyrek, Berg, Kamiński, Konopczyński, Ładna, Nafradi, Rosłaniec, Troszyński (2025),
"Generative AI and Jobs: A Refined Global Index of Occupational Exposure", ILO Working Paper 140,
https://webapps.ilo.org/static/english/intserv/working-papers/wp140/index.html (CC BY 4.0).

Writes data/external/ilo_wp140_table_a1.csv and data/external/ilo_category_scores.csv.
mean = mean task exposure score (0-1) for the occupation; sd = spread across its tasks.
"""
import csv
import html
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
LABEL = r"(Gradient \d|Not Exposed|Minimal Exposure)"


def main(page):
    raw = open(page, encoding="utf-8", errors="ignore").read()
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    start = text.index("Table A1. ISCO-08 occupations by exposure gradient")
    seg = text[start:text.index("2. Sampling Formula", start)]
    rows = re.findall(LABEL + r"\s+(\d{4})\s+(.+?)\s+(\d\.\d+|0|1)\s+(\d\.\d+|0)(?=\s+" + LABEL + r"|\s*$)", seg)
    table = [{"isco08": c, "occupation": n, "mean": m, "sd": s, "gradient": g} for g, c, n, m, s, _ in rows]
    with open(DATA / "external" / "ilo_wp140_table_a1.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)

    by_code = {r["isco08"]: r for r in table}
    out = []
    for c in csv.DictReader(open(DATA / "categories.csv", newline="")):
        r = by_code.get(c["isco08"], {})
        out.append({"category_id": c["category_id"], "isco08": c["isco08"], "ilo_occupation": r.get("occupation", "NOT FOUND"),
                    "ilo_mean": r.get("mean", ""), "ilo_sd": r.get("sd", ""), "ilo_gradient": r.get("gradient", "")})
    with open(DATA / "external" / "ilo_category_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{len(table)} occupations in Table A1")
    for o in out:
        print(o["category_id"], o["isco08"], o["ilo_occupation"], o["ilo_mean"], o["ilo_gradient"])


if __name__ == "__main__":
    main(sys.argv[1])
