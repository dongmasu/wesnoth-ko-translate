# Review Cycle 2026-09-26: final follow-up

## Scope

- Completed the remaining PO order after the earlier per-file reviews:
  `tsg`, `tutorial`, `units`, `utbs`, `wc`, and `wof`.
- Ran a narrow global follow-up for the same high-confidence spacing and typo
  patterns in already reviewed files.
- Obsolete (`#~`) entries were included in terminology standardization; they
  remain historical entries but are no longer exempt from corrections.

## Changes

- `tutorial`: corrected `진영은`, `최대 차례 수 내`, and active
  `1차례` spacing.
- `utbs`: corrected clear spacing, typo, and sentence-structure errors,
  including `회복사`, `탈수를 치료`, `3차례`, and `1차례`.
- `wof`: standardized active `18차례` and `24차례`.
- `sotbe`: standardized active turn-count spacing and `뭐 하는`.
- `dw`, `httt`, and `help`: corrected clear active spacing errors.
- `units`: corrected the active `오래전`, `될 때까지`, and related spacing.
- The previously deferred `드워프`/`난쟁이` decision is now resolved:
  `Dwarf`, `Dwarves`, and `Dwarvish` all use `드워프`, `드워프들`,
  and `드워프의`/`드워프제` as appropriate.
- Expanded the same review to obsolete (`#~`) entries across all PO files:
  standardized legacy race plurals, `사우리언` to `사우리안`, Wose/name
  pairings, and healing terminology where the English source established the
  gameplay meaning.
- Synchronized four glossary rows whose standards changed during the global
  obsolete review: `Fallen Lich Point`, `Naga Sentinel`, `Talking with Trolls`,
  and `Troll Flamecaster`.

## Verification

- `python3 -m unittest discover -s tests -v`: 142 tests passed.
- All active PO files pass `msgfmt --check --check-format`.
- `audit_po_completion.py`: 30 PO files, `untranslated=0`, `fuzzy=0`.
- `audit_po_structure.py`: zero markup, placeholder, and newline mismatches
  in all reviewed files.
- `audit_glossary.py`: `errors=0`, `warnings=0`.
- Obsolete-focused follow-up: no obsolete `msgstr` remains with the reviewed
  legacy forms `사우리언`, `반룡족`, `고블린족`, `인간족`, `인어족`,
  `나가족`, `오우거족`, `트롤족`, `엔트족`, `나모`, or `드워프족`.
