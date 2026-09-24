#!/usr/bin/env python3
"""Extract short, translated PO entries as glossary candidates."""

from __future__ import annotations

import ast
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PO_ROOT = ROOT / "po" / "1.18.x"
WORK_KO_ROOT = ROOT / "work" / "1.18.x" / "ko"
WORK_GLOSSARY = ROOT / "work" / "1.18.x" / "glossary.tsv"
OUTPUT = ROOT / "work" / "1.18.x" / "glossary-candidates.tsv"
INVENTORY_OUTPUT = ROOT / "work" / "1.18.x" / "glossary-inventory.tsv"
UNTRANSLATED_OUTPUT = ROOT / "work" / "1.18.x" / "glossary-untranslated.tsv"
FIELD_RE = re.compile(r"^(msgid|msgstr(?:\[\d+\])?)\s+(.+)$")
WORD_RE = re.compile(r"^[\wÀ-ÿ][\wÀ-ÿ' -]*$", re.UNICODE)


def parse_po(path: Path) -> dict[str, str]:
    messages: dict[str, str] = {}
    msgid = None
    msgstr = None
    current = None
    fuzzy = False
    obsolete = False

    def finish() -> None:
        nonlocal msgid, msgstr, current, fuzzy, obsolete
        if (
            msgid
            and msgstr
            and not fuzzy
            and not obsolete
            and msgid not in messages
        ):
            messages[msgid] = msgstr
        msgid = msgstr = current = None
        fuzzy = obsolete = False

    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.startswith("#~"):
            obsolete = True
        elif line.startswith("#,") and "fuzzy" in line:
            fuzzy = True

        match = FIELD_RE.match(line)
        if match:
            field, raw = match.groups()
            if field == "msgid":
                if msgid is not None:
                    finish()
                msgid = ast.literal_eval(raw)
                current = "msgid"
            elif msgid is not None:
                msgstr = ast.literal_eval(raw)
                current = "msgstr"
            continue

        if line.startswith('"') and current:
            value = ast.literal_eval(line)
            if current == "msgid":
                msgid = (msgid or "") + value
            else:
                msgstr = (msgstr or "") + value
        elif not line.strip():
            finish()

    return messages


def locale_messages(locale: str, root: Path = PO_ROOT) -> dict[str, Counter[str]]:
    messages: dict[str, Counter[str]] = defaultdict(Counter)
    for path in (root / locale).glob("*.po"):
        for source, translation in parse_po(path).items():
            messages[source][translation] += 1
    return messages


def existing_sources() -> set[str]:
    with WORK_GLOSSARY.open(encoding="utf-8", newline="") as stream:
        return {
            row["source_term"]
            for row in csv.DictReader(stream, delimiter="\t")
            if row.get("source_term")
        }


def is_candidate(source: str) -> bool:
    words = source.split()
    if not 1 <= len(words) <= 4 or len(source) > 50:
        return False
    if "\\n" in source or "<" in source or "%" in source or "$" in source:
        return False
    if source.endswith((".", "!", "?", ";")):
        return False
    return bool(WORD_RE.fullmatch(source))


def is_inventory_entry(source: str) -> bool:
    if not source or len(source) > 100 or len(source.split()) > 8:
        return False
    if (
        any(character in source for character in "\n\r\t")
        or "\\n" in source
        or "<" in source
        or "%" in source
        or "$" in source
    ):
        return False
    if source.endswith((".", "!", "?", ";")):
        return False
    return True


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
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


def main() -> None:
    english = locale_messages("en_GB")
    korean = locale_messages("ko", WORK_KO_ROOT.parent)
    japanese = locale_messages("ja")
    chinese = locale_messages("zh_CN")
    existing = existing_sources()
    rows = []
    inventory = []
    untranslated = []

    for source in sorted(korean):
        if source in existing or not is_candidate(source):
            continue
        translations = {
            "ko": korean[source].most_common(1)[0][0],
            "ja": japanese.get(source, Counter()).most_common(1),
            "zh_CN": chinese.get(source, Counter()).most_common(1),
        }
        if not translations["ja"] or not translations["zh_CN"]:
            continue
        korean_variants = [
            translation for translation, _ in korean[source].most_common()
        ]
        rows.append(
            {
                "source_term": source,
                "standard_korean": translations["ko"],
                "reference_japanese": translations["ja"][0][0],
                "reference_chinese": translations["zh_CN"][0][0],
                "category": "candidate",
                "forbidden_terms": "; ".join(
                    translation
                    for translation in korean_variants
                    if translation != translations["ko"]
                ),
                "notes": "자동 추출 후보; 문맥과 중복 표기를 검토한 뒤 본 용어집으로 승격",
            }
        )

    for source in sorted(english):
        if not is_inventory_entry(source):
            continue
        korean_translation = (
            korean.get(source, Counter()).most_common(1)[0][0]
            if korean.get(source)
            else ""
        )
        review_kind = (
            "untranslated"
            if not korean_translation
            else "same_as_source"
            if korean_translation == source
            else "inventory"
        )
        inventory_row = {
                "source_term": source,
                "standard_korean": korean_translation,
                "reference_japanese": japanese.get(source, Counter()).most_common(1)[0][0]
                if japanese.get(source)
                else "",
                "reference_chinese": chinese.get(source, Counter()).most_common(1)[0][0]
                if chinese.get(source)
                else "",
                "category": "unclassified",
                "forbidden_terms": "",
                "notes": (
                    "한국어 msgstr가 비어 있어 번역 대상"
                    if not korean_translation
                    else "원문과 동일한 한국어 표기인지 검토 필요"
                    if korean_translation == source
                    else "원문 기반 전체 후보; 품사·문맥·고유명사 여부를 검토한 뒤 용어집으로 승격"
                )
                + f" [review={review_kind}]",
            }
        inventory.append(inventory_row)
        if review_kind == "untranslated":
            untranslated.append(inventory_row)

    write_rows(OUTPUT, rows)
    write_rows(INVENTORY_OUTPUT, inventory)
    write_rows(UNTRANSLATED_OUTPUT, untranslated)
    print(f"wrote {len(rows)} candidates to {OUTPUT}")
    print(f"wrote {len(inventory)} inventory entries to {INVENTORY_OUTPUT}")
    print(f"wrote {len(untranslated)} untranslated entries to {UNTRANSLATED_OUTPUT}")


if __name__ == "__main__":
    main()
