"""Send each test prompt to each model and save raw outputs.

Usage:
    python3 -I run_models.py --dry-run          # show what would run
    python3 -I run_models.py                    # Claude CLI backend (default); safe to re-run
    OPENROUTER_API_KEY=... python3 -I run_models.py --backend openrouter

The claude-cli backend runs each prompt in a fresh, empty session: temp working directory, no
settings, no tools, no skills, no MCP servers, no saved session. Only the system prompt and the
task input are seen by the model. It cannot set temperature.

Outputs are appended to data/model_runs/runs.jsonl, one line per task and model.
Only the system prompt and task input are sent. rater_notes never leave this machine.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "data" / "model_runs"
URL = "https://openrouter.ai/api/v1/chat/completions"


def call(key, model, system, user, temperature, max_tokens):
    body = json.dumps({
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 ** (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}")
    raise RuntimeError("unreachable")


def call_cli(model, system, user):
    with tempfile.TemporaryDirectory() as cwd:
        p = subprocess.run(
            ["claude", "-p", "--model", model, "--output-format", "json", "--setting-sources", "",
             "--tools", "", "--disable-slash-commands", "--strict-mcp-config",
             "--no-session-persistence", "--system-prompt", system],
            input=user, capture_output=True, text=True, cwd=cwd, timeout=600)
    if p.returncode != 0:
        raise RuntimeError(f"claude exited {p.returncode}: {p.stderr[:300]}")
    data = json.loads(p.stdout)
    if data.get("is_error"):
        raise RuntimeError(f"claude error: {str(data.get('result'))[:300]}")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--backend", choices=["claude-cli", "openrouter"], default="claude-cli")
    args = ap.parse_args()

    cfg = json.load(open(RUNS / "models.json"))
    prompts = json.load(open(RUNS / "test_prompts.json"))
    out_path = RUNS / "runs.jsonl"
    done = set()
    if out_path.exists():
        for line in open(out_path):
            r = json.loads(line)
            if not r.get("error"):
                done.add((r["task_id"], r["model"]))

    models = cfg["models_" + args.backend.replace("-", "_")]
    todo = [(t, m) for t in prompts["tasks"] for m in models if (t["task_id"], m) not in done]
    print(f"{len(todo)} runs to do ({len(done)} already done)")
    if args.dry_run or not todo:
        return

    key = os.environ.get("OPENROUTER_API_KEY")
    if args.backend == "openrouter" and not key:
        sys.exit("Set OPENROUTER_API_KEY first")

    with open(out_path, "a") as f:
        for i, (t, model) in enumerate(todo, 1):
            rec = {"task_id": t["task_id"], "model": model, "system_prompt": prompts["system_prompt"],
                   "input": t["input"], "backend": args.backend,
                   "temperature": cfg["temperature"] if args.backend == "openrouter" else None,
                   "run_at": datetime.now(timezone.utc).isoformat()}
            try:
                if args.backend == "claude-cli":
                    data = call_cli(model, prompts["system_prompt"], t["input"])
                    rec.update(response=data.get("result") or "", finish_reason=data.get("subtype"),
                               served_model=list((data.get("modelUsage") or {}).keys()),
                               usage=data.get("usage"))
                else:
                    data = call(key, model, prompts["system_prompt"], t["input"], cfg["temperature"], cfg["max_tokens"])
                    choice = data["choices"][0]
                    rec.update(response=choice["message"].get("content") or "",
                               finish_reason=choice.get("finish_reason"),
                               served_model=data.get("model"), usage=data.get("usage"))
            except Exception as e:
                rec["error"] = str(e)
            f.write(json.dumps(rec) + "\n")
            f.flush()
            print(f"[{i}/{len(todo)}] {t['task_id']} {model} {'ERROR ' + rec['error'] if 'error' in rec else 'ok'}")


if __name__ == "__main__":
    main()
