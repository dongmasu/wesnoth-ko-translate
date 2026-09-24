#!/usr/bin/env python3
"""Merge trusted Korean translations into the current work PO files.

Only exact gettext message keys are merged. The current GitHub PO files remain
the structural source of truth; the archived Korean translations provide the
preferred wording where their message key still exists.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


FIELD_RE = re.compile(
    r"^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.+)$"
)
MSGSTR_RE = re.compile(r"^msgstr(?:\[\d+\])?")


def parse_field_values(block: str) -> dict[str, str]:
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


def key_for(values: dict[str, str]) -> tuple[str, str, str]:
    return (
        values.get("msgctxt", ""),
        values.get("msgid", ""),
        values.get("msgid_plural", ""),
    )


def is_fuzzy(block: str) -> bool:
    return any(line.startswith("#,") and "fuzzy" in line for line in block.splitlines())


def po_quote(value: str) -> str:
    return (
        '"'
        + value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\t", "\\t")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        + '"'
    )


def replacement_lines(field: str, value: str) -> list[str]:
    if "\n" not in value:
        return [f"{field} {po_quote(value)}"]
    pieces = value.splitlines(keepends=True)
    lines = [f'{field} ""']
    lines.extend(po_quote(piece) for piece in pieces)
    if pieces and not pieces[-1].endswith("\n"):
        lines[-1] = po_quote(pieces[-1])
    return lines


def replace_msgstr_fields(block: str, translations: dict[str, str]) -> str:
    lines = block.splitlines()
    output: list[str] = []
    index = 0
    changed = False
    while index < len(lines):
        line = lines[index]
        match = FIELD_RE.match(line)
        if not match or not MSGSTR_RE.match(match.group(1)):
            output.append(line)
            index += 1
            continue

        field = match.group(1)
        value = translations.get(field)
        if value is None:
            output.append(line)
            index += 1
            while index < len(lines) and lines[index].startswith('"'):
                output.append(lines[index])
                index += 1
            continue

        output.extend(replacement_lines(field, value))
        changed = True
        index += 1
        while index < len(lines) and lines[index].startswith('"'):
            index += 1

    result = "\n".join(output)
    if changed:
        result = re.sub(r"^#, fuzzy\s*\n", "", result, flags=re.MULTILINE)
    return result


def normalize_translation_boundaries(msgid: str, translations: dict[str, str]) -> dict[str, str]:
    """Keep gettext's required leading/trailing newline boundaries."""
    normalized = {}
    for field, value in translations.items():
        if msgid.startswith("\n") and not value.startswith("\n"):
            value = "\n" + value
        if msgid.endswith("\n") and not value.endswith("\n"):
            value += "\n"
        normalized[field] = value
    return normalized


def reference_translations(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        values = parse_field_values(block)
        if not values or not values.get("msgid") or is_fuzzy(block):
            continue
        translations = {
            field: value
            for field, value in values.items()
            if MSGSTR_RE.match(field) and value
        }
        if translations:
            result[key_for(values)] = translations
    return result


def merge_file(work_path: Path, reference_path: Path) -> int:
    references = reference_translations(reference_path)
    blocks = work_path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    merged: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        translations = references.get(key_for(values)) if values else None
        if translations:
            translations = normalize_translation_boundaries(
                values.get("msgid", ""),
                translations,
            )
            updated = replace_msgstr_fields(block, translations)
            if updated != block:
                changed += 1
            block = updated
        merged.append(block)
    work_path.write_text("\n\n".join(merged), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--work",
        type=Path,
        default=Path("work/1.18.x/ko"),
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=Path("References/20250322_wesnoth_한국어번역"),
    )
    args = parser.parse_args()

    total = 0
    for work_path in sorted(args.work.glob("*.po")):
        reference_path = args.reference / work_path.name
        if reference_path.exists():
            count = merge_file(work_path, reference_path)
            total += count
            print(f"{work_path.name}: {count} entries merged")
    print(f"total: {total} entries merged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
