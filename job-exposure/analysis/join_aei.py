"""Join our tasks to the Anthropic Economic Index (observed Claude usage by O*NET task).

Usage: python3 -I join_aei.py <dir with task_penetration.csv, job_exposure.csv, task_pct_v2.csv>
Source: https://huggingface.co/datasets/Anthropic/EconomicIndex
  labor_market_impacts/task_penetration.csv   (task text -> penetration)
  labor_market_impacts/job_exposure.csv       (6-digit SOC -> observed_exposure)
  release_2025_03_27/task_pct_v2.csv          (task text -> share of conversations)

The files ship without column definitions. Confirm what "penetration" and
"observed_exposure" measure against Anthropic's labor market report before citing them.
Joined on exact O*NET task text (case and whitespace normalised).
"""
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def norm(s):
    return " ".join(s.lower().split()).rstrip(".")


def main(src):
    src = Path(src)
    pen = {norm(r["task"]): r["penetration"] for r in csv.DictReader(open(src / "task_penetration.csv", newline=""))}
    pct = {norm(r["task_name"]): r["pct"] for r in csv.DictReader(open(src / "task_pct_v2.csv", newline=""))}
    job = {r["occ_code"]: r for r in csv.DictReader(open(src / "job_exposure.csv", newline=""))}

    onet = {(r["O*NET-SOC Code"], r["Task ID"]): r["Task"]
            for r in csv.DictReader(open(DATA / "external" / "onet_31_0_tasks_used.csv", newline=""))}
    cats = {r["category_id"]: r["onet_soc_closest"] for r in csv.DictReader(open(DATA / "categories.csv"))}

    out, missing = [], []
    for t in csv.DictReader(open(DATA / "tasks.csv", newline="")):
        if not t["onet_task_id"]:
            continue
        soc = cats[t["category_id"]]
        text = norm(onet[(soc, t["onet_task_id"])])
        if text not in pen and text not in pct:
            missing.append(t["task_id"])
        out.append({"task_id": t["task_id"], "onet_soc": soc, "onet_task_id": t["onet_task_id"],
                    "aei_task_penetration": pen.get(text, ""), "aei_task_pct_v2": pct.get(text, "")})
    with open(DATA / "external" / "aei_task_usage.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    occ = []
    for cid, soc in cats.items():
        r = job.get(soc[:7], {})
        occ.append({"category_id": cid, "onet_soc": soc, "aei_title": r.get("title", ""),
                    "aei_observed_exposure": r.get("observed_exposure", "")})
    with open(DATA / "external" / "aei_occupation_exposure.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(occ[0]))
        w.writeheader()
        w.writerows(occ)

    print(f"{len(out) - len(missing)}/{len(out)} tasks matched; unmatched: {missing or 'none'}")
    print(f"penetration found for {sum(1 for o in out if o['aei_task_penetration'])}, pct_v2 for {sum(1 for o in out if o['aei_task_pct_v2'])}")
    for o in occ:
        print(o["category_id"], o["onet_soc"], o["aei_title"] or "NOT FOUND", o["aei_observed_exposure"])


if __name__ == "__main__":
    main(sys.argv[1])
