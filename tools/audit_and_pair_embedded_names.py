#!/usr/bin/env python3
"""Audit and pair glossary proper names embedded in longer PO messages."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

try:
    from tools.merge_reference_translations import (
        is_fuzzy,
        parse_field_values,
        replacement_lines,
        replace_msgstr_fields,
    )
    from tools.project_config import GLOSSARY, WORK_KO
except ModuleNotFoundError:
    # Keep direct execution from the repository root working as documented.
    from merge_reference_translations import (
        is_fuzzy,
        parse_field_values,
        replacement_lines,
        replace_msgstr_fields,
    )
    from project_config import GLOSSARY, WORK_KO


NAME_CATEGORIES = {
    "person_name",
    "place_name",
    "race_name",
    "proper_noun",
    "unit_name",
    "faction",
    "campaign_name",
    "ability",
}
NON_NAME_COMPONENTS = {
    "a",
    "and",
    "chief",
    "clan",
    "contender",
    "duke",
    "elder",
    "general",
    "king",
    "lady",
    "lord",
    "minister",
    "mother",
    "mr",
    "mrs",
    "queen",
    "sir",
    "the",
}
PARENTHESIZED = re.compile(r"\(([^()]+)\)")
ENGLISH_COMPONENT = re.compile(r"[A-Za-z][A-Za-z0-9 .\-’']*")
PARTICLE = r"(?:은|는|이|가|을|를|의|에|로|와|과|도|만|에서|에게|으로)?"


@dataclass(frozen=True)
class NamePair:
    source: str
    korean: str
    category: str
    glossary_source: str


def load_pairs(path: Path) -> tuple[list[NamePair], list[str]]:
    by_source: dict[str, list[NamePair]] = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            if row["category"] not in NAME_CATEGORIES:
                continue
            standard = row["standard_korean"]
            for match in PARENTHESIZED.finditer(standard):
                source = match.group(1)
                if not ENGLISH_COMPONENT.fullmatch(source):
                    continue
                korean_prefix = standard[: match.start()].strip()
                korean_tokens = re.findall(r"[가-힣]+", korean_prefix)
                source_tokens = re.findall(r"[A-Za-z]+", source)
                source_token_count = len(source_tokens)
                korean = " ".join(korean_tokens[-source_token_count:])
                if korean:
                    pair = NamePair(source, korean, row["category"], row["source_term"])
                    by_source.setdefault(source, []).append(pair)

                # A compound name may occur later as individual components in
                # prose. Reuse the established transliteration for those
                # components, but never turn titles into names.
                if (
                    source == row["source_term"]
                    and
                    len(source.split()) > 1
                    and source_token_count > 1
                    and len(korean_tokens) >= source_token_count
                ):
                    for source_token, korean_token in zip(
                        source_tokens, korean_tokens[-source_token_count:]
                    ):
                        if source_token.lower() in NON_NAME_COMPONENTS:
                            continue
                        component = NamePair(
                            source_token,
                            korean_token,
                            row["category"],
                            row["source_term"],
                        )
                        by_source.setdefault(source_token, []).append(component)

    pairs: list[NamePair] = []
    conflicts: list[str] = []
    for source, candidates in by_source.items():
        exact = [pair for pair in candidates if pair.glossary_source == source]
        choices = exact or candidates
        unique = {pair.korean for pair in choices}
        if len(unique) > 1:
            conflicts.append(
                f"{source}: "
                + ", ".join(sorted(unique))
            )
            continue
        pairs.append(choices[0])
    return pairs, conflicts


def source_occurs(source: str, text: str) -> bool:
    if source not in text:
        return False
    return bool(SOURCE_PATTERNS[source].search(text))


def pair_translation(translation: str, pair: NamePair) -> tuple[str, int]:
    marker = f"({pair.source})"
    pattern = TRANSLATION_PATTERNS[(pair.korean, pair.source)]
    changed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        changed += 1
        return f"{pair.korean}{marker}{match.group('particle')}"

    updated = pattern.sub(replace, translation)
    source_pattern = SOURCE_TRANSLATION_PATTERNS[pair.source]

    def replace_source(match: re.Match[str]) -> str:
        nonlocal changed
        changed += 1
        return f"{pair.korean}{marker}{match.group('particle')}"

    return source_pattern.sub(replace_source, updated), changed


def obsolete_to_parseable(block: str) -> str:
    """Remove obsolete prefixes while ignoring gettext's previous-msgid lines."""
    lines = []
    for line in block.splitlines():
        if line.startswith("#~|"):
            continue
        if line.startswith("#~ "):
            lines.append(line[3:])
    return "\n".join(lines)


def obsolete_previous_msgid(block: str) -> str:
    """Read gettext's previous msgid kept in ``#~|`` comments."""
    lines = [
        line[4:]
        for line in block.splitlines()
        if line.startswith("#~| ")
    ]
    return parse_field_values("\n".join(lines)).get("msgid", "")


def replace_obsolete_msgstr_fields(
    block: str,
    translations: dict[str, str],
) -> str:
    """Replace obsolete msgstr fields without discarding obsolete metadata."""
    lines = block.splitlines()
    output: list[str] = []
    index = 0
    field_re = re.compile(r"^#~ (msgstr(?:\[\d+\])?)\s+(.+)$")
    while index < len(lines):
        line = lines[index]
        match = field_re.match(line)
        if not match:
            output.append(line)
            index += 1
            continue

        field = match.group(1)
        value = translations.get(field)
        if value is None:
            output.append(line)
            index += 1
            while index < len(lines) and lines[index].startswith("#~ "):
                continuation = lines[index][3:]
                if continuation.startswith('"'):
                    output.append(lines[index])
                    index += 1
                else:
                    break
            continue

        replacement = replacement_lines(field, value)
        output.extend(f"#~ {replacement_line}" for replacement_line in replacement)
        index += 1
        while index < len(lines):
            continuation = lines[index]
            if not continuation.startswith("#~ "):
                break
            if continuation[3:].startswith('"'):
                index += 1
                continue
            break

    return "\n".join(output)


SOURCE_PATTERNS: dict[str, re.Pattern[str]] = {}
TRANSLATION_PATTERNS: dict[tuple[str, str], re.Pattern[str]] = {}
SOURCE_TRANSLATION_PATTERNS: dict[str, re.Pattern[str]] = {}
NESTED_COMPONENT_PAIR = re.compile(
    r"(?P<left>[가-힣]+)\((?P<left_source>[A-Za-z]+)\)\s+"
    r"(?P<right>[가-힣]+)\((?P=left_source)\s+"
    r"(?P=right)\((?P<right_source>[A-Za-z]+)\)\)"
)


def process_file(path: Path, pairs: list[NamePair], apply: bool) -> tuple[int, int]:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    output: list[str] = []
    changed_messages = 0
    unresolved = 0
    for block in blocks:
        obsolete = any(line.startswith("#~") for line in block.splitlines())
        parseable_block = obsolete_to_parseable(block) if obsolete else block
        values = parse_field_values(parseable_block)
        source = values.get("msgid", "")
        pairing_source = source
        if obsolete:
            pairing_source += "\n" + obsolete_previous_msgid(block)
        translation = values.get("msgstr")
        if (
            not source
            or not translation
            or source.count(",") >= 20
            or "=" in source
            or "{" in source
            or (is_fuzzy(block) and not obsolete)
            or "msgid_plural" in values
        ):
            output.append(block)
            continue

        updated = NESTED_COMPONENT_PAIR.sub(
            r"\g<left>(\g<left_source>) \g<right>(\g<right_source>)",
            translation,
        )
        message_changes = 0
        whole_sources = {
            pair.source
            for pair in pairs
            if pair.glossary_source == pair.source
            and source_occurs(pair.source, pairing_source)
        }
        whole_components = {
            component
            for whole in whole_sources
            for component in re.findall(r"[A-Za-z]+", whole)
        }
        for pair in sorted(pairs, key=lambda item: len(item.source)):
            if (
                pair.glossary_source != pair.source
                and (
                    pair.glossary_source in whole_sources
                    or pair.source in whole_components
                )
            ):
                continue
            if not source_occurs(pair.source, pairing_source):
                continue
            updated, count = pair_translation(updated, pair)
            message_changes += count
            if pair.korean in updated and f"({pair.source})" not in updated:
                unresolved += 1

        if message_changes and apply:
            translations = {"msgstr": updated}
            if obsolete:
                block = replace_obsolete_msgstr_fields(block, translations)
            else:
                block = replace_msgstr_fields(block, translations)
        if message_changes:
            changed_messages += 1
        output.append(block)

    if apply:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed_messages, unresolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work", type=Path, default=WORK_KO)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    pairs, conflicts = load_pairs(args.glossary)
    SOURCE_PATTERNS.update(
        {
            pair.source: re.compile(
                r"(?<![A-Za-z0-9-])"
                + re.escape(pair.source)
                + r"(?![A-Za-z0-9-])"
            )
            for pair in pairs
        }
    )
    TRANSLATION_PATTERNS.update(
        {
            (pair.korean, pair.source): re.compile(
                re.escape(pair.korean)
                + f"(?P<particle>{PARTICLE})(?!{re.escape(f'({pair.source})')})"
                + r"(?!\()"
            )
            for pair in pairs
        }
    )
    SOURCE_TRANSLATION_PATTERNS.update(
        {
            pair.source: re.compile(
                r"(?<![A-Za-z0-9-(])"
                + re.escape(pair.source)
                + f"(?P<particle>{PARTICLE})"
                + r"(?![A-Za-z0-9-])"
            )
            for pair in pairs
        }
    )
    for conflict in conflicts:
        print(f"conflict: {conflict}")
    total_messages = 0
    total_unresolved = 0
    for path in sorted(args.work.glob("*.po")):
        messages, unresolved = process_file(path, pairs, apply=not args.check)
        if messages or unresolved:
            print(f"{path.name}: messages={messages} unresolved={unresolved}")
        total_messages += messages
        total_unresolved += unresolved
    print(f"pairs={len(pairs)} conflicts={len(conflicts)}")
    print(f"messages={total_messages} unresolved={total_unresolved}")
    return 1 if conflicts or total_unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
