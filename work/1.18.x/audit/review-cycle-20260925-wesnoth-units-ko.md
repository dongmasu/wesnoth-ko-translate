# Review Cycle 2026-09-26: `wesnoth-units-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-units-ko.po`
- Reason: follow-up review for established terminology rules, especially
  `faerie`, `Nagas`, and `Saurian`

## Changes

- Corrected `true faerie` from the erroneous `진정한 엘프가` to
  `진짜 요정`.
- Standardized active `faerie fire` descriptions to `요정 불꽃`.
- Corrected `Nagas` to `나가들`.
- Standardized active `Saurian` unit names and descriptions to
  `사우리안`/`사우리안들`, removing mixed `도마뱀`, `도마뱀족`, and
  `사우리언` forms.
- Updated the corresponding glossary entries for the changed Saurian
  unit names.
- Preserved obsolete (`#~`) historical translations.

## Verification

- `msgfmt --check --check-format`: passed
- `audit_po_structure.py`: passed
- `audit_glossary.py`: passed
- `git diff --check` for the PO: passed
- Follow-up check: corrected a leading tab on the first continuation line of
  the active `Saurian Oracle` description. The Korean translation itself was
  already present; this was a PO structure issue that caused the completion
  auditor to report one false untranslated entry.
- After the correction, the directory-wide completion audit reports
  `wesnoth-units-ko.po` as `untranslated=0` and `fuzzy=0`.

## Deferred and Follow-up

- No further high-confidence active terminology mismatch was found in this
  file.
- The remaining obsolete `사우리언` entry is intentionally unchanged.
- The follow-up decision standardized active `Dwarf`, `Dwarves`, and
  `Dwarvish` translations to `드워프`, `드워프들`, and the corresponding
  `드워프의`/`드워프제` forms across race labels, unit names, and prose.
