#!/usr/bin/env python3
"""Audit glossary structure and synchronization without changing files."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

# Allow direct execution from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values
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
WORD_RE = re.compile(r"\b[\w’'-]+\b")
PAREN_RE = re.compile(r"\(([A-Za-z][^()]*)\)")
NOTE_MARKER_RE = re.compile(r"(?:번역|검토|확인|TODO|FIXME)")
TECHNICAL_PARENTS = {"ZOC"}
GENDER_CONTEXT_RE = re.compile(r"^(?:(?:race\+)?(?:female|male)\^)(.+)$")
# These variants use the context key to distinguish a specifically female
# entity. Korean normally has no equivalent grammatical form, except where
# the sex itself is part of the displayed identity.
GENDER_CONTEXT_DISPLAY_EXCEPTIONS = {"female^Inky"}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        for field in FIELDS:
            row[field] = row.get(field) or ""
    return rows


def po_translations(directory: Path) -> dict[str, set[str]]:
    """Collect all translations for a msgid across contextual PO entries."""
    translations: dict[str, set[str]] = {}
    for path in directory.glob("*.po"):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values = parse_field_values(block)
            if values.get("msgid") and "msgstr" in values:
                translations.setdefault(values["msgid"], set()).add(values["msgstr"])
    return translations


def source_tokens(source: str) -> set[str]:
    """Return source tokens, excluding possessive suffixes."""
    tokens = set(WORD_RE.findall(source.split("^", 1)[-1]))
    return {
        token[:-1] if token.endswith(("’", "'")) else token
        for token in tokens
    }


def parenthetical_is_source_component(parenthetical: str, source: str) -> bool:
    """Accept names that are source tokens or components of compound tokens."""
    parenthetical_tokens = WORD_RE.findall(parenthetical)
    if not parenthetical_tokens:
        return False
    source_words = source_tokens(source)
    for candidate in parenthetical_tokens:
        if candidate in source_words:
            continue
        if any(word.startswith(candidate) for word in source_words):
            continue
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work-ko", type=Path, default=WORK_KO)
    args = parser.parse_args()

    rows = load_rows(args.glossary)
    errors: list[str] = []
    warnings: list[str] = []

    if rows and tuple(rows[0]) != FIELDS:
        errors.append("glossary header does not match the required schema")

    sources = [row["source_term"] for row in rows]
    for source, count in Counter(sources).items():
        if count > 1:
            errors.append(f"duplicate source_term: {source}")

    translations = po_translations(args.work_ko)
    for row in rows:
        source = row["source_term"]
        standard = row["standard_korean"]
        stripped_standard = standard.strip()
        forbidden = {
            item.strip()
            for item in row["forbidden_terms"].split(";")
            if item.strip()
        }
        if not source or not stripped_standard:
            errors.append(f"empty required value: {source!r}")
        if stripped_standard in forbidden:
            errors.append(f"standard translation is forbidden: {source}")
        if any(NOTE_MARKER_RE.search(item) for item in forbidden):
            errors.append(f"review note leaked into forbidden_terms: {source}")
        if source in translations and standard not in translations[source]:
            errors.append(f"glossary/PO mismatch: {source}")

        for parenthetical in PAREN_RE.findall(standard):
            if parenthetical in TECHNICAL_PARENTS:
                continue
            if not parenthetical_is_source_component(parenthetical, source):
                warnings.append(
                    f"parenthetical text is not a source token: "
                    f"{source} -> ({parenthetical})"
                )

        if (
            row["category"] == "term"
            and len(WORD_RE.findall(source)) > 6
        ):
            warnings.append(f"long term candidate: {source}")

        gender_match = GENDER_CONTEXT_RE.fullmatch(source)
        if (
            gender_match
            and source not in GENDER_CONTEXT_DISPLAY_EXCEPTIONS
            and gender_match.group(1) in {item["source_term"] for item in rows}
        ):
            base = next(
                item
                for item in rows
                if item["source_term"] == gender_match.group(1)
            )
            if standard != base["standard_korean"]:
                errors.append(
                    "gender-context/base mismatch: "
                    f"{source} != {base['source_term']}"
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
