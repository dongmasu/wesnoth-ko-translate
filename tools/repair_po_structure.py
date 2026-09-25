#!/usr/bin/env python3
"""Repair mechanically recoverable PO markup mismatches.

This tool only changes markup tokens. It removes tags added where the source
has none, and restores source tag names when source and translation have the
same number of tags. Messages with different tag counts are reported for
manual review instead of being guessed.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.audit_po_structure import TAG_RE


FIELD_RE = re.compile(r"^(msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.+)$")
TAG_TOKEN_RE = re.compile(TAG_RE.pattern)


def parse_values(block: str) -> dict[str, str]:
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


def field_lines(field: str, value: str) -> list[str]:
    if "\n" not in value:
        return [f"{field} {quote(value)}"]
    pieces = value.splitlines(keepends=True)
    lines = [f'{field} ""']
    lines.extend(quote(piece) for piece in pieces)
    if pieces and not pieces[-1].endswith("\n"):
        lines[-1] = quote(pieces[-1])
    return lines


def repair_tags(source: str, translation: str) -> tuple[str, bool]:
    source_tags = TAG_TOKEN_RE.findall(source)
    translation_tags = TAG_TOKEN_RE.findall(translation)
    if not translation_tags:
        return translation, False
    if not source_tags:
        return TAG_TOKEN_RE.sub("", translation), True
    if len(source_tags) != len(translation_tags):
        return translation, False
    iterator = iter(source_tags)
    repaired = TAG_TOKEN_RE.sub(lambda _: next(iterator), translation)
    return repaired, repaired != translation


def repair_file(path: Path, apply: bool) -> tuple[int, int]:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    manual = 0
    output: list[str] = []
    for block in blocks:
        values = parse_values(block)
        source = values.get("msgid", "")
        if not source or "msgstr" not in values:
            output.append(block)
            continue
        translations = [
            field for field in values
            if field == "msgstr" or field.startswith("msgstr[")
        ]
        replacements: dict[str, str] = {}
        source_forms = [source]
        if values.get("msgid_plural"):
            source_forms.append(values["msgid_plural"])
        for index, field in enumerate(translations):
            translation = values[field]
            source_form = source_forms[min(index, len(source_forms) - 1)]
            repaired, did_change = repair_tags(source_form, translation)
            if TAG_TOKEN_RE.findall(source_form) and len(TAG_TOKEN_RE.findall(source_form)) != len(TAG_TOKEN_RE.findall(translation)):
                manual += 1
            if did_change:
                replacements[field] = repaired
        if not replacements:
            output.append(block)
            continue
        changed += 1
        if not apply:
            output.append(block)
            continue
        lines = block.splitlines()
        rebuilt: list[str] = []
        index = 0
        while index < len(lines):
            line = lines[index]
            match = FIELD_RE.match(line)
            if not match or match.group(1) not in replacements:
                rebuilt.append(line)
                index += 1
                continue
            field = match.group(1)
            rebuilt.extend(field_lines(field, replacements[field]))
            index += 1
            while index < len(lines) and lines[index].startswith('"'):
                index += 1
        output.append("\n".join(rebuilt))
    if apply:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed, manual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    total = 0
    manual = 0
    for path in sorted(args.directory.glob("*.po")):
        changed, pending = repair_file(path, args.apply)
        if changed or pending:
            print(f"{path.name}\tchanged={changed}\tmanual={pending}")
        total += changed
        manual += pending
    print(f"changed={total}\tmanual={manual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
