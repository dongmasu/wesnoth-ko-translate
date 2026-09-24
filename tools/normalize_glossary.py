#!/usr/bin/env python3
"""Normalize the curated glossary and synchronize it with the work PO files."""

from __future__ import annotations

import argparse
import ast
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_config import GLOSSARY, PO_ROOT, WORK_KO


FIELDS = (
    "source_term",
    "standard_korean",
    "reference_japanese",
    "reference_chinese",
    "category",
    "forbidden_terms",
    "notes",
)

WORD_RE = re.compile(r"\b[\w'-]+\b")
FIELD_RE = re.compile(r"^(msgid|msgstr(?:\[\d+\])?)\s+(.+)$")
SENTENCE_START_RE = re.compile(
    r"(?i)^(?:"
    r"a player has|a player is|the selected file is|"
    r"you\b|we\b|they\b|he\b|she\b|it\b|there\b|this\b|that\b|"
    r"if\b|when\b|while\b|because\b|please\b|let\b|"
    r"be sure\b|no,\s|"
    r"copy\b|clear\b|find\b|defeat\b|destroy\b|die\b|"
    r"eliminate\b|escape\b|force\b|hold\b|improve(?:s)?\b|"
    r"increase(?:s)?\b|investigate\b|join\b|kill\b|"
    r"launch\b|load\b|make\b|maintain\b|move\b|"
    r"protect\b|raise\b|reinitialize\b|remove\b|rescue\b|"
    r"randomize\b|release\b|reload(?:ing)?\b|"
    r"save\b|show\b|summon\b|toggle\b|"
    r"when\b|which\b"
    r")"
)

UI_MARKERS = (
    "[grid]",
    "[label]",
    "[button]",
    "[menu_button]",
    "[menu]",
    "[option]",
    "[checkbox]",
    "[toggle_button]",
    "[slider]",
    "[text_box]",
    "[list]",
    "[tooltip]",
    "[column]",
    "[row]",
    "[topic]",
    "[section]",
    "[widget]",
    "[column]",
    "[set_menu_item]",
    "[advanced_preference]",
    "[toggle_button]",
)

STABLE_CONTEXTS = {
    "alignment",
    "campaign_name",
    "combat_range",
    "difficulty",
    "faction",
    "identifier",
    "item_name",
    "magic",
    "music_title",
    "person_name",
    "place_name",
    "rank",
    "race_name",
    "terrain",
    "trait",
    "unit_name",
    "unit_role",
}

PLACE_WORDS = re.compile(
    r"(?i)\b(?:bay|bridge|castle|cave|cavern|coast|desert|fall|"
    r"forest|fort|gate|grove|hill|hills|isle|island|lake|marsh|"
    r"mount|mountain|pass|plain|river|road|sea|shore|swamp|"
    r"temple|town|village|valley|wall|wood)\b"
)

EXPLICIT_PLACE_NAMES = {
    "Basilica of Li’sar",
    "Blackwater Port",
    "Clearwater Lake",
    "East Gate",
    "East Tower",
    "Ford of Alyas",
    "Ford of Tifranur",
    "Fort Brell",
    "Fort Miryen",
    "Garard’s Hold",
    "Great Continent",
    "Great Ocean",
    "Great River",
    "Gryphon Mountain",
    "Heart Mountains",
    "High Pass",
    "Karmarth Hills",
    "Kingdom of Wesnoth",
    "Lake Naga",
    "Lord Alric’s Palace",
    "Lord Gaelyc’s Citadel",
    "North Bridge",
    "North Tower",
    "Port of Elensefar",
    "River Telfar",
    "Sir Efran’s Castle",
    "Sir Seoraery’s Keep",
    "South Bastion",
    "Southwest Elven Lands",
    "The Bay of Pearls",
    "The Ford of Abez",
    "The Great Valley",
    "The Isle of Alduin",
    "The Road to Weldyn",
    "The Swamp of Esten",
    "West Gate",
    "West Tower",
    "Wolf Coast",
}

KNOWN_NON_PLACE_TERMS = {
    "island factor",
    "village density",
}

CONTEXT_PREFIXES = {
    "teamname": "faction",
    "faction": "faction",
    "feature": "ui",
    "controller": "ui",
    "filesystem": "ui",
    "addon_tag": "ui",
    "addon_state": "ui",
    "timespan": "ui",
}

KNOWN_NON_ENGLISH_IDENTIFIERS = {
    "HP: ",
    "XP: ",
    "MP: ",
    "Oldania ADF Std",
    "DejaVu Sans Mono",
    "∞",
}

RACE_NAMES = {
    "Drakes",
    "Dwarves",
    "Elves",
    "Goblins",
    "Humans",
    "Merfolk",
    "Naga",
    "Orcs",
    "Saurians",
    "Trolls",
}

AUTO_NOTE_RE = re.compile(
    r"^(?:"
    r"대소문자를 구분하는 source_term 기준으로 유지; "
    r"category=[^;]+; PO locale 실제 표현을 대조"
    r"|PO locale 실제 표현과 고유명사 여부를 대조"
    r")$"
)


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


def load_locale(
    paths: list[Path],
) -> tuple[dict[str, Counter[str]], dict[str, set[str]]]:
    translations: dict[str, Counter[str]] = defaultdict(Counter)
    contexts: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            values, comments = parse_block(block)
            source = values.get("msgid", "")
            if not source:
                continue
            translation = values.get("msgstr", "")
            if translation:
                translations[source][translation] += 1
            contexts[source].update(comments)
    return translations, contexts


def choose(counter: Counter[str], fallback: str) -> str:
    return counter.most_common(1)[0][0] if counter else fallback


def has_marker(comments: set[str], marker: str) -> bool:
    return any(marker in comment for comment in comments)


def infer_context(row: dict[str, str], comments: set[str]) -> str:
    source = row["source_term"]
    current = row["category"]

    if source in KNOWN_NON_PLACE_TERMS:
        return "term"
    if source in EXPLICIT_PLACE_NAMES:
        return "place_name"
    if source in RACE_NAMES:
        return "race_name"

    if "^" in source:
        prefix = source.split("^", 1)[0]
        if prefix in CONTEXT_PREFIXES:
            return CONTEXT_PREFIXES[prefix]

    if has_marker(comments, "[scenario]") or has_marker(comments, "[campaign]"):
        return "campaign_name"
    if has_marker(comments, "[race]"):
        return "race_name"
    if has_marker(comments, "[music]"):
        return "music_title"
    if has_marker(comments, "[unit]") or has_marker(comments, "[unit_type]"):
        return "unit_name"
    if has_marker(comments, "[side]") or has_marker(comments, "[multiplayer_side]"):
        return "faction"
    if has_marker(comments, "[terrain_type]"):
        return "terrain"
    if any(has_marker(comments, marker) for marker in (
        "[item]", "[artifact]", "[object]"
    )):
        return "item_name"
    if has_marker(comments, "[trait]"):
        return "trait"
    if (
        has_marker(comments, "[attack]")
        or has_marker(comments, "[attacks]")
        or has_marker(comments, "[effect]")
    ):
        return "attack_type"
    if has_marker(comments, "[leader]"):
        words = WORD_RE.findall(source)
        if len(words) <= 4:
            return "person_name"
        return "proper_noun"
    if has_marker(comments, "[label]") and (
        PLACE_WORDS.search(source) or current == "place_name"
    ):
        return "place_name"
    if has_marker(comments, "[event]"):
        return "proper_noun"
    if any(marker in comments for marker in UI_MARKERS):
        if re.match(r"(?i)^(?:drop|choose|select|open|close|load|save|"
                    r"show|hide|run|change|toggle|copy|remove|"
                    r"recruit|recall|move)\b", source):
            return "command"
        return "ui"

    if current in STABLE_CONTEXTS:
        return current
    if source in KNOWN_NON_ENGLISH_IDENTIFIERS:
        return "identifier"
    if current == "proper_noun":
        return "proper_noun"
    return "term"


def is_sentence_like(
    row: dict[str, str],
    context: str,
    comments: set[str],
) -> bool:
    source = row["source_term"]
    if re.fullmatch(r"\s*\d+\s*", source):
        return True
    if not WORD_RE.search(source) and source not in KNOWN_NON_ENGLISH_IDENTIFIERS:
        return True
    if context in {
        "campaign_name",
        "music_title",
        "unit_name",
        "person_name",
        "place_name",
        "proper_noun",
        "item_name",
    }:
        return False
    if has_marker(comments, "[objective]") or row["category"] == "objective":
        return True
    if "\n" in source or any(marker in source for marker in ("<", "%", "$")):
        return True
    if source.rstrip().endswith((".", "!", "?", ":")):
        return True
    words = WORD_RE.findall(source)
    if len(words) > 6:
        return True
    if context in {"ui", "command"} and len(words) <= 5:
        return False
    if source in {"You", "This Turn", "The password is"}:
        return True
    return bool(len(words) >= 3 and SENTENCE_START_RE.match(source))


def merge_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for row in rows:
        normalized = {field: row.get(field, "") for field in FIELDS}
        source = normalized["source_term"]
        if not source:
            continue
        if source not in merged:
            merged[source] = normalized
            continue
        current = merged[source]
        forbidden = {
            item.strip()
            for value in (current["forbidden_terms"], normalized["forbidden_terms"])
            for item in value.split(";")
            if item.strip()
        }
        current["forbidden_terms"] = "; ".join(sorted(forbidden))
        for field in ("reference_japanese", "reference_chinese", "notes"):
            if not current[field] and normalized[field]:
                current[field] = normalized[field]
    return list(merged.values())


def clean_forbidden_terms(row: dict[str, str]) -> None:
    standard = row["standard_korean"].strip()
    terms = {
        item.strip()
        for item in row["forbidden_terms"].split(";")
        if item.strip() and item.strip() != standard
    }
    row["forbidden_terms"] = "; ".join(sorted(terms))


def normalize(args: argparse.Namespace) -> tuple[int, int, int]:
    with args.glossary.open(encoding="utf-8", newline="") as stream:
        original = list(csv.DictReader(stream, delimiter="\t"))

    ko, ko_contexts = load_locale(sorted((args.work_ko).glob("*.po")))
    ja, _ = load_locale(sorted((args.po_root / "ja").glob("*.po")))
    zh, _ = load_locale(sorted((args.po_root / "zh_CN").glob("*.po")))
    all_rows = merge_rows(original)

    kept: list[dict[str, str]] = []
    removed = 0
    context_counts: Counter[str] = Counter()
    for row in all_rows:
        source = row["source_term"]
        comments = ko_contexts.get(source, set())
        context = infer_context(row, comments)
        if is_sentence_like(row, context, comments):
            removed += 1
            continue

        row["category"] = context
        row["standard_korean"] = choose(ko.get(source, Counter()), row["standard_korean"])
        row["reference_japanese"] = choose(
            ja.get(source, Counter()), row["reference_japanese"] or "not found"
        )
        row["reference_chinese"] = choose(
            zh.get(source, Counter()), row["reference_chinese"] or "not found"
        )
        clean_forbidden_terms(row)
        if AUTO_NOTE_RE.fullmatch(row["notes"].strip()):
            row["notes"] = ""
        kept.append(row)
        context_counts[context] += 1

    kept.sort(key=lambda row: row["source_term"])
    with args.glossary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(kept)

    print(f"input rows: {len(original)}")
    print(f"removed exact duplicate rows: {len(original) - len(all_rows)}")
    print(f"removed sentence-like rows: {removed}")
    print(f"output rows: {len(kept)}")
    print("contexts:")
    for context, count in context_counts.most_common():
        print(f"  {context}: {count}")
    return len(original), removed, len(kept)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glossary", type=Path, default=GLOSSARY)
    parser.add_argument("--work-ko", type=Path, default=WORK_KO)
    parser.add_argument("--po-root", type=Path, default=PO_ROOT)
    args = parser.parse_args()
    normalize(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
