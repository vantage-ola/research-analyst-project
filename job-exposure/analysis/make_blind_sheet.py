"""Build the blind rating sheet from runs.jsonl.

Usage: python3 -I make_blind_sheet.py

Writes:
  data/model_ratings.csv      shuffled outputs with no model names; you fill in rating and comment
  data/model_ratings_key.csv  blind_id -> model. Do not open it until every rating is in.

Refuses to run if model_ratings.csv already has ratings, so it can't scramble finished work.
"""
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 20261102


def main():
    sheet = DATA / "model_ratings.csv"
    if sheet.exists() and any(r["rating"] for r in csv.DictReader(open(sheet, newline=""))):
        raise SystemExit("model_ratings.csv already has ratings; not overwriting")

    prompts = json.load(open(DATA / "model_runs" / "test_prompts.json"))
    notes = {t["task_id"]: t["rater_notes"] for t in prompts["tasks"]}
    task_text = {r["task_id"]: r["task"] for r in csv.DictReader(open(DATA / "tasks.csv", newline=""))}

    runs = [json.loads(l) for l in open(DATA / "model_runs" / "runs.jsonl")]
    runs = [r for r in runs if not r.get("error") and r.get("response")]
    random.Random(SEED).shuffle(runs)

    with open(sheet, "w", newline="") as f, open(DATA / "model_ratings_key.csv", "w", newline="") as k:
        w = csv.writer(f)
        w.writerow(["blind_id", "task_id", "task", "input", "response", "rater_notes", "rating", "comment"])
        kw = csv.writer(k)
        kw.writerow(["blind_id", "task_id", "model", "finish_reason"])
        for n, r in enumerate(runs, 1):
            bid = f"B{n:03d}"
            w.writerow([bid, r["task_id"], task_text.get(r["task_id"], ""), r["input"],
                        r["response"], notes.get(r["task_id"], ""), "", ""])
            kw.writerow([bid, r["task_id"], r["model"], r.get("finish_reason")])
    print(f"{len(runs)} outputs in model_ratings.csv")


if __name__ == "__main__":
    main()
