# Review Cycle 2026-09-26: `wesnoth-trow-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-trow-ko.po`
- Focus: race-name pluralization and naturalness after the confirmed terminology decision

## Changes

- Standardized active plural race names from `족` to `들`:
  - Orcs -> `오크들`
  - Humans -> `인간들`
  - Dwarves -> `난쟁이들`
  - Elves -> `엘프들`
  - Saurians -> `사우리안들`
  - Nagas -> `나가들`
  - Trolls -> `트롤들`
  - Drakes -> `반룡들`
  - Yetis -> `예티들`
- Corrected naturalness issues introduced by the normalization:
  - `오크들 몇놈` -> `오크 몇 놈`
  - `오크들 떼거리` -> `오크 떼거리`
  - `오크들 무리` -> `오크 무리`
- Updated the glossary entry for `Yetis`.

## Deferred

- Generic terms such as `종족`, `민족`, `동족`, and `부족` were preserved.
- The obsolete `#~ msgstr "나모 묘목"` entry was not rewritten.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-trow-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
