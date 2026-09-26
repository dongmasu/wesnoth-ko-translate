# Review Cycle 2026-09-26: `wesnoth-tutorial-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-tutorial-ko.po`
- Focus: tutorial terminology, Elf naming, healing terminology, and obvious spacing errors

## Changes

- Standardized active `Elf/Elvish` translations from `요정` to `엘프` forms.
- Standardized gameplay healing terminology:
  - `heal/healing` -> `회복`
  - `healer` -> `회복사`
  - `cure poison` remains `독을 치료`
- Changed `faerie fire` to `요정 불꽃`.
- Corrected obvious spacing and grammar issues:
  - `한 차례동안` -> `한 차례 동안`
  - `두명의 엘프들` -> `엘프 두 명`
  - `끝장낼때까지` -> `끝장낼 때까지`
  - `감소 합니다` -> `감소합니다`
  - `회복를` -> `회복을`
  - `회복효과` -> `회복 효과`
- Corrected the active tutorial sentence errors `진영에는` -> `진영은` and
  `최대 차례 수내` -> `최대 차례 수 내`.
- Synchronized glossary entries for `Multiple Healers` and `Healers and Villages`.

## Deferred

- The obsolete `#~` tutorial entries were not rewritten.
- `독을 치료` was preserved because it corresponds to `cure`, not `heal`.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-tutorial-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
- Existing `glossary.tsv` trailing-tab formatting was preserved.
