#!/usr/bin/env python3
"""Apply a high-confidence UI and core-rules translation review batch."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import GLOSSARY, WORK_KO


EXACT_TRANSLATIONS = {
    "Install Dependencies": "의존성 설치",
    "Victory:": "승리 조건:",
    "Defeat:": "패배 조건:",
    "Plan Unit Advance": "유닛 승급 계획",
    "Force advancement planning": "승급 계획 강제",
    "No planned advancement": "승급 대상 미설정",
    "Plan Advancement": "승급 계획",
    "This advancement is currently the default for all units of the same type":
        "이 승급은 현재 같은 유형의 모든 유닛에 적용되는 기본값입니다.",
    "Neutral units are unaffected by day and night, fighting equally well under "
    "both conditions.":
        "중립 유닛은 낮과 밤의 영향을 받지 않으며, 두 시간대에 똑같이 잘 싸웁니다.",
}

PREFIX_TRANSLATIONS = {
    "Liminal units fight best during the twilight times of day.": (
        "경계성 유닛은 황혼 시간대에 가장 잘 싸웁니다.\n\n"
        "황혼: 피해 +25%"
    ),
}

GLOSSARY_ROWS = {
    "Defeat:": ("패배 조건:", "敗北条件：", "失败：", "term"),
    "Force advancement planning": (
        "승급 계획 강제",
        "レベルアップ先設定の必須化",
        "强制计划升级",
        "term",
    ),
    "Install Dependencies": (
        "의존성 설치",
        "依存関係のインストール",
        "安装依赖项目",
        "term",
    ),
    "No planned advancement": (
        "승급 대상 미설정",
        "レベルアップ先未設定",
        "无计划升级方向",
        "term",
    ),
    "Plan Advancement": (
        "승급 계획",
        "レベルアップ先の設定",
        "计划升级",
        "term",
    ),
    "Plan Unit Advance": (
        "유닛 승급 계획",
        "ユニットレベルアップ先の設定",
        "计划单位升级",
        "term",
    ),
    "Victory:": ("승리 조건:", "勝利条件：", "胜利：", "term"),
}


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        if block.lstrip().startswith("#~"):
            output.append(block)
            continue
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation = EXACT_TRANSLATIONS.get(source)
        if translation is None:
            for prefix, candidate in PREFIX_TRANSLATIONS.items():
                if source.startswith(prefix):
                    translation = candidate
                    break
        if translation is None or "msgid_plural" in values:
            output.append(block)
            continue
        current = values.get("msgstr", "")
        if current != translation:
            block = replace_msgstr_fields(block, {"msgstr": translation})
            changed += 1
        output.append(block)
    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def update_glossary() -> int:
    with GLOSSARY.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
        fields = tuple(stream_line for stream_line in (rows[0].keys() if rows else ()))
    by_source = {row["source_term"]: row for row in rows}
    changed = 0
    for source, values in GLOSSARY_ROWS.items():
        korean, japanese, chinese, category = values
        row = by_source.get(source)
        if row is None:
            row = {
                "source_term": source,
                "standard_korean": korean,
                "reference_japanese": japanese,
                "reference_chinese": chinese,
                "category": category,
                "forbidden_terms": "",
                "notes": "",
            }
            rows.append(row)
            by_source[source] = row
            changed += 1
            continue
        updates = {
            "standard_korean": korean,
            "reference_japanese": japanese,
            "reference_chinese": chinese,
            "category": category,
            "forbidden_terms": "",
            "notes": "",
        }
        if any(row.get(key, "") != value for key, value in updates.items()):
            row.update(updates)
            changed += 1
    rows.sort(key=lambda row: row["source_term"])
    with GLOSSARY.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fields or (
                "source_term",
                "standard_korean",
                "reference_japanese",
                "reference_chinese",
                "category",
                "forbidden_terms",
                "notes",
            ),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    return changed


def main() -> int:
    total = 0
    for path in sorted(WORK_KO.glob("*.po")):
        changed = apply_file(path)
        if changed:
            print(f"{path.name}: {changed} entries reviewed")
            total += changed
    glossary_changed = update_glossary()
    print(f"PO entries reviewed: {total}")
    print(f"glossary rows updated: {glossary_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
