# Review Cycle 2026-09-26: `wesnoth-tsg-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-tsg-ko.po`
- Focus: Elf/Faerie distinction and healing terminology

## Changes

- `Merfolk` in the recruitment explanation:
  - `인어족` -> `인어들`
- `arcane attack`:
  - `신령` -> `비전`
- `Elves`:
  - `엘프족` -> `엘프들`
- Troll dialogue:
  - `elfsies` -> `엘프들`
  - Removed incorrect `요정` references in the same dialogue.
- Game ability descriptions:
  - `heal/heals` -> `회복`

## Deferred

- Narrative `heal the mind` remains `정신을 치유하다`, where `치유` is natural prose rather than the HP recovery ability term.
- No obsolete `#~` entries were rewritten.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-tsg-ko.po`
- `python3 tools/audit_po_structure.py`: passed with zero mismatches
- `python3 tools/audit_glossary.py --glossary work/1.18.x/glossary.tsv --work-ko work/1.18.x/ko`: passed with zero errors and warnings
