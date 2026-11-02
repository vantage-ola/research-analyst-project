"""Check scores_author.csv against the rubric's allowed values.

Usage: python3 -I check_scores.py
"""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
TAGS = {"payment", "connectivity", "language", "informal", "regulatory", "none"}


def main():
    rows = list(csv.DictReader(open(DATA / "scores_author.csv", newline="")))
    done, problems = 0, []
    for r in rows:
        if not r["score"]:
            continue
        done += 1
        t = r["task_id"]
        if r["score"] not in {"0", "1", "2"}:
            problems.append(f"{t}: score must be 0, 1 or 2")
        if not r["reason"].strip():
            problems.append(f"{t}: reason is empty")
        if r["confidence"] not in {"low", "med", "high"}:
            problems.append(f"{t}: confidence must be low, med or high")
        tags = {x.strip() for x in r["barrier_tags"].split(";") if x.strip()}
        if not tags or not tags <= TAGS:
            problems.append(f"{t}: barrier_tags must be ';'-separated from {sorted(TAGS)}")
        if not r["scoring_date"] or not r["model_in_mind"]:
            problems.append(f"{t}: scoring_date and model_in_mind are required")
    print(f"{done}/{len(rows)} scored")
    print("\n".join(problems) or "no problems")


if __name__ == "__main__":
    main()
