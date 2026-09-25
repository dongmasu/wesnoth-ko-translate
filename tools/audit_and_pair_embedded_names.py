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


@dataclass(frozen=True)
class NameCandidate:
    source: str
    path: Path
    context: str
    obsolete: bool = False


COMMON_SOURCE_WORDS = {
    "A",
    "An",
    "And",
    "As",
    "At",
    "But",
    "Can",
    "Chapter",
    "Campaign",
    "For",
    "From",
    "He",
    "Her",
    "His",
    "I",
    "If",
    "In",
    "Is",
    "It",
    "King",
    "Kingdom",
    "Lady",
    "Let",
    "Many",
    "May",
    "Minister",
    "My",
    "No",
    "Now",
    "Of",
    "On",
    "One",
    "Only",
    "Or",
    "Our",
    "She",
    "Some",
    "The",
    "Their",
    "There",
    "These",
    "They",
    "This",
    "To",
    "Today",
    "Two",
    "When",
    "Where",
    "Which",
    "While",
    "Who",
    "With",
    "You",
    "Your",
    "Wesnoth",
    "North",
    "South",
    "East",
    "West",
    "Grey",
    "Great",
    "New",
    "Old",
    "First",
    "Last",
    "End",
    "Start",
    "Level",
    "Scenario",
    "Unit",
    "Gold",
    "Damage",
    "Attack",
    "Armor",
    "Armour",
    "Mage",
    "Warrior",
    "Village",
    "People",
    "Game",
    "Player",
    "Side",
    "Help",
    "Time",
    "Day",
    "Night",
    "DiD",
    "III",
    "Road",
    "Town",
    "Towns",
    "Farm",
    "Farms",
    "Sword",
    "Shield",
    "Horse",
    "Horses",
    "Elves",
    "Orcs",
    "Dwarves",
    "Human",
    "Humans",
    "Dragon",
    "Dragons",
    "Language",
    "English",
    "Korean",
    "Japanese",
    "Chinese",
    "Lua",
    "WML",
}
SOURCE_NAME_TOKEN = re.compile(
    r"(?<![A-Za-z])[A-Z][A-Za-z0-9’'-]{2,}(?![A-Za-z])"
)
RAW_NAME_TOKEN = re.compile(
    r"(?<![A-Za-z(])[A-Z][A-Za-z0-9’'-]{2,}(?![A-Za-z)])"
)


def candidate_context(source: str, translation: str) -> str:
    source = " ".join(source.split())
    translation = " ".join(translation.split())
    return f"{source[:180]} => {translation[:220]}"


def is_generated_name_list(block: str, source: str) -> bool:
    """Exclude runtime-generated comma-separated name tables from prose audits."""
    del source
    return (
        "random_names.lua" in block
        or "data/core/macros/names.cfg" in block
        or "Generator for " in block
    )


def find_candidates(path: Path) -> list[NameCandidate]:
    """Find source-name tokens that remain raw in a Korean translation."""
    candidates: list[NameCandidate] = []
    for block in path.read_text(encoding="utf-8").split("\n\n"):
        obsolete = any(line.startswith("#~") for line in block.splitlines())
        values = parse_field_values(obsolete_to_parseable(block) if obsolete else block)
        source = values.get("msgid", "")
        translation = values.get("msgstr", "")
        if (
            not source
            or not translation
            or "=" in source
            or "{" in source
            or is_generated_name_list(block, source)
            or (is_fuzzy(block) and not obsolete)
            or "msgid_plural" in values
            or "@" in source
        ):
            continue

        source_tokens = set(SOURCE_NAME_TOKEN.findall(source))
        # A bilingual name such as ``바락 고르(Barag Gór)`` is already
        # resolved. Do not report the source spelling inside its parentheses
        # as an unregistered raw English name.
        unpaired_translation = PARENTHESIZED.sub("", translation)
        for token in sorted(
            source_tokens & set(RAW_NAME_TOKEN.findall(unpaired_translation))
        ):
            if token in COMMON_SOURCE_WORDS:
                continue
            candidates.append(
                NameCandidate(
                    token,
                    path,
                    candidate_context(source, translation),
                    obsolete=obsolete,
                )
            )
    return candidates


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
                # Keep hyphenated Korean transliterations intact.  A source
                # such as ``Mal-Ravanal`` must pair with ``말-라바날`` rather
                # than the space-normalized ``말 라바날``.
                korean_tokens = re.findall(r"[가-힣]+(?:-[가-힣]+)*", korean_prefix)
                source_tokens = re.findall(r"[A-Za-z]+", source)
                source_token_count = len(source_tokens)
                korean = " ".join(korean_tokens[-source_token_count:])
                if korean:
                    pair = NamePair(source, korean, row["category"], row["source_term"])
                    by_source.setdefault(source, []).append(pair)

                # A compound name may occur later as individual components in
                # prose. Reuse the established transliteration for those
                # components, but never turn titles into names.
                # A glossary row that explicitly pairs the complete source
                # name must remain a single bilingual name. Do not infer
                # component pairs for it (for example, Mal A’kai).
                if (
                    not (
                        source.startswith("Mal ")
                        and f"({source})" in standard
                    )
                    and source == row["source_term"]
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


def remove_component_pair(
    translation: str, pair: NamePair
) -> tuple[str, int]:
    """Remove a source marker from a translated compound component."""
    pattern = re.compile(
        re.escape(pair.korean)
        + f"(?P<particle>{PARTICLE})"
        + re.escape(f"({pair.source})")
    )
    changed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        changed += 1
        return f"{pair.korean}{match.group('particle')}"

    return pattern.sub(replace, translation), changed


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


def configure_patterns(pairs: list[NamePair]) -> None:
    """Initialize the patterns shared by the audit and pairing pass."""
    SOURCE_PATTERNS.clear()
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
    TRANSLATION_PATTERNS.clear()
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
    SOURCE_TRANSLATION_PATTERNS.clear()
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


def process_file(path: Path, pairs: list[NamePair], apply: bool) -> tuple[int, int]:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    output: list[str] = []
    changed_messages = 0
    unresolved = 0
    # Some compound glossary rows intentionally pair only one component, for
    # example ``Naga Myrmidon`` -> ``나가 미르미돈(Myrmidon)``.  Do not let a
    # separate ``Naga`` row override the compound's translated race name.
    partial_compounds: dict[str, set[str]] = {}
    for pair in pairs:
        if pair.glossary_source == pair.source:
            continue
        source_tokens = set(re.findall(r"[A-Za-z][A-Za-z’'-]*", pair.glossary_source))
        paired_tokens = set(re.findall(r"[A-Za-z][A-Za-z’'-]*", pair.source))
        partial_compounds.setdefault(pair.glossary_source, set()).update(
            source_tokens - paired_tokens
        )
    excluded_token_compounds: dict[str, set[str]] = {}
    for compound, excluded_tokens in partial_compounds.items():
        for token in excluded_tokens:
            excluded_token_compounds.setdefault(token, set()).add(compound)

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
            or "=" in source
            or "{" in source
            or is_generated_name_list(block, source)
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
        for pair in pairs:
            if (
                pair.glossary_source != pair.source
                or pair.source not in excluded_token_compounds
                or not any(
                    compound in pairing_source
                    for compound in excluded_token_compounds[pair.source]
                )
            ):
                continue
            updated, count = remove_component_pair(updated, pair)
            message_changes += count
        whole_sources = {
            pair.source
            for pair in pairs
            if pair.glossary_source == pair.source
            and source_occurs(pair.source, pairing_source)
        }
        whole_components = {
            component
            for whole in whole_sources
            if len(re.findall(r"[A-Za-z][A-Za-z’'-]*", whole)) > 1
            for component in re.findall(r"[A-Za-z][A-Za-z’'-]*", whole)
        }
        for pair in sorted(pairs, key=lambda item: len(item.source)):
            if (
                pair.glossary_source == pair.source
                and any(
                    compound in pairing_source
                    for compound in excluded_token_compounds.get(pair.source, ())
                )
            ):
                continue
            if (
                pair.source != source
                and pair.source in whole_components
            ):
                continue
            if (
                pair.glossary_source != pair.source
                and pair.glossary_source in whole_sources
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
    parser.add_argument(
        "--candidates",
        action="store_true",
        help="report raw source-name candidates missing from the glossary",
    )
    args = parser.parse_args()

    pairs, conflicts = load_pairs(args.glossary)
    if args.candidates:
        candidates: dict[tuple[str, str], NameCandidate] = {}
        for path in sorted(args.work.glob("*.po")):
            for candidate in find_candidates(path):
                key = (candidate.path.name, candidate.source)
                candidates.setdefault(key, candidate)
        ordered = sorted(
            candidates.values(),
            key=lambda item: (item.path.name, item.source),
        )
        for candidate in ordered:
            print(
                f"candidate={candidate.path.name}:{candidate.source}\t"
                f"status={'obsolete' if candidate.obsolete else 'active'}\t"
                f"{candidate.context}"
            )
        active_count = sum(not candidate.obsolete for candidate in ordered)
        obsolete_count = sum(candidate.obsolete for candidate in ordered)
        print(f"candidates={len(candidates)}")
        print(f"active_candidates={active_count}")
        print(f"obsolete_candidates={obsolete_count}")
        return 1 if candidates else 0

    configure_patterns(pairs)
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
