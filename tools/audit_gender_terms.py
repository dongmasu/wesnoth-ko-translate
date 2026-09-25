#!/usr/bin/env python3
"""Audit lexical gender pairs separately from gettext gender contexts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import GLOSSARY


LEXICAL_PAIRS = (
    ("sorceress", "sorcerer"),
    ("princess", "prince"),
    ("queen", "king"),
    ("baroness", "baron"),
    ("duchess", "duke"),
    ("empress", "emperor"),
    ("priestess", "priest"),
    ("heroine", "hero"),
    ("watchwoman", "watchman"),
    ("woman", "man"),
    ("girl", "boy"),
    ("daughter", "son"),
    ("mother", "father"),
    ("sister", "brother"),
    ("wife", "husband"),
    ("widow", "widower"),
)
CONTEXT_PREFIXES = ("female^", "male^", "race+female^", "race+male^")
CONTEXT_DISPLAY_EXCEPTIONS = {"female^Inky"}
FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def lexical_pairs(rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    by_source = {row["source_term"]: row for row in rows}
    source_by_lower = {source.lower(): source for source in by_source}
    found: set[tuple[str, str]] = set()
    for source in by_source:
        lower = source.lower()
        for feminine, masculine in LEXICAL_PAIRS:
            if not lower.endswith(feminine) or lower == feminine:
                continue
            masculine_candidate = lower[: -len(feminine)] + masculine
            masculine_source = source_by_lower.get(masculine_candidate)
            if masculine_source:
                found.add((masculine_source, source))
    return sorted(found)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    args = parser.parse_args()

    rows = load_rows(args.glossary)
    if rows and tuple(rows[0]) != FIELDS:
        raise SystemExit("ERROR: glossary header does not match the required schema")

    by_source = {row["source_term"]: row for row in rows}
    errors: list[str] = []
    warnings: list[str] = []

    for masculine, feminine in lexical_pairs(rows):
        masculine_ko = by_source[masculine]["standard_korean"]
        feminine_ko = by_source[feminine]["standard_korean"]
        print(
            f"LEXICAL_PAIR\t{masculine}\t{masculine_ko}\t"
            f"{feminine}\t{feminine_ko}"
        )
        if masculine_ko == feminine_ko:
            warnings.append(
                f"lexical gender pair shares Korean translation: "
                f"{masculine} / {feminine} -> {masculine_ko}"
            )

    for row in rows:
        source = row["source_term"]
        if not source.startswith(CONTEXT_PREFIXES):
            continue
        if source in CONTEXT_DISPLAY_EXCEPTIONS:
            continue
        base = source.split("^", 1)[1]
        if base not in by_source:
            continue
        if row["standard_korean"] != by_source[base]["standard_korean"]:
            errors.append(f"context/base mismatch: {source} != {base}")

    for left, right in (
        ("Mage", "Sorcerer"),
        ("Mage", "Wizard"),
        ("Sorcerer", "Wizard"),
    ):
        if left in by_source and right in by_source:
            left_ko = by_source[left]["standard_korean"]
            right_ko = by_source[right]["standard_korean"]
            print(f"MAGIC_TERM\t{left}\t{left_ko}\t{right}\t{right_ko}")
            if left_ko == right_ko:
                warnings.append(
                    f"magic term collision: {left} / {right} -> {left_ko}"
                )

    print(f"rows={len(rows)}")
    print(f"errors={len(errors)}")
    print(f"warnings={len(warnings)}")
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
