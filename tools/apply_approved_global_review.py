#!/usr/bin/env python3
"""Apply the approved, context-limited global terminology review."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.audit_and_pair_embedded_names import replace_obsolete_msgstr_fields
from tools.merge_reference_translations import replace_msgstr_fields
from tools.project_config import WORK_KO


FIELD_RE = re.compile(r"^(msgid|msgstr(?:\[\d+\])?)\s+(.+)$")
GAMEPLAY_MARKERS = (
    "[heals]",
    "[regenerate]",
    "data/core/",
    "doc/manual/",
    "data/campaigns/under_the_burning_suns/",
    "src/help/",
)


def parse_fields(block: str) -> dict[str, str]:
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


def replace_race_terms(translation: str) -> str:
    # Dwarf is a distinct fantasy race in Wesnoth; keep it separate from
    # generic Korean "난쟁이" descriptions.
    return (
        translation.replace("엘프족", "엘프들")
        .replace("난쟁이족", "드워프들")
        .replace("난쟁이들", "드워프들")
        .replace("난쟁이의", "드워프의")
        .replace("난쟁이제", "드워프제")
        .replace("난쟁이", "드워프")
        .replace("사우리언족", "사우리안들")
        .replace("사우리언", "사우리안")
    )


def replace_explicit_race_plurals(source: str, translation: str) -> str:
    source_lower = source.lower()
    plural_replacements = {
        "orcs": ("오크족", "오크들"),
        "humans": ("인간족", "인간들"),
        "drakes": ("반룡족", "반룡들"),
        "goblins": ("고블린족", "고블린들"),
        "mermen": ("인어족", "인어들"),
        "nagas": ("나가족", "나가들"),
        "ogres": ("오우거족", "오우거들"),
        "trolls": ("트롤족", "트롤들"),
        "woses": ("엔트족", "워즈들(Woses)"),
    }
    for source_token, (old, new) in plural_replacements.items():
        if re.search(rf"\b{re.escape(source_token)}\b", source_lower):
            translation = translation.replace(old, new)
    return translation


def replace_wose_terms(source: str, translation: str) -> str:
    lower = source.lower()
    if "woses" not in lower and "wose" not in lower:
        return translation

    if source.startswith("Bramwythl the Wose"):
        return translation.replace(
            "나모 브람위슬(Bramwythl)",
            "워즈(Wose) 브람위슬(Bramwythl)",
        ).replace("나모들", "워즈들(Woses)").replace("나모 공동체", "워즈 공동체")
    if "wose-born allies" in lower:
        return translation.replace("나모붙이 동맹군", "워즈 태생 동맹군")
    if source == "Woses":
        return "워즈들(Woses)"
    if "woses do not receive" in lower:
        return translation.replace("워스", "워즈들(Woses)")
    if "woses" in lower:
        return (
            translation.replace("나무정령들", "워즈들(Woses)")
            .replace("나무정령", "워즈들(Woses)")
            .replace("나모들", "워즈들(Woses)")
            .replace("워스", "워즈들(Woses)")
        )
    if "wose" in lower:
        return (
            translation.replace("나무정령", "워즈(Wose)")
            .replace("나모", "워즈(Wose)")
            .replace("워스", "워즈(Wose)")
        )
    return translation


def replace_gameplay_healing(source: str, translation: str, block: str) -> str:
    lower = source.lower()
    source_is_cure = "curer" in lower or re.search(r"\bcure\b|\bcures\b", lower)
    source_is_heal = (
        re.search(r"\bheal(?:s|ed|ing|er|ers)?\b", lower) is not None
        and "healing senses" not in lower
        and "healing art" not in lower
    )
    gameplay = (
        any(marker in block.lower() for marker in GAMEPLAY_MARKERS)
        or source in {"Cures", "female^Cures"}
        or source.startswith("This unit heals")
        or source.startswith("The unit will heal")
        or source.startswith("a fully-healed")
        or "melee attack heals" in lower
    )

    if source_is_cure and "curer" in lower:
        translation = translation.replace("치유사", "치료사").replace("치유자", "치료사")
    if source_is_cure:
        translation = translation.replace("치유사", "치료사").replace("치유자", "치료사")
        translation = translation.replace("치유", "치료")
    if source in {"Cures", "female^Cures"}:
        translation = translation.replace("치유", "치료")
    if "<i>cures</i>" in lower:
        translation = translation.replace("치유", "치료")

    if not (source_is_heal and gameplay):
        return translation

    translation = translation.replace("치유사", "회복사").replace("치유자", "회복사")
    translation = translation.replace("치유", "회복")
    return translation


def repair_common_combinations(translation: str) -> str:
    return (
        translation.replace("회복를", "회복을")
        .replace("회복와", "회복과")
        .replace("회복가", "회복이")
        .replace("탈수를 회복할", "탈수를 치료할")
        .replace("워즈들(Woses)는", "워즈들(Woses)은")
        .replace("워즈들(Woses)가", "워즈들(Woses)이")
        .replace("나모 기준", "워즈 기준")
    )


def update_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    output: list[str] = []
    changed = 0
    for block in blocks:
        obsolete = any(line.startswith("#~") for line in block.splitlines())
        parseable_block = (
            "\n".join(line[3:] if line.startswith("#~ ") else line for line in block.splitlines())
            if obsolete
            else block
        )
        values = parse_fields(parseable_block)
        source = values.get("msgid", "")
        translation = values.get("msgstr", "")
        if not source or not translation:
            output.append(block)
            continue

        updated = replace_race_terms(translation)
        updated = replace_explicit_race_plurals(source, updated)
        updated = replace_wose_terms(source, updated)
        updated = replace_gameplay_healing(source, updated, block)
        updated = repair_common_combinations(updated)
        if updated != translation:
            if obsolete:
                block = replace_obsolete_msgstr_fields(block, {"msgstr": updated})
            else:
                block = replace_msgstr_fields(block, {"msgstr": updated})
            changed += 1
        output.append(block)

    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = update_file(path)
        if changed:
            print(f"{path.name}: {changed}")
            total += changed
    print(f"total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
