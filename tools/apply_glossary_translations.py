#!/usr/bin/env python3
"""Apply exact glossary entries to Korean PO messages."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from merge_reference_translations import (
    is_fuzzy,
    normalize_translation_boundaries,
    parse_field_values,
    replace_msgstr_fields,
)


def load_glossary(path: Path) -> dict[str, str]:
    with path.open(encoding="utf-8", newline="") as stream:
        return {
            row["source_term"]: row["standard_korean"]
            for row in csv.DictReader(stream, delimiter="\t")
            if row["source_term"] and row["standard_korean"]
        }


def apply_file(path: Path, glossary: dict[str, str]) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        if source in glossary and not is_fuzzy(block) and "msgid_plural" not in values:
            translations = normalize_translation_boundaries(
                source,
                {"msgstr": glossary[source]},
            )
            updated = replace_msgstr_fields(block, translations)
            if updated != block:
                changed += 1
                block = updated
        output.append(block)
    path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=Path("work/1.18.x/glossary.tsv"))
    parser.add_argument("--work", type=Path, default=Path("work/1.18.x/ko"))
    args = parser.parse_args()

    glossary = load_glossary(args.glossary)
    total = 0
    for path in sorted(args.work.glob("*.po")):
        count = apply_file(path, glossary)
        if count:
            print(f"{path.name}: {count} entries applied")
            total += count
    print(f"total: {total} entries applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
