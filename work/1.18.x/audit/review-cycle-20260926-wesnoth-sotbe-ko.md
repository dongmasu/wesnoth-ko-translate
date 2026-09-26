# Review Cycle 2026-09-26: `wesnoth-sotbe-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-sotbe-ko.po`
- Applied the confirmed race-name and Wose terminology rules

## Changes

- Corrected three active `tree-shagger` references from the obsolete
  `나무붙이` expression to context-appropriate `워즈(Wose)` and
  `워즈들(Woses)`.
- Fixed nearby spacing and sentence-boundary errors in those dialogue and
  narrative lines.

- `Dwarves` -> `난쟁이들`
- `Elves` -> `엘프들`
- `saurians` -> `사우리안들`
- `wose-born weaklings` -> `워즈(Wose) 태생들`
- `wose-born` -> `워즈(Wose) 태생`

## Deferred

- Generic uses of `종족`, `동족`, `부족`, and `나무붙이`-style non-Wose expressions were not changed without a direct source-term confirmation.
- No obsolete `#~` entries were rewritten.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-sotbe-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
