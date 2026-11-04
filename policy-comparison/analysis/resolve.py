"""Merge the two raters into final scores, applying written resolutions to every disagreement.

Usage: python3 -I resolve.py   (after check_citations.py and compare_raters.py)

Where both raters agree, the final score is theirs and the evidence is rater A's (or B's if
A's quote failed the citation check). Where they disagree, RESOLUTIONS gives the final score,
which rater's evidence it rests on, and why. Resolutions were made by reading the cited pages.

Writes data/final_scores.csv (long form) and data/matrix.csv (document x criterion).
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# (doc_id, criterion): (final score, evidence from rater, note)
RESOLUTIONS = {
    ("au_continental_ai_strategy_2024-07", "measurable_targets"): (2, "rater_a",
        "A number with a deadline meets level 2 as written. It is the AU's only numeric target and it counts forums, not outcomes."),
    ("egypt_ai_strategy_2025-2030", "responsible_body"): (2, "rater_b",
        "The National Council for AI is named with the stated duty to govern implementation, which meets level 2."),
    ("egypt_ai_strategy_2025-2030", "enforcement"): (1, "rater_a",
        "The AI law is still being drafted (p10). The penalties rater B cited belong to the data protection law, which is scored under data protection."),
    ("nigeria_nais_2025-09-19", "data_protection"): (2, "rater_a",
        "Both raters gave 2. Rater B cited p28; the quote is on p29."),
    ("rwanda_ai_policy_2023", "risk_safety"): (2, "rater_a",
        "Regulatory sandboxes giving a controlled environment to test and evaluate AI solutions (p21) are a testing measure named at level 2."),
    ("rwanda_ai_policy_2023", "local_language"): (0, "rater_a",
        "No language is mentioned. 'Tailored guidelines' are ethics guidelines, not a commitment to local language or context."),
}


# Safety-check splits: (doc_id, question): (final answer, evidence from rater or None, note).
# Rule applied to all documents: "frontier_risk" means risks specific to the most capable or
# general-purpose models (loss of control, existential or catastrophic risk), not ordinary harms
# such as privacy or bias that happen to be mentioned alongside generative AI.
SAFETY_RESOLUTIONS = {
    ("kenya_ai_strategy_2025-2030", "frontier_risk"): ("no", None,
        "p37 raises privacy concerns about generative AI, an ordinary harm, not frontier-model risk."),
    ("nigeria_nais_2025-09-19", "frontier_risk"): ("no", None,
        "p48 lists bias, misleading models and adversarial manipulation, ordinary harms of poorly built systems."),
    ("egypt_ai_strategy_2025-2030", "incident_reporting"): ("no", None,
        "p33's feedback portal is for data security breaches, not AI incidents."),
}


def safety(titles):
    out = []
    for fa in sorted((DATA / "scores").glob("rater_a__*.json")):
        a = json.loads(fa.read_text())
        b = json.loads((DATA / "scores" / fa.name.replace("rater_a", "rater_b")).read_text())
        for q, sa in a["safety"].items():
            sb = b["safety"][q]
            key = (a["doc_id"], q)
            if key in SAFETY_RESOLUTIONS:
                ans, src, note = SAFETY_RESOLUTIONS[key]
                ev = {"rater_a": sa, "rater_b": sb}.get(src, {})
            elif sa["answer"] == sb["answer"]:
                ans, ev, note = sa["answer"], sa, ""
            else:
                raise SystemExit(f"unresolved safety split: {key}")
            out.append({"doc_id": a["doc_id"], "country": titles[a["doc_id"]], "question": q, "answer": ans,
                        "rater_a": sa["answer"], "rater_b": sb["answer"],
                        "page": ev.get("page") if ans == "yes" else "", "quote": ev.get("quote") if ans == "yes" else "",
                        "resolution_note": note})
    with open(DATA / "final_safety.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print("\nSafety check (final):")
    for o in out:
        print(f"  {o['country']:<14} {o['question']:<19} {o['answer']:<4} {('p' + str(o['page'])) if o['page'] else ''}")


def main():
    titles = {r["doc_id"]: r["country"] for r in csv.DictReader(open(ROOT / "sources" / "sources.csv", newline=""))}
    out = []
    for r in csv.DictReader(open(DATA / "rater_comparison.csv", newline="")):
        key = (r["doc_id"], r["criterion"])
        if key in RESOLUTIONS:
            score, src, note = RESOLUTIONS[key]
            basis = "resolved"
        else:
            if r["a_score"] != r["b_score"] or r["a_quote_ok"] == "False" and r["b_quote_ok"] == "False":
                raise SystemExit(f"unresolved disagreement: {key}")
            score, src, note, basis = int(r["a_score"]), "rater_a" if r["a_quote_ok"] != "False" else "rater_b", "", "agreed"
        s = src[-1]
        out.append({"doc_id": r["doc_id"], "country": titles[r["doc_id"]], "criterion": r["criterion"],
                    "score": score, "basis": basis, "rater_a": r["a_score"], "rater_b": r["b_score"],
                    "page": r[f"{s}_page"], "quote": r[f"{s}_quote"], "reason": r[f"{s}_reason"], "resolution_note": note})
    with open(DATA / "final_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    crits = list(dict.fromkeys(o["criterion"] for o in out))
    docs = list(dict.fromkeys(o["doc_id"] for o in out))
    matrix = []
    for d in docs:
        row = {"country": titles[d], "doc_id": d}
        row.update({c: next(o["score"] for o in out if o["doc_id"] == d and o["criterion"] == c) for c in crits})
        row["total_of_20"] = sum(row[c] for c in crits)
        matrix.append(row)
    matrix.sort(key=lambda r: -r["total_of_20"])
    with open(DATA / "matrix.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(matrix[0]))
        w.writeheader()
        w.writerows(matrix)
    print(f"{len(out)} final scores ({sum(o['basis'] == 'resolved' for o in out)} resolved)")
    print("country".ljust(16), " ".join(c[:6].ljust(6) for c in crits), "total")
    for m in matrix:
        print(m["country"].ljust(16), " ".join(str(m[c]).ljust(6) for c in crits), m["total_of_20"])
    safety(titles)


if __name__ == "__main__":
    main()
