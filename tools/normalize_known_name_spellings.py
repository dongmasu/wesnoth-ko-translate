#!/usr/bin/env python3
"""Fix reviewed Korean proper-name spellings before embedded-name pairing."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import GLOSSARY, WORK_KO


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)

REPLACEMENTS = {
    "Maghre": {
        "마그흐레(Maghre)": "마그레(Maghre)",
    },
    "Arvith": {
        "아르비트(Arvith)": "아르비쓰(Arvith)",
    },
    "Baran": {
        "바라네(Baran)": "바란(Baran)",
    },
    "Gerrick": {
        "게르릭(Gerrick)": "게릭(Gerrick)",
    },
    "Dacyn": {
        "다친(Dacyn)": "다신(Dacyn)",
    },
    "Mal-Ravanal": {
        "말 라바날(Mal-Ravanal)": "말-라바날(Mal-Ravanal)",
        "말 라바날": "말-라바날",
    },
}

CANONICAL = {
    "Maghre": "마그레",
    "Arvith": "아르비쓰",
    "Baran": "바란",
    "Gerrick": "게릭",
    "Dacyn": "다신",
    "Mal-Ravanal": "말-라바날",
}

OLD_BY_SOURCE = {
    "Maghre": "마그흐레",
    "Arvith": "아르비트",
    "Baran": "바라네",
    "Gerrick": "게르릭",
    "Dacyn": "다친",
    "Mal-Ravanal": "말 라바날",
}


def update_glossary(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("unexpected glossary schema")

    changed = 0
    for row in rows:
        source = row["source_term"]
        if source not in CANONICAL:
            continue
        standard = CANONICAL[source]
        updated = f"{standard}({source})"
        if row["standard_korean"] != updated:
            row["standard_korean"] = updated
            changed += 1
        forbidden = {
            item.strip()
            for item in row["forbidden_terms"].split(";")
            if item.strip()
        }
        forbidden.discard(standard)
        forbidden.add(OLD_BY_SOURCE[source])
        row["forbidden_terms"] = "; ".join(sorted(forbidden))
        row["notes"] = "고유명사 표준 음차와 긴 문장 내부 병기를 전수 대조"

    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=FIELDS,
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(output.getvalue(), encoding="utf-8")
    return changed


def update_po(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for replacements in REPLACEMENTS.values():
        for old, new in replacements.items():
            count = text.count(old)
            if count:
                text = text.replace(old, new)
                changed += count
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work", type=Path, default=WORK_KO)
    args = parser.parse_args()

    print(f"glossary: {update_glossary(args.glossary)} entries updated")
    total = 0
    for path in sorted(args.work.glob("*.po")):
        count = update_po(path)
        if count:
            print(f"{path.name}: {count} spellings normalized")
            total += count
    print(f"po total: {total} spellings normalized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
