"""Compare the two blind raters' scores and list every disagreement.

Usage: python3 -I compare_raters.py   (run check_citations.py first)

Writes:
  data/rater_comparison.csv   one row per document x criterion, both raters side by side
  data/disagreements.csv      only the rows where scores differ, or where a quote failed the check
Prints exact agreement, within-one agreement and weighted kappa (linear weights).
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
A, B = "rater_a", "rater_b"


def wkappa(a, b, levels=(0, 1, 2)):
    k, n = len(levels), len(a)
    idx = {v: i for i, v in enumerate(levels)}
    obs = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[idx[x]][idx[y]] += 1
    ra = [sum(r) for r in obs]
    cb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    num = sum(abs(i - j) / (k - 1) * obs[i][j] / n for i in range(k) for j in range(k))
    den = sum(abs(i - j) / (k - 1) * ra[i] * cb[j] / n / n for i in range(k) for j in range(k))
    return None if den == 0 else 1 - num / den


def main():
    check = {(r["rater"], r["doc_id"], r["kind"], r["key"]): r["found_on_page"] == "True"
             for r in csv.DictReader(open(DATA / "citation_check.csv", newline=""))}
    docs = sorted({f.name.split("__")[1][:-5] for f in (DATA / "scores").glob("rater_*__*.json")})
    rows = []
    for doc in docs:
        sa = json.loads((DATA / "scores" / f"{A}__{doc}.json").read_text())["scores"]
        sb = json.loads((DATA / "scores" / f"{B}__{doc}.json").read_text())["scores"]
        for crit in sa:
            a, b = sa[crit], sb[crit]
            rows.append({
                "doc_id": doc, "criterion": crit, "a_score": a["score"], "b_score": b["score"],
                "a_page": a.get("page"), "a_quote_ok": check.get((A, doc, "score", crit), "") if a.get("quote") else "",
                "b_page": b.get("page"), "b_quote_ok": check.get((B, doc, "score", crit), "") if b.get("quote") else "",
                "a_quote": a.get("quote") or "", "b_quote": b.get("quote") or "",
                "a_reason": a.get("reason", ""), "b_reason": b.get("reason", ""),
            })
    fields = list(rows[0])
    with open(DATA / "rater_comparison.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    dis = [r for r in rows if r["a_score"] != r["b_score"] or r["a_quote_ok"] is False or r["b_quote_ok"] is False]
    with open(DATA / "disagreements.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(dis)

    a = [int(r["a_score"]) for r in rows]
    b = [int(r["b_score"]) for r in rows]
    n = len(rows)
    print(f"{n} document x criterion pairs across {len(docs)} documents")
    print(f"exact agreement {sum(x == y for x, y in zip(a, b)) / n:.0%}, within one {sum(abs(x - y) <= 1 for x, y in zip(a, b)) / n:.0%}, "
          f"weighted kappa {wkappa(a, b):.2f}")
    print(f"mean score: rater A {sum(a) / n:.2f}, rater B {sum(b) / n:.2f}")
    print(f"{len(dis)} rows need resolution (score differs or a quote failed): data/disagreements.csv")


if __name__ == "__main__":
    main()
