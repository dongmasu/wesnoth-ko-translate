#!/usr/bin/env python3
"""Synchronize gettext-context glossary rows with the locale PO files."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from merge_reference_translations import (
    parse_field_values,
    replace_msgstr_fields,
)
from project_config import GLOSSARY, PO_ROOT, WORK_KO


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)


def load_messages(paths: list[Path]) -> dict[str, Counter[str]]:
    messages: dict[str, Counter[str]] = defaultdict(Counter)
    for path in paths:
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values = parse_field_values(block)
            source = values.get("msgid", "")
            translation = values.get("msgstr", "")
            if source:
                messages[source][translation] += 1
    return messages


def one_translation(messages: dict[str, Counter[str]], source: str) -> str | None:
    choices = messages.get(source, Counter())
    if not choices:
        return None
    return choices.most_common(1)[0][0]


def display_translation(source: str, translation: str) -> str:
    """Drop an accidentally stored gettext context prefix from Korean."""
    if "^" in source and "^" in translation:
        return translation.split("^", 1)[1]
    return translation


def contextual_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return [
            row
            for row in csv.DictReader(stream, delimiter="\t")
            if "^" in row["source_term"]
        ]


def update_glossary(
    path: Path,
    korean: dict[str, Counter[str]],
    japanese: dict[str, Counter[str]],
    chinese: dict[str, Counter[str]],
) -> tuple[int, int]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)

    changed = 0
    reference_changed = 0
    for row in rows:
        source = row["source_term"]
        if "^" not in source:
            continue

        korean_value = one_translation(korean, source)
        if korean_value is not None:
            korean_value = display_translation(source, korean_value)
            if row["standard_korean"] != korean_value:
                row["standard_korean"] = korean_value
                changed += 1

        for field, messages in (
            ("reference_japanese", japanese),
            ("reference_chinese", chinese),
        ):
            value = one_translation(messages, source)
            if value is not None and row[field] != value:
                row[field] = value
                reference_changed += 1

        row["notes"] = (
            "gettext 문맥 키(source_term의 ^ 앞부분)는 번역하지 않고, "
            "^ 뒤의 표시 문자열만 표준 번역으로 사용"
        )

    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    return changed, reference_changed


def update_work_po(path: Path, glossary: dict[str, str]) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = glossary.get(source)
        if translation is None:
            output.append(block)
            continue
        updated = replace_msgstr_fields(block, {"msgstr": translation})
        if updated != block:
            changed += 1
        output.append(updated)
    path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--glossary",
        type=Path,
        default=GLOSSARY,
    )
    parser.add_argument(
        "--work-ko",
        type=Path,
        default=WORK_KO,
    )
    parser.add_argument(
        "--po-root",
        type=Path,
        default=PO_ROOT,
    )
    args = parser.parse_args()

    work_ko = load_messages(sorted(args.work_ko.glob("*.po")))
    japanese = load_messages(sorted((args.po_root / "ja").glob("*.po")))
    chinese = load_messages(sorted((args.po_root / "zh_CN").glob("*.po")))

    changed, reference_changed = update_glossary(
        args.glossary,
        work_ko,
        japanese,
        chinese,
    )

    with args.glossary.open(encoding="utf-8", newline="") as stream:
        glossary = {
            row["source_term"]: row["standard_korean"]
            for row in csv.DictReader(stream, delimiter="\t")
            if "^" in row["source_term"]
        }

    po_changed = sum(
        update_work_po(path, glossary)
        for path in sorted(args.work_ko.glob("*.po"))
    )
    print(f"glossary Korean values updated: {changed}")
    print(f"glossary reference values updated: {reference_changed}")
    print(f"work PO entries updated: {po_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
