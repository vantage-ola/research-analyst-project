"""Fill onet_task_id and onet_match in data/tasks.csv from O*NET 31.0 task_statements.csv.

Usage: python3 -I map_onet.py <path to task_statements.csv>
Source: https://www.onetcenter.org/dl_files/database/db_31_0_csv/task_statements.csv

onet_match: close = same activity as the O*NET task; loose = overlaps but differs in
scope, channel or context; none = no O*NET task describes it (left blank on purpose).
"""
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

MAP = {
    "CS01": (18565, "close"), "CS02": (2579, "close"), "CS03": (2578, "close"),
    "CS04": (2579, "close"), "CS05": (18565, "loose"),
    "DA05": (11403, "loose"),
    "CW01": (22662, "close"), "CW02": (22657, "close"), "CW03": (22670, "close"),
    "CW04": (22664, "close"), "CW06": (22655, "loose"), "CW07": (22662, "loose"),
    "VA01": (2813, "close"), "VA02": (2801, "close"), "VA03": (20281, "close"),
    "VA04": (2812, "close"), "VA05": (2805, "close"), "VA06": (20284, "close"),
    "BK01": (2490, "close"), "BK02": (2503, "close"), "BK03": (2491, "close"),
    "BK04": (2492, "close"), "BK05": (2510, "close"), "BK06": (2494, "close"),
    "BK07": (18561, "close"),
    "TR01": (793, "close"), "TR02": (793, "loose"), "TR03": (793, "loose"),
    "TR04": (793, "loose"), "TR06": (790, "close"), "TR07": (802, "close"),
    "TL01": (9331, "close"), "TL02": (9331, "close"), "TL03": (9331, "close"),
    "TL04": (9337, "loose"), "TL05": (9329, "close"), "TL06": (9328, "close"),
    "TL07": (9331, "loose"),
    "GD01": (306, "close"), "GD02": (299, "loose"), "GD03": (23970, "close"),
    "GD04": (301, "loose"), "GD05": (304, "loose"), "GD07": (23971, "loose"),
    "TU01": (17037, "close"), "TU02": (17028, "close"), "TU03": (17035, "close"),
    "TU04": (17036, "loose"), "TU05": (17034, "close"), "TU06": (17027, "loose"),
    "TU07": (17026, "close"),
    "WD01": (14694, "close"), "WD02": (14707, "loose"), "WD03": (14707, "close"),
    "WD04": (14704, "loose"), "WD05": (14700, "close"), "WD06": (14729, "loose"),
    "WD07": (14706, "loose"),
    "SM05": (5438, "loose"), "SM06": (5438, "loose"),
    "SL01": (4624, "close"), "SL02": (4626, "close"), "SL03": (4629, "loose"),
    "SL04": (4628, "close"), "SL05": (4627, "close"), "SL06": (4620, "loose"),
    "SL07": (4623, "close"),
}


def main(onet_path):
    cats = {r["category_id"]: r["onet_soc_closest"] for r in csv.DictReader(open(DATA / "categories.csv"))}
    onet = {}
    for r in csv.DictReader(open(onet_path, newline="")):
        onet[(r["O*NET-SOC Code"], int(r["Task ID"]))] = r

    rows = list(csv.DictReader(open(DATA / "tasks.csv", newline="")))
    used = []
    for r in rows:
        tid, match = MAP.get(r["task_id"], (None, "none"))
        if tid is not None:
            key = (cats[r["category_id"]], tid)
            assert key in onet, f"{r['task_id']}: O*NET task {tid} not under {key[0]}"
            used.append(onet[key])
        r["onet_task_id"] = tid or ""
        r["onet_match"] = match

    fields = ["task_id", "category_id", "task", "source", "onet_task_id", "onet_match", "nigeria_adjustment"]
    with open(DATA / "tasks.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r[k] for k in fields} for r in rows)

    uniq = {(u["O*NET-SOC Code"], u["Task ID"]): u for u in used}.values()
    with open(DATA / "external" / "onet_31_0_tasks_used.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["O*NET-SOC Code", "Title", "Task ID", "Task", "Task Type", "Domain Source"])
        w.writeheader()
        w.writerows({k: u[k] for k in w.fieldnames} for u in uniq)


if __name__ == "__main__":
    main(sys.argv[1])
