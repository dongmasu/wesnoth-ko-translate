#!/usr/bin/env python3
"""Normalize non-transliterated labels and campaign abbreviations."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

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

REPLACEMENTS = {
    "AToTB": "형제",
    "Base.x": "기준점 X",
    "Base.y": "기준점 Y",
    "Clan": "일족",
    "DM": "회고",
    "DW": "바다",
    "DiD": "DiD",
    "EI": "침동",
    "Garrison": "수비군",
    "HttT": "왕자",
    "LoW": "전설",
    "Northerners": "북부인",
    "NR": "부활",
    "SotA": "고대인",
    "SotBE": "검은눈",
    "THoT": "망치",
    "TRoW": "성립",
    "Treefolk": "나무 동포",
    "TSG": "남부",
    "UtBS": "태양",
    "WoF": "바람",
}

NOTES = {
    "Base.x": "편집기 좌표 레이블",
    "Base.y": "편집기 좌표 레이블",
    "Clan": "일반 명칭은 음차 병기하지 않음",
    "Garrison": "일반 명칭은 음차 병기하지 않음",
    "Northerners": "일반 명칭은 음차 병기하지 않음",
    "Treefolk": "일반 명칭은 음차 병기하지 않음",
}


def quote(value: str) -> str:
    return (
        '"'
        + value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        + '"'
    )


def parse_msgid(block: str) -> str:
    import ast

    value = ""
    active = False
    for line in block.splitlines():
        if line.startswith("msgid "):
            value = ast.literal_eval(line[6:])
            active = True
        elif active and line.startswith('"'):
            value += ast.literal_eval(line)
        else:
            active = False
    return value


def update_glossary(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("unexpected glossary schema")

    changed = 0
    for row in rows:
        source = row["source_term"]
        replacement = REPLACEMENTS.get(source)
        if replacement is None or row["standard_korean"] == replacement:
            continue
        row["standard_korean"] = replacement
        if source in NOTES:
            row["notes"] = NOTES[source]
        elif source in {
            "AToTB", "DM", "DW", "DiD", "EI", "HttT", "LoW", "NR",
            "SotA", "SotBE", "THoT", "TRoW", "TSG", "UtBS", "WoF",
        }:
            row["notes"] = "캠페인 약어는 음차 병기 대상이 아니므로 한국어 제목만 사용"
        changed += 1

    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    return changed


def update_po(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    blocks = []
    for block in text.split("\n\n"):
        source = parse_msgid(block)
        replacement = REPLACEMENTS.get(source)
        if replacement is None or re.search(r"^msgid_plural ", block, re.M):
            blocks.append(block)
            continue
        lines = block.splitlines()
        for index, line in enumerate(lines):
            if re.match(r"^msgstr(?:\[\d+\])? ", line):
                field = line.split(" ", 1)[0]
                updated = f"{field} {quote(replacement)}"
                if line != updated:
                    lines[index:] = [updated]
                    changed += 1
                break
        blocks.append("\n".join(lines))
    path.write_text("\n\n".join(blocks), encoding="utf-8")
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
            print(f"{path.name}: {count} entries updated")
            total += count
    print(f"po total: {total} entries updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
