"""Local page for rating model outputs one at a time. Saves straight into model_ratings.csv.

Usage: python3 -I rate_server.py [--csv path] [--port 8765]
Then open http://127.0.0.1:8765

Binds to 127.0.0.1 only. Model names are never loaded: the key file is not read.
"""
import argparse
import csv
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parent.parent / "data" / "model_ratings.csv"

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rate outputs</title>
<style>
:root{--bg:#fafaf8;--fg:#1c1c1a;--mute:#6b6b66;--line:#dcdcd5;--card:#fff;--accent:#2a5bd7;--ok:#1d7a46}
@media (prefers-color-scheme:dark){:root{--bg:#161615;--fg:#ececE8;--mute:#9a9a94;--line:#33332f;--card:#1f1f1d;--accent:#7aa2ff;--ok:#5ec98a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header .bar{flex:1;min-width:120px;height:6px;background:var(--line);border-radius:3px;overflow:hidden}
header .bar i{display:block;height:100%;background:var(--ok);width:0}
main{max-width:1100px;margin:0 auto;padding:16px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:800px){main{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px}
h2{margin:0 0 8px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute);font-weight:600}
pre{white-space:pre-wrap;word-wrap:break-word;margin:0;font:14px/1.55 ui-monospace,Menlo,monospace}
.full{grid-column:1/-1}
.rate{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 12px}
.rate button{flex:1;min-width:120px;padding:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:6px;cursor:pointer;font:inherit}
.rate button b{display:block;font-size:18px}.rate button small{color:var(--mute)}
.rate button.on{border-color:var(--accent);outline:2px solid var(--accent)}
textarea{width:100%;min-height:70px;border:1px solid var(--line);border-radius:6px;padding:8px;background:var(--bg);color:var(--fg);font:inherit}
nav{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
nav button,header button,header select{padding:7px 12px;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:6px;cursor:pointer;font:inherit}
.notes{border-left:3px solid var(--accent)}
#status{color:var(--mute);font-size:13px}
</style></head><body>
<header>
 <strong id="pos"></strong><span id="status"></span>
 <div class="bar"><i id="fill"></i></div>
 <label>Order <select id="order"><option value="task">By task</option><option value="blind">Shuffled</option></select></label>
 <button id="next-un">Next unrated</button>
</header>
<main>
 <div class="card"><h2>Task <span id="tid"></span></h2><div id="task"></div></div>
 <div class="card notes"><h2>Check this</h2><div id="notes"></div></div>
 <div class="card full"><h2>Prompt sent to the model</h2><pre id="input"></pre></div>
 <div class="card full"><h2>Output <span id="bid"></span></h2><pre id="resp"></pre></div>
 <div class="card full"><h2>Your rating (keys 1 to 4)</h2>
  <div class="rate" id="rate"></div>
  <textarea id="comment" placeholder="What was wrong or good? Facts you checked, edits you'd make."></textarea>
  <nav><button id="prev">&larr; Previous</button><button id="next">Next &rarr;</button></nav>
 </div>
</main>
<script>
const LABELS={1:["Unusable","wrong or harmful"],2:["Heavy edits","redo most"],3:["Light edits","fix small errors"],4:["Client-ready","read and send"]};
let rows=[],order=[],i=0;
const $=id=>document.getElementById(id);
async function load(){rows=await (await fetch('/api/rows')).json();reorder();show(firstUnrated())}
function reorder(){const keep=order[i];const m=$('order').value;
 order=rows.map((_,k)=>k);
 if(m==='task')order.sort((a,b)=>rows[a].task_id.localeCompare(rows[b].task_id)||rows[a].blind_id.localeCompare(rows[b].blind_id));
 const p=order.indexOf(keep);i=p<0?0:p}
function firstUnrated(){const p=order.findIndex(k=>!rows[k].rating);return p<0?0:p}
function show(p){i=Math.max(0,Math.min(order.length-1,p));const r=rows[order[i]];
 $('tid').textContent=r.task_id;$('task').textContent=r.task;$('notes').textContent=r.rater_notes;
 $('input').textContent=r.input;$('resp').textContent=r.response;$('bid').textContent=r.blind_id;
 $('comment').value=r.comment;
 $('rate').innerHTML='';
 for(const n of [1,2,3,4]){const b=document.createElement('button');b.innerHTML=`<b>${n}</b>${LABELS[n][0]}<br><small>${LABELS[n][1]}</small>`;
  if(String(r.rating)===String(n))b.className='on';b.onclick=()=>setRating(n);$('rate').appendChild(b)}
 const done=rows.filter(x=>x.rating).length;
 $('pos').textContent=`${i+1} / ${rows.length}`;$('status').textContent=`${done} rated`;
 $('fill').style.width=(100*done/rows.length)+'%';window.scrollTo(0,0)}
async function save(r){$('status').textContent='saving...';
 const res=await fetch('/api/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({blind_id:r.blind_id,rating:r.rating,comment:r.comment})});
 $('status').textContent=res.ok?`${rows.filter(x=>x.rating).length} rated, saved`:'SAVE FAILED'}
async function setRating(n){const r=rows[order[i]];r.rating=String(n);r.comment=$('comment').value;await save(r);show(i)}
$('comment').addEventListener('blur',async()=>{const r=rows[order[i]];if(r.comment!==$('comment').value){r.comment=$('comment').value;await save(r)}});
$('next').onclick=async()=>{await $('comment').blur();show(i+1)};$('prev').onclick=()=>show(i-1);
$('next-un').onclick=()=>show(order.findIndex((k,p)=>p>i&&!rows[k].rating)<0?firstUnrated():order.findIndex((k,p)=>p>i&&!rows[k].rating));
$('order').onchange=()=>{reorder();show(i)};
document.addEventListener('keydown',e=>{if(e.target.tagName==='TEXTAREA')return;
 if('1234'.includes(e.key))setRating(+e.key);if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1)});
load();
</script></body></html>"""


def make_handler(csv_path):
    def read():
        with open(csv_path, newline="") as f:
            return list(csv.DictReader(f)), csv.DictReader(open(csv_path, newline="")).fieldnames

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, ctype):
            data = body.encode() if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/":
                self.send(200, PAGE, "text/html; charset=utf-8")
            elif self.path == "/api/rows":
                rows, _ = read()
                self.send(200, json.dumps(rows), "application/json")
            else:
                self.send(404, "not found", "text/plain")

        def do_POST(self):
            if self.path != "/api/save":
                return self.send(404, "not found", "text/plain")
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            rating = str(body.get("rating", ""))
            if rating not in {"", "1", "2", "3", "4"}:
                return self.send(400, "bad rating", "text/plain")
            rows, fields = read()
            hit = [r for r in rows if r["blind_id"] == body.get("blind_id")]
            if not hit:
                return self.send(400, "unknown blind_id", "text/plain")
            hit[0]["rating"] = rating
            hit[0]["comment"] = str(body.get("comment", ""))
            fd, tmp = tempfile.mkstemp(dir=csv_path.parent, suffix=".tmp")
            with os.fdopen(fd, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)
            os.replace(tmp, csv_path)
            self.send(200, "ok", "text/plain")

    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    print(f"Rating {args.csv}\nOpen http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", args.port), make_handler(args.csv.resolve())).serve_forever()


if __name__ == "__main__":
    main()
