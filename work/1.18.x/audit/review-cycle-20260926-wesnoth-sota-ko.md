# Review Cycle 2026-09-26: `wesnoth-sota-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-sota-ko.po`
- Follow-up to the earlier Wose correction cycle

## Changes

- Standardized plural race names:
  - `Merfolk Revenge` -> `인어들의 복수`
  - `Saurians` -> `사우리안들`
  - `Gryphons` -> `그리폰들`
  - `Dwarves` -> `난쟁이들`
  - `Elves` -> `엘프들`
- Standardized Saurian corpse labels:
  - `Walking Corpse (Saurian)` -> `걸어다니는 시체 (사우리안)`
  - `saurian corpses` -> `사우리안들의 시체`
- Changed `fish people` in dialogue to `어인들`.
- Updated matching glossary entries.
- Preserved existing Wose spellings:
  - `Wose` -> `워즈(Wose)`
  - `wose corpses` -> `워즈들(Woses)의 시체`

## Deferred

- Generic words such as `종족`, `동족`, and `부족` remain unchanged because they do not identify a specific race-name translation.
- No obsolete `#~` entries were rewritten.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-sota-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
