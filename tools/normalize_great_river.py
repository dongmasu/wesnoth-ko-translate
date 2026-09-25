#!/usr/bin/env python3
"""Normalize reviewed Great River translations in active Korean PO entries."""

from __future__ import annotations

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import (  # noqa: E402
    is_fuzzy,
    parse_field_values,
    replace_msgstr_fields,
)
from tools.project_config import WORK_KO  # noqa: E402


CANONICAL = "위대한 강"
GREAT_RIVER_RE = re.compile(r"\bgreat river\b", re.IGNORECASE)
STANDALONE_OLD_TERM_RE = re.compile(
    r"(?<![가-힣])(한강|대하)(에서|으로|까지|보다|처럼|을|를|이|가|은|는|의|에|와|과|도|로|만)?"
    r"(?![가-힣])"
)
PARTICLE_REPLACEMENTS = {
    "을": "을",
    "를": "을",
    "이": "이",
    "가": "이",
    "은": "은",
    "는": "은",
    "의": "의",
    "에": "에",
    "와": "과",
    "과": "과",
    "도": "도",
    "로": "으로",
    "만": "만",
    "에서": "에서",
    "으로": "으로",
    "까지": "까지",
    "보다": "보다",
    "처럼": "처럼",
}
CANONICAL_PARTICLE_REPAIRS = (
    (re.compile(r"위대한 강를"), "위대한 강을"),
    (re.compile(r"위대한 강와"), "위대한 강과"),
    (re.compile(r"위대한 강로"), "위대한 강으로"),
    (re.compile(r"위대한 강가 합류"), "위대한 강이 합류"),
)


def normalize_translation(translation: str) -> str:
    """Replace only standalone Great River names, not substrings of words."""
    for pattern, replacement in CANONICAL_PARTICLE_REPAIRS:
        translation = pattern.sub(replacement, translation)

    def replace(match: re.Match[str]) -> str:
        particle = match.group(2) or ""
        return CANONICAL + PARTICLE_REPLACEMENTS.get(particle, particle)

    return STANDALONE_OLD_TERM_RE.sub(replace, translation)


def update_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = values.get("msgstr")
        if (
            not source
            or translation is None
            or any(line.startswith("#~") for line in block.splitlines())
            or is_fuzzy(block)
            or not GREAT_RIVER_RE.search(source)
        ):
            output.append(block)
            continue

        target = normalize_translation(translation)
        if target != translation:
            output.append(replace_msgstr_fields(block, {"msgstr": target}))
            changed += 1
        else:
            output.append(block)

    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = update_file(path)
        if changed:
            print(f"{path.name}: {changed} message(s)")
            total += changed
    print(f"total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
