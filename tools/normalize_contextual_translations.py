#!/usr/bin/env python3
"""Normalize gettext context prefixes and register short contextual terms."""

from __future__ import annotations

import argparse
import ast
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

try:
    from tools.merge_reference_translations import replace_msgstr_fields
    from tools.project_config import GLOSSARY, PO_ROOT, WORK_KO
except ModuleNotFoundError:
    from merge_reference_translations import replace_msgstr_fields
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
FIELD_RE = re.compile(r"^(msgid|msgstr)\s+(.+)$")
SHORT_RE = re.compile(r"^[\wÀ-ÿ][\wÀ-ÿ' ^+.-]*$", re.UNICODE)
OVERRIDES = {
    "teamname^Settlers": "정착민",
    "teamname^Enemies": "적",
    "teamname^Prisoners": "포로",
}


def parse_block(block: str) -> dict[str, str]:
    values: dict[str, str] = {}
    current: str | None = None
    for line in block.splitlines():
        match = FIELD_RE.match(line)
        if match:
            current = match.group(1)
            values[current] = ast.literal_eval(match.group(2))
        elif current and line.startswith('"'):
            values[current] += ast.literal_eval(line)
        else:
            current = None
    return values


def parse_locale(paths: list[Path]) -> dict[str, Counter[str]]:
    messages: dict[str, Counter[str]] = defaultdict(Counter)
    for path in paths:
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values = parse_block(block)
            source = values.get("msgid", "")
            translation = values.get("msgstr", "")
            if source and "^" in source and translation:
                messages[source][translation] += 1
    return messages


def normalize_translation(source: str, translation: str) -> str:
    if "\n" in source or "<" in source or "%" in source or "$" in source:
        return translation
    if source in OVERRIDES:
        return OVERRIDES[source]
    # The text before ^ is a gettext context identifier, not display text.
    # Strip any accidentally translated context prefix, including female^,
    # male^, and race^. Words such as "여성" or "종족" remain when they are
    # part of the actual Korean translation rather than a context marker.
    first_caret = translation.find("^")
    if 0 <= first_caret < 80 and "\n" not in translation[:first_caret]:
        translation = translation.split("^", 1)[1]
    return translation


def update_po(path: Path) -> tuple[int, dict[str, Counter[str]]]:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    messages: dict[str, Counter[str]] = defaultdict(Counter)
    output = []
    for block in blocks:
        values = parse_block(block)
        source = values.get("msgid", "")
        translation = values.get("msgstr", "")
        if source and "^" in source and translation:
            normalized = normalize_translation(source, translation)
            messages[source][normalized] += 1
            if normalized != translation and "#~" not in block:
                updated = replace_msgstr_fields(block, {"msgstr": normalized})
                if updated != block:
                    block = updated
                    changed += 1
        output.append(block)
    path.write_text("\n\n".join(output), encoding="utf-8")
    return changed, messages


def add_short_rows(
    path: Path,
    messages: dict[str, Counter[str]],
    japanese: dict[str, Counter[str]],
    chinese: dict[str, Counter[str]],
) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        fields = tuple(reader.fieldnames or ())
    existing = {row["source_term"] for row in rows}
    added = 0
    for source, translations in sorted(messages.items()):
        korean = translations.most_common(1)[0][0]
        if source in existing:
            for row in rows:
                if row["source_term"] == source and row["category"] == "contextual":
                    row["standard_korean"] = korean
                    row["notes"] = "gettext ^ 문맥 키의 표시 문자열을 표준화"
            continue
        if len(source.split("^", 1)[1].split()) > 4:
            continue
        if "\n" in source or not SHORT_RE.fullmatch(source):
            continue
        rows.append(
            {
                "source_term": source,
                "standard_korean": korean,
                "reference_japanese": (
                    japanese.get(source, Counter()).most_common(1)[0][0]
                    if japanese.get(source)
                    else "not found"
                ),
                "reference_chinese": (
                    chinese.get(source, Counter()).most_common(1)[0][0]
                    if chinese.get(source)
                    else "not found"
                ),
                "category": "contextual",
                "forbidden_terms": "",
                "notes": "gettext ^ 문맥 키의 표시 문자열을 표준화",
            }
        )
        existing.add(source)
        added += 1
    rows.sort(key=lambda row: row["source_term"])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    return added


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-ko", type=Path, default=WORK_KO)
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--po-root", type=Path, default=PO_ROOT)
    args = parser.parse_args()

    all_messages: dict[str, Counter[str]] = defaultdict(Counter)
    changed = 0
    for path in sorted(args.work_ko.glob("*.po")):
        count, messages = update_po(path)
        changed += count
        for source, translations in messages.items():
            all_messages[source].update(translations)

    japanese = parse_locale(sorted((args.po_root / "ja").glob("*.po")))
    chinese = parse_locale(sorted((args.po_root / "zh_CN").glob("*.po")))
    added = add_short_rows(args.glossary, all_messages, japanese, chinese)
    print(f"PO entries normalized: {changed}")
    print(f"short contextual glossary rows added: {added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
