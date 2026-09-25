#!/usr/bin/env python3
"""Compare active Korean PO entries with en_GB, ja, zh_CN, and the archive.

This is a review aid, not an automatic translation merger.  It reports
candidate entries; a human must decide whether a difference is a real error,
an intentional Korean wording choice, or a code/documentation string.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import (  # noqa: E402
    is_fuzzy,
    key_for,
    parse_field_values,
)
from tools.audit_po_structure import PLACEHOLDER_RE  # noqa: E402
from tools.project_config import PO_ROOT, ROOT, WORK_KO  # noqa: E402


REFERENCE_KO = ROOT / "References" / "20250322_wesnoth_한국어번역"
RAW_ENGLISH = re.compile(r"[A-Za-z]{3,}")
KOREAN = re.compile(r"[가-힣]")


@dataclass(frozen=True)
class Entry:
    key: tuple[str, str, str]
    msgid: str
    msgid_plural: str
    msgstr: str
    translations: tuple[str, ...]
    path: Path


def active_entries(directory: Path) -> dict[tuple[str, str, str], Entry]:
    entries: dict[tuple[str, str, str], Entry] = {}
    for path in sorted(directory.glob("*.po")):
        for block in path.read_text(encoding="utf-8").split("\n\n"):
            if any(line.startswith("#~") for line in block.splitlines()):
                continue
            if is_fuzzy(block):
                continue
            values = parse_field_values(block)
            if not values.get("msgid"):
                continue
            key = key_for(values)
            translation_fields = [
                field
                for field in values
                if field == "msgstr" or field.startswith("msgstr[")
            ]
            translation_fields.sort(
                key=lambda field: 0
                if field == "msgstr"
                else int(field[7:-1]) + 1
            )
            translations = tuple(values[field] for field in translation_fields)
            translation = translations[0] if translations else ""
            entries[key] = Entry(
                key=key,
                msgid=values["msgid"],
                msgid_plural=values.get("msgid_plural", ""),
                msgstr=translation,
                translations=translations,
                path=path,
            )
    return entries


def source_path(locale: str) -> Path:
    return PO_ROOT / locale


def archive_entries() -> dict[tuple[str, str, str], Entry]:
    if not REFERENCE_KO.is_dir():
        return {}
    return active_entries(REFERENCE_KO)


def candidate_kind(entry: Entry, english: Entry | None) -> str | None:
    if not entry.msgstr:
        return "empty"
    if english and entry.msgstr.strip() == english.msgid.strip():
        if KOREAN.search(entry.msgstr) is None:
            return "english-identical"
    if english and RAW_ENGLISH.search(entry.msgstr):
        if KOREAN.search(entry.msgstr) is None:
            return "english-only"
    return None


def format_text(value: str, width: int = 260) -> str:
    return value.replace("\n", "\\n")[:width]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--work", type=Path, default=WORK_KO)
    args = parser.parse_args()

    ko = active_entries(args.work)
    locales = {locale: active_entries(source_path(locale)) for locale in ("en_GB", "ja", "zh_CN")}
    archive = archive_entries()
    missing = {
        locale: len(set(ko) - set(entries))
        for locale, entries in locales.items()
    }
    print(
        f"active_keys ko={len(ko)} en_GB={len(locales['en_GB'])} "
        f"ja={len(locales['ja'])} zh_CN={len(locales['zh_CN'])} "
        f"archive={len(archive)}"
    )
    print("missing_source_keys " + " ".join(f"{k}={v}" for k, v in missing.items()))

    candidates: list[tuple[str, Entry, Entry | None, Entry | None, Entry | None, Entry | None]] = []
    for key, entry in sorted(ko.items(), key=lambda item: (item[1].path.name, item[1].msgid)):
        en = locales["en_GB"].get(key)
        kind = candidate_kind(entry, en)
        if kind:
            candidates.append((kind, entry, en, locales["ja"].get(key), locales["zh_CN"].get(key), archive.get(key)))

    print(f"english_residue_candidates={len(candidates)}")
    for kind, ko_entry, en, ja, zh, ref in candidates[: None if args.all else args.limit]:
        print(f"\n[{kind}] {ko_entry.path.name}")
        print(f"EN: {format_text(en.msgid if en else ko_entry.msgid)}")
        print(f"KO: {format_text(ko_entry.msgstr)}")
        if ja:
            print(f"JA: {format_text(ja.msgstr)}")
        if zh:
            print(f"ZH: {format_text(zh.msgstr)}")
        if ref and ref.msgstr and ref.msgstr != ko_entry.msgstr:
            print(f"REF: {format_text(ref.msgstr)}")

    structure_candidates = 0
    for key, entry in ko.items():
        en = locales["en_GB"].get(key)
        if not en:
            continue
        source_forms = [en.msgid]
        if en.msgid_plural:
            source_forms.append(en.msgid_plural)
        if any(
            sorted(
                PLACEHOLDER_RE.findall(
                    source_forms[min(index, len(source_forms) - 1)]
                )
            )
            != sorted(PLACEHOLDER_RE.findall(translation))
            for index, translation in enumerate(entry.translations)
        ):
            structure_candidates += 1
    print(f"placeholder_candidates={structure_candidates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
