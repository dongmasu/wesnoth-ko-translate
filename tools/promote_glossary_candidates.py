#!/usr/bin/env python3
"""Merge all reviewed candidate rows into the curated glossary."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work" / "1.18.x"
GLOSSARY = WORK / "glossary.tsv"
CANDIDATES = WORK / "glossary-candidates.tsv"

FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_rows(rows: list[dict[str, str]]) -> None:
    with GLOSSARY.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    curated = read_rows(GLOSSARY)
    candidates = read_rows(CANDIDATES)
    sources = {row["source_term"] for row in curated}
    promoted = 0

    for row in candidates:
        source = row["source_term"]
        if source in sources or not row["standard_korean"]:
            continue
        row["category"] = "term"
        row["notes"] = (
            "PO 전체 대조 후 표준 번역으로 채택; "
            "문맥별 예외가 발견되면 별도 source_term으로 분리"
        )
        curated.append(row)
        sources.add(source)
        promoted += 1

    curated.sort(key=lambda row: row["source_term"].casefold())
    write_rows(curated)
    print(f"promoted {promoted} candidates into {GLOSSARY}")
    print(f"total glossary entries: {len(curated)}")


if __name__ == "__main__":
    main()
