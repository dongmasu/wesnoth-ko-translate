#!/usr/bin/env python3
"""Synchronize exact glossary Korean values with the generated work PO files."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from merge_reference_translations import parse_field_values
from project_config import GLOSSARY, WORK_KO


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)


def load_translations(work: Path) -> dict[str, str]:
    values: dict[str, Counter[str]] = {}
    for path in sorted(work.glob("*.po")):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            parsed = parse_field_values(block)
            source = parsed.get("msgid", "")
            translation = parsed.get("msgstr")
            if source and translation is not None:
                values.setdefault(source, Counter())[translation] += 1
    return {source: counts.most_common(1)[0][0] for source, counts in values.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work-ko", type=Path, default=WORK_KO)
    args = parser.parse_args()

    translations = load_translations(args.work_ko)
    with args.glossary.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))

    changed = 0
    for row in rows:
        value = translations.get(row["source_term"])
        if value is not None and value != row["standard_korean"]:
            row["standard_korean"] = value
            changed += 1

    with args.glossary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"glossary Korean values updated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
