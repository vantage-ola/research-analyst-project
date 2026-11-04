"""Score each policy document with independent AI raters, each in a fresh, empty session.

Usage:
    python3 -I score_docs.py --dry-run
    python3 -I score_docs.py            # runs every rater x document not yet done; safe to re-run

Each call gets only the rubric (data/rubric.md), the output format, and the document's
page-numbered text. No tools, no settings, no other context, and no rater sees another's scores.
Raw replies go to data/scores/raw/<rater>__<doc>.json and parsed JSON to data/scores/<rater>__<doc>.json.
"""
import argparse
import csv
import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC = ROOT / "sources"
OUT = DATA / "scores"
RATERS = {"rater_a": "claude-opus-5-5", "rater_b": "claude-sonnet-5-5"}
CRITERIA = ["binding_force", "responsible_body", "funding", "measurable_targets", "jobs_workforce",
            "risk_safety", "data_protection", "enforcement", "local_language", "monitoring_evaluation"]

SYSTEM = "You are a careful policy analyst. You score documents strictly against a rubric and cite exact evidence."

FORMAT = """Return ONLY a JSON object, no other text, in this shape:
{
  "scores": {
    "<criterion>": {"score": 0|1|2, "page": <int or null>, "quote": "<exact words or null>", "reason": "<one sentence>"}
  },
  "vague_commitments": [{"page": <int>, "quote": "<exact words>", "missing": ["owner"|"number"|"date"|"money", ...]}],
  "safety": {
    "frontier_risk": {"answer": "yes"|"no", "page": <int or null>, "quote": "<exact words or null>"},
    "model_evaluation": {...same...},
    "incident_reporting": {...same...}
  }
}
Use exactly these criterion keys, in rubric order: """ + ", ".join(CRITERIA) + """.
Page numbers are the numbers in the "=== PAGE n ===" headers. Quotes must be copied word for word
from that page, 15 words or fewer. Never paraphrase inside a quote."""


def prompt(doc_title, text):
    rubric = (DATA / "rubric.md").read_text()
    return f"{rubric}\n\n{FORMAT}\n\nDOCUMENT: {doc_title}\n\n{text}"


def parse(reply):
    m = re.search(r"\{.*\}", reply, re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    data = json.loads(m.group(0))
    missing = [c for c in CRITERIA if c not in data.get("scores", {})]
    if missing:
        raise ValueError(f"missing criteria: {missing}")
    return data


def run(rater, model, doc):
    raw_path = OUT / "raw" / f"{rater}__{doc['doc_id']}.json"
    text = (SRC / "text" / f"{doc['doc_id']}.txt").read_text()
    with tempfile.TemporaryDirectory() as cwd:
        p = subprocess.run(
            ["claude", "-p", "--model", model, "--output-format", "json", "--setting-sources", "",
             "--tools", "", "--disable-slash-commands", "--strict-mcp-config",
             "--no-session-persistence", "--system-prompt", SYSTEM],
            input=prompt(doc["title"], text), capture_output=True, text=True, cwd=cwd, timeout=1800)
    if p.returncode != 0:
        return f"{rater} {doc['doc_id']}: ERROR exit {p.returncode} {p.stderr[:200]}"
    envelope = json.loads(p.stdout)
    raw_path.write_text(json.dumps({"rater": rater, "model": model, "doc_id": doc["doc_id"],
                                    "run_at": datetime.now(timezone.utc).isoformat(),
                                    "reply": envelope.get("result"), "usage": envelope.get("usage")}, indent=1))
    try:
        data = parse(envelope.get("result") or "")
    except Exception as e:
        return f"{rater} {doc['doc_id']}: PARSE ERROR {e}"
    data.update(rater=rater, model=model, doc_id=doc["doc_id"])
    (OUT / f"{rater}__{doc['doc_id']}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    return f"{rater} {doc['doc_id']}: ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    docs = [d for d in csv.DictReader(open(SRC / "sources.csv", newline="")) if d["use"] == "score"]
    todo = [(r, m, d) for r, m in RATERS.items() for d in docs if not (OUT / f"{r}__{d['doc_id']}.json").exists()]
    print(f"{len(todo)} scoring runs to do")
    if args.dry_run:
        for r, m, d in todo:
            print(" ", r, m, d["doc_id"], f"{len(prompt(d['title'], (SRC / 'text' / (d['doc_id'] + '.txt')).read_text())):,} chars")
        return
    with ThreadPoolExecutor(max_workers=4) as ex:
        for msg in ex.map(lambda a: run(*a), todo):
            print(msg, flush=True)


if __name__ == "__main__":
    main()
