"""Extract page-numbered text from each scored policy PDF.

Usage: uv run --no-project --with pypdf --with fonttools python -I extract_text.py

Reads sources/sources.csv and sources/pdf/*.pdf. Writes, per document:
  sources/text/<doc_id>.txt          whole document, each page headed "=== PAGE n ==="
  sources/text/<doc_id>/p###.txt     one file per page
and sources/text/quality.csv (characters per page, so empty or garbled pages show up).

Page numbers are PDF page numbers (1 = first page of the file), which is what a reader
types into a PDF viewer. Text is NFKC-normalised so ligatures like "ﬁ" become "fi";
the citation checker applies the same normalisation.
"""
import csv
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
TEXT = SRC / "text"

# Per-document character fixes, checked by hand against the rendered PDF pages.
# Kenya's body font encodes the full stop so it extracts as U+FFFD ("4�1%" is "4.1%").
FIXES = {"kenya_ai_strategy_2025-2030": {"�": "."}}


def clean(s, fixes=None):
    s = unicodedata.normalize("NFKC", s or "")
    for bad, good in (fixes or {}).items():
        s = s.replace(bad, good)
    s = s.replace("­", "")              # soft hyphens
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def main():
    TEXT.mkdir(exist_ok=True)
    quality = []
    for d in csv.DictReader(open(SRC / "sources.csv", newline="")):
        if d["use"] != "score":
            continue
        reader = PdfReader(SRC / "pdf" / d["file"])
        out_dir = TEXT / d["doc_id"]
        out_dir.mkdir(exist_ok=True)
        whole = []
        for i, page in enumerate(reader.pages, 1):
            t = clean(page.extract_text(), FIXES.get(d["doc_id"]))
            (out_dir / f"p{i:03d}.txt").write_text(t + "\n")
            whole.append(f"=== PAGE {i} ===\n{t}\n")
            words = t.split()
            odd = sum(1 for w in words if not re.search(r"[A-Za-z]", w))
            quality.append({"doc_id": d["doc_id"], "page": i, "chars": len(t), "words": len(words),
                            "non_word_share": round(odd / len(words), 2) if words else ""})
        (TEXT / f"{d['doc_id']}.txt").write_text("\n".join(whole))
        print(f"{d['doc_id']}: {len(reader.pages)} pages")
    with open(TEXT / "quality.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(quality[0]))
        w.writeheader()
        w.writerows(quality)


if __name__ == "__main__":
    main()
