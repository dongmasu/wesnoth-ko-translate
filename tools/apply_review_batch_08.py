#!/usr/bin/env python3
"""Apply exact wording fixes for shared UI strings found in the PO comparison."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import WORK_KO


TRANSLATIONS = {
    "(Intermediate level, 10 scenarios.)": "(중급 난이도, 10개 시나리오.)",
    "Clipboard support not found, contact your packager":
        "클립보드 지원을 찾을 수 없습니다. 패키지 관리자에게 문의하세요",
    "Do you really want to quit?": "정말로 종료하시겠습니까?",
    "Fights normally during unfavorable times of day/night":
        "낮/밤 중 불리한 시간대에도 평소처럼 싸울 수 있습니다.",
    "Map saved.": "지도가 저장되었습니다.",
    "No description available.": "설명이 없습니다.",
    "Overwrite?": "덮어쓰시겠습니까?",
    "Save Map As": "다른 이름으로 지도 저장",
    "Save Scenario As": "다른 이름으로 시나리오 저장",
    "Special Notes:": "특별 참고 사항:",
    "This trident gives merfolk the power to throw lightning at their enemies.":
        "이 삼지창은 인어가 적에게 번개를 던질 수 있게 합니다.",
    "This unit always strikes first with this attack, even if they are defending.":
        "이 유닛은 방어 중이라도 항상 이 공격으로 먼저 공격합니다.",
    "This unit is skilled in moving past enemies quickly, and ignores all enemy Zones of Control.":
        "이 유닛은 빠르게 적을 지나가는 데 능숙하며, 모든 적의 통제 권역을 무시합니다.",
}


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = TRANSLATIONS.get(source)
        if translation is None or "msgid_plural" in values:
            output.append(block)
            continue
        if values.get("msgstr", "") != translation:
            block = replace_msgstr_fields(block, {"msgstr": translation})
            changed += 1
        output.append(block)
    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = apply_file(path)
        if changed:
            print(f"{path.name}: {changed} entries reviewed")
            total += changed
    print(f"total: {total} entries reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
