# Review Cycle 2026-09-26: `wesnoth-ei-ko.po` follow-up

## Scope

- Target: `work/1.18.x/ko/wesnoth-ei-ko.po`
- Focus: shared terminology and clear active spacing errors after the earlier
  EI review
- Obsolete(`#~`) entries were not edited

## High-Confidence Fixes

| ID | Area | Change |
| --- | --- | --- |
| H-EI-P-001 | Shared proper name | Changed active `Whitefang` references from `흰송곳니` to `화이트팽(Whitefang)` in the clan and mercenary dialogue. |
| H-EI-P-002 | Spacing | Corrected active `안돼` forms to `안 돼`. |

## Deliberately Unchanged

- `wyrm → 도마뱀` in the two insult lines remains valid under the documented
  Wyrm exception for contemptuous dialogue.
- Obsolete `#~` lines containing older spacing or terminology were preserved.
- Existing `동부 침공`, `에스트마르크(Estmark)`, `사우리안`, and plural
  conventions remain unchanged.

## Verification

- `msgfmt --check`: passed
- PO structure audit: markup `0`, placeholder `0`, newline `0`
- Glossary audit: `errors=0`, `warnings=0`

## Next File

Continue automatically with the next PO in order.
