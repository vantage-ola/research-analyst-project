"""Agreement between raters, model results, and the ranked category table.

Usage: python3 -I analysis.py

Reads (all under data/): scores_author.csv, scores_claude.csv, model_ratings.csv,
model_ratings_claude.csv, model_ratings_key.csv, tasks.csv, categories.csv, external/*.
Writes (under output/): ranked_table.csv, task_disagreements.csv, model_results.csv,
tested_vs_scored.csv, summary.md.

Run it only after BOTH raters have finished: it reads the model key.
Scores are 0 to 2 (exposure); ratings are 1 to 4 (output quality). Weighted kappa uses linear weights.
"""
import csv
import statistics as st
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output"


def rows(name):
    return list(csv.DictReader(open(DATA / name, newline="")))


def wkappa(a, b, levels):
    k = len(levels)
    idx = {v: i for i, v in enumerate(levels)}
    n = len(a)
    obs = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[idx[x]][idx[y]] += 1
    ra = [sum(r) for r in obs]
    cb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = abs(i - j) / (k - 1)
            num += w * obs[i][j] / n
            den += w * ra[i] * cb[j] / n / n
    return None if den == 0 else 1 - num / den


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return None if den == 0 else num / den


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(st.mean(xs), 2) if xs else None


def write(name, data):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)


def main():
    OUT.mkdir(exist_ok=True)
    tasks = {r["task_id"]: r for r in rows("tasks.csv")}
    cats = {r["category_id"]: r for r in rows("categories.csv")}
    me = {r["task_id"]: int(r["score"]) for r in rows("scores_author.csv")}
    cl = {r["task_id"]: int(r["score"]) for r in rows("scores_claude.csv")}
    ids = list(tasks)
    s = [];  md = []

    # 1. Agreement on task scores
    a, b = [me[t] for t in ids], [cl[t] for t in ids]
    exact = sum(x == y for x, y in zip(a, b)) / len(ids)
    within1 = sum(abs(x - y) <= 1 for x, y in zip(a, b)) / len(ids)
    k_scores = wkappa(a, b, [0, 1, 2])
    md += ["## Task scores: author vs Claude (84 tasks)", "",
           f"- Exact agreement: {exact:.0%}; within one point: {within1:.0%}; weighted kappa: {k_scores:.2f}",
           f"- Mean score (0-2): author {st.mean(a):.2f}, Claude {st.mean(b):.2f}",
           f"- Author scored higher on {sum(x > y for x, y in zip(a, b))} tasks, Claude on {sum(y > x for x, y in zip(a, b))}", ""]
    diffs = [{"task_id": t, "category_id": tasks[t]["category_id"], "task": tasks[t]["task"], "author": me[t],
              "claude": cl[t], "gap": me[t] - cl[t]} for t in ids if me[t] != cl[t]]
    diffs.sort(key=lambda d: (-abs(d["gap"]), d["task_id"]))
    write("task_disagreements.csv", diffs)

    # 2. Output ratings, unblinded
    key = {r["blind_id"]: r for r in rows("model_ratings_key.csv")}
    mr = {r["blind_id"]: int(r["rating"]) for r in rows("model_ratings.csv")}
    cr = {r["blind_id"]: int(r["rating"]) for r in rows("model_ratings_claude.csv")}
    bids = sorted(mr)
    ra, rb = [mr[x] for x in bids], [cr[x] for x in bids]
    k_rat = wkappa(ra, rb, [1, 2, 3, 4])
    md += ["## Output ratings: author vs Claude (66 outputs)", "",
           f"- Exact agreement: {sum(x == y for x, y in zip(ra, rb)) / len(bids):.0%}; within one point: "
           f"{sum(abs(x - y) <= 1 for x, y in zip(ra, rb)) / len(bids):.0%}; weighted kappa: {k_rat:.2f}",
           f"- Mean rating (1-4): author {st.mean(ra):.2f}, Claude {st.mean(rb):.2f}",
           f"- Rating distribution, author: {dict(sorted({v: ra.count(v) for v in set(ra)}.items()))}; "
           f"Claude: {dict(sorted({v: rb.count(v) for v in set(rb)}.items()))}",
           "- Kappa is unreliable when one rater uses a narrow range of the scale; read it with the exact-agreement figure.", ""]

    by_model = defaultdict(list)
    for x in bids:
        by_model[key[x]["model"]].append(x)
    mres = []
    for m, bs in sorted(by_model.items()):
        mres.append({"model": m, "n": len(bs), "author_mean": mean([mr[x] for x in bs]),
                     "claude_mean": mean([cr[x] for x in bs]),
                     "author_pct_client_ready": f"{sum(mr[x] == 4 for x in bs) / len(bs):.0%}",
                     "claude_pct_client_ready": f"{sum(cr[x] == 4 for x in bs) / len(bs):.0%}"})
    write("model_results.csv", mres)
    md += ["### By model (unblinded)", "", "| Model | n | Author mean | Claude mean | Author % client-ready | Claude % client-ready |", "|---|---|---|---|---|---|"]
    md += [f"| {m['model']} | {m['n']} | {m['author_mean']} | {m['claude_mean']} | {m['author_pct_client_ready']} | {m['claude_pct_client_ready']} |" for m in mres]
    md += ["", "Caveat: Claude rated outputs that include its own model family. The author rated blind; Claude rated blind to model names but could not be blind to its own style. Treat model-vs-model differences as indicative only (22 tasks, one run each).", ""]

    # 3. Tested tasks: prior score vs tested quality
    by_task = defaultdict(list)
    for x in bids:
        by_task[key[x]["task_id"]].append(x)
    tv = []
    for t, bs in sorted(by_task.items()):
        tv.append({"task_id": t, "category_id": tasks[t]["category_id"], "task": tasks[t]["task"],
                   "author_score": me[t], "claude_score": cl[t],
                   "author_mean_rating": mean([mr[x] for x in bs]), "claude_mean_rating": mean([cr[x] for x in bs])})
    write("tested_vs_scored.csv", tv)
    under = [r for r in tv if r["author_score"] <= 1 and r["author_mean_rating"] >= 3.5]
    over = [r for r in tv if r["author_score"] == 2 and r["author_mean_rating"] < 3.5]
    md += ["## Prior scores vs tested quality (22 tested tasks)", "",
           f"- Author scored 'partly or not exposed' (0-1) but outputs averaged 3.5+ out of 4: {len(under)} tasks ({', '.join(r['task_id'] for r in under) or 'none'})",
           f"- Author scored 'largely exposed' (2) but outputs averaged under 3.5: {len(over)} tasks ({', '.join(r['task_id'] for r in over) or 'none'})",
           f"- Spearman between author score and mean author rating across the 22 tasks: {spearman([r['author_score'] for r in tv], [r['author_mean_rating'] for r in tv]):.2f}", ""]

    # 4. Category table vs published measures
    g = {r["task_id"]: r for r in rows("external/gpts_task_labels.csv")}
    ilo = {r["category_id"]: r for r in rows("external/ilo_category_scores.csv")}
    aeo = {r["category_id"]: r for r in rows("external/aei_occupation_exposure.csv")}
    aei_t = {r["task_id"]: r for r in rows("external/aei_task_usage.csv")}
    table = []
    for c in cats:
        ts = [t for t in ids if tasks[t]["category_id"] == c]
        gt = [t for t in ts if t in g]
        table.append({
            "category_id": c, "category": cats[c]["category"],
            "author_mean_0_2": mean([me[t] for t in ts]), "claude_mean_0_2": mean([cl[t] for t in ts]),
            "tested_rating_author_1_4": mean([mr[x] for t in ts for x in by_task.get(t, [])]),
            "gpts_human_beta_0_1": mean([float(g[t]["human_beta"]) for t in gt]),
            "gpts_gpt4_beta_0_1": mean([float(g[t]["gpt4_beta"]) for t in gt]),
            "gpts_tasks_matched": len(gt),
            "ilo_mean_0_1": float(ilo[c]["ilo_mean"]), "ilo_gradient": ilo[c]["ilo_gradient"],
            "aei_observed_exposure_0_1": float(aeo[c]["aei_observed_exposure"]),
            "aei_task_penetration": mean([float(aei_t[t]["aei_task_penetration"]) for t in ts if t in aei_t and aei_t[t]["aei_task_penetration"]]),
        })
    table.sort(key=lambda r: -r["author_mean_0_2"])
    for i, r in enumerate(table, 1):
        r["rank_by_author"] = i
    write("ranked_table.csv", table)
    md += ["## Ranked table (by author mean exposure)", "",
           "| # | Category | Author (0-2) | Claude (0-2) | Tested rating (1-4) | GPTs human (0-1) | GPTs n | ILO (0-1) | AEI observed (0-1) |", "|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {r['rank_by_author']} | {r['category']} | {r['author_mean_0_2']} | {r['claude_mean_0_2']} | {r['tested_rating_author_1_4'] or '-'} | {r['gpts_human_beta_0_1']} | {r['gpts_tasks_matched']} | {r['ilo_mean_0_1']} | {r['aei_observed_exposure_0_1']} |" for r in table]
    md += ["", "### Rank correlation of category scores (Spearman, 12 categories)", ""]
    series = {"Author": [r["author_mean_0_2"] for r in table], "Claude": [r["claude_mean_0_2"] for r in table],
              "ILO": [r["ilo_mean_0_1"] for r in table], "AEI observed": [r["aei_observed_exposure_0_1"] for r in table]}
    for (n1, x), (n2, y) in combinations(series.items(), 2):
        md.append(f"- {n1} vs {n2}: {spearman(x, y):.2f}")
    md += ["", "GPTs-are-GPTs is left out of the correlation table: it covers 1 to 2 mapped tasks for data annotation and social media management, so category means are not comparable.", ""]

    (OUT / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
