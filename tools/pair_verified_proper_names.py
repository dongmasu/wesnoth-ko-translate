#!/usr/bin/env python3
"""Add source spelling to verified internal proper names in the glossary."""

from __future__ import annotations

import argparse
import ast
import csv
import re
from pathlib import Path


EXTERNAL_IDENTIFIERS = {"Discord", "IRC", "Reddit", "SoF", "Steam", "WC", "WoCopedia"}
PAIR_NOTE = "원본 PO의 고유명사 문맥을 확인해 한국어 음차와 원문을 병기"
FIELD_RE = re.compile(r"^(msgid|msgstr)\s+(.+)$")


def parse_block(block: str) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    comments: list[str] = []
    current: str | None = None
    for line in block.splitlines():
        if line.startswith("#."):
            comments.append(line)
        match = FIELD_RE.match(line)
        if match:
            current = match.group(1)
            values[current] = ast.literal_eval(match.group(2))
        elif current and line.startswith('"'):
            values[current] += ast.literal_eval(line)
        else:
            current = None
    return values, comments


def verified_unit_names(en_root: Path) -> set[str]:
    names: set[str] = set()
    for path in en_root.glob("*.po"):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values, comments = parse_block(block)
            source = values.get("msgid", "")
            if source and any(
                re.search(r"\[unit\].*\bid=", comment) for comment in comments
            ):
                names.add(source)
    return names


def verified_named_terms(en_root: Path) -> set[str]:
    """Return source terms explicitly declared as named PO entities."""
    names: set[str] = set()
    id_pattern = re.compile(r"\bid=([A-Za-z][A-Za-z0-9_'’.-]*)")
    for path in en_root.glob("*.po"):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values, comments = parse_block(block)
            source = values.get("msgid", "")
            if not source:
                continue
            comment_text = "\n".join(comments)
            side_comments = [
                comment
                for comment in comments
                if re.search(r"\[\s*side\s*\]", comment)
            ]
            topic_comments = [
                comment
                for comment in comments
                if re.search(r"\[\s*topic\s*\]", comment)
            ]
            ids = id_pattern.findall("\n".join(side_comments))
            geography_topic = "geography.cfg" in block
            if geography_topic:
                ids.extend(id_pattern.findall("\n".join(topic_comments)))
            if any(identifier.casefold() == source.casefold() for identifier in ids):
                names.add(source)
    return names


def update(path: Path, en_root: Path) -> tuple[int, list[str]]:
    named_terms = verified_named_terms(en_root)
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
        fields = tuple(reader.fieldnames or ())

    changed: list[str] = []
    for row in rows:
        source = row["source_term"]
        # Pair only when the English source is verified from PO entity
        # references. The glossary category is descriptive, not a pairing rule.
        verified = source in named_terms
        suffix = f" ({source})"
        if not verified and row["notes"] == PAIR_NOTE and row["standard_korean"].endswith(suffix):
            row["standard_korean"] = row["standard_korean"][: -len(suffix)].rstrip()
            row["notes"] = "PO locale 실제 표현과 고유명사 여부를 대조"
            changed.append(f"reverted:{source}")
            continue
        if source in EXTERNAL_IDENTIFIERS or "(" in row["standard_korean"]:
            continue
        if not verified:
            continue
        if not row["standard_korean"].strip() or "\n" in row["standard_korean"]:
            continue
        row["standard_korean"] = f"{row['standard_korean'].strip()} ({source})"
        row["notes"] = (
            PAIR_NOTE
        )
        changed.append(source)

    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(changed), changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=Path("work/1.18.x/glossary.tsv"))
    parser.add_argument("--en-root", type=Path, default=Path("po/1.18.x/en_GB"))
    args = parser.parse_args()
    count, changed = update(args.glossary, args.en_root)
    print(f"updated: {count}")
    print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
