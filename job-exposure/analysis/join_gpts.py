"""Join our tasks to Eloundou et al. "GPTs are GPTs" task-level exposure labels.

Usage: python3 -I join_gpts.py <dir with full_labelset.tsv and occ_level.csv>
Source: https://github.com/openai/GPTs-are-GPTs/tree/main/data

Writes data/external/gpts_task_labels.csv (one row per our task with an O*NET task ID)
and data/external/gpts_occupation_scores.csv (our 12 occupations).

Labels: E0 no exposure, E1 direct exposure (LLM alone cuts time by half or more at the
same quality), E2 exposure with software built on an LLM. beta = E1 + 0.5 * E2.
"""
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
BETA = {"E0": 0.0, "E1": 1.0, "E2": 0.5}


def main(src):
    src = Path(src)
    labels = {}
    for r in csv.DictReader(open(src / "full_labelset.tsv", newline=""), delimiter="\t"):
        labels[(r["O*NET-SOC Code"], int(float(r["Task ID"])))] = r
    cats = {r["category_id"]: r["onet_soc_closest"] for r in csv.DictReader(open(DATA / "categories.csv"))}

    out, missing = [], []
    for t in csv.DictReader(open(DATA / "tasks.csv", newline="")):
        if not t["onet_task_id"]:
            continue
        soc = cats[t["category_id"]]
        g = labels.get((soc, int(t["onet_task_id"])))
        if g is None:
            missing.append(t["task_id"])
            continue
        out.append({
            "task_id": t["task_id"], "onet_soc": soc, "onet_task_id": t["onet_task_id"],
            "onet_match": t["onet_match"],
            "human_exposure": g["human_exposure_agg"], "gpt4_exposure": g["gpt4_exposure"],
            "human_beta": BETA[g["human_exposure_agg"]], "gpt4_beta": BETA[g["gpt4_exposure"]],
        })
    with open(DATA / "external" / "gpts_task_labels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    socs = set(cats.values())
    occ = [r for r in csv.DictReader(open(src / "occ_level.csv", newline="")) if r["O*NET-SOC Code"] in socs]
    with open(DATA / "external" / "gpts_occupation_scores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(occ[0]))
        w.writeheader()
        w.writerows(occ)

    print(f"{len(out)} tasks joined; no GPTs label for: {missing or 'none'}")
    print(f"{len(occ)}/{len(socs)} occupations found; missing: {sorted(socs - {r['O*NET-SOC Code'] for r in occ}) or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1])
