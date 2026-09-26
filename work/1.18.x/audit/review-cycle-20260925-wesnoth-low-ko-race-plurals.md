# Review Cycle 2026-09-25: `wesnoth-low-ko.po` race plurals

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-low-ko.po`
- Rule: explicit English plural groups use Korean `들`; `족` is not used as
  a plural marker.
- Existing dirty changes in this PO, including proper-name and glossary
  corrections unrelated to this cycle, were preserved.

## Changes

High-confidence direct references to plural groups were changed from `족` to
`들`, including:

- Orcs: `오크족` → `오크들`
- Elves: `엘프족` → `엘프들`
- Trolls: `트롤족` → `트롤들`
- Dwarves: `드워프족` or `난쟁이족` → `드워프들` or `난쟁이들`
- Saurians: `사우리안족` → `사우리안들`
- Humans: `인간족` → `인간들`

The edits cover direct dialogue, a scenario title, vocatives, and clear
subject/object references. They do not rewrite conceptual expressions such as
`엘프족의 역사`, `엘프족의 방식`, or other prose where `족` describes a
people or race as a concept rather than marking an English plural label.

## Verification

- `msgfmt --check --check-format`: passed for `wesnoth-low-ko.po`
- `git diff --check`: passed for the PO file
- Existing unrelated dirty changes were not reverted.

## Remaining Scope

Some narrative expressions in this PO still use `족` and require sentence-level
review to distinguish a conceptual race reference from an explicit plural
group. They remain unchanged in this cycle rather than being mechanically
rewritten.
