# Review Cycle 2026-09-26: `wesnoth-thot-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-thot-ko.po`

## Changes

- Applied the established Elf terminology in the existing changed entries:
  - `elves` -> `엘프들`
  - `elves` in the relevant dialogue -> `엘프들`
- `heal` -> `회복` in the Loremaster description.
- `dwarven-kind loremasters` -> `난쟁이 전승자들`.

## Review Result

- No active `나모`, `요정`, or `정령` issue was found.
- Existing unit names with uncertain established terminology were preserved.
- No obsolete `#~` entries were rewritten.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-thot-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
