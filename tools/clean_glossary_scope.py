#!/usr/bin/env python3
"""Remove sentence-like rows from the curated glossary."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "work" / "1.18.x" / "glossary.tsv"
FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)
WORD_RE = re.compile(r"\b[\w'-]+\b")


def is_sentence_like(row: dict[str, str]) -> bool:
    """Keep terms and short fixed UI phrases; remove prose from term rows."""
    if row["category"] != "term":
        return False
    source = row["source_term"]
    return (
        len(WORD_RE.findall(source)) > 6
        or bool(re.search(r"[.!?]\s*$", source))
        or "\n" in source
        or any(marker in source for marker in ("<", "%", "$"))
    )


def main() -> int:
    with GLOSSARY.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    kept = [row for row in rows if not is_sentence_like(row)]
    removed = len(rows) - len(kept)
    with GLOSSARY.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(kept)
    print(f"removed {removed} sentence-like glossary rows")
    print(f"remaining glossary rows: {len(kept)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
