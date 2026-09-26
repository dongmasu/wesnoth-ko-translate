# Review Cycle: Elf and Faerie Terminology

- Date: 2026-09-26
- Scope: active Korean PO entries and glossary entries related to `Elf`, `Elvish`, `Elven`, and `faerie`

## Decisions Applied

- `Elf` -> `엘프`
- `Elves` -> `엘프들`
- `Elvish` and `Elven` -> `엘프의` or context-appropriate `엘프`
- `faerie` and `Faerie` -> `요정`
- `Faerie World` -> `요정계`
- `faerie fire` -> `요정 불꽃`
- `faerie touch` -> `요정의 손길`
- `forest spirits` and `water spirits` remain translated as spirit concepts, not `faerie`
- Removed obsolete glossary aliases `엘프족` and `요정들` from `Elves`

## Changes

- Corrected four active PO translations where `faerie` had been translated as `정령`.
- Updated matching glossary entries for `faerie`, `Elvish*`, Quenoth Elves, and the Elvish Treasury.
- Corrected the active Quenoth team name in `wesnoth-utbs-ko.po`.
- Obsolete `#~` entries were not modified.

## Verification

- `msgfmt --check --check-format`: passed for all Korean PO files.
- `python3 -m unittest tests.test_po_layout -q`: 30 tests passed.
- `python3 tools/audit_po_structure.py`: passed with zero mismatches.
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings.
- Active `faerie` entries translated as `정령`: none found.
