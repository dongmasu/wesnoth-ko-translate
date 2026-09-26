# Review Cycle 2026-09-26: `wesnoth-dm-ko.po` prose follow-up

## Scope

- Target: `work/1.18.x/ko/wesnoth-dm-ko.po`
- Focus: long narrative entries and active dialogue with clear semantic,
  grammar, spacing, or proper-name issues
- Obsolete(`#~`) entries were not edited
- Existing approved DM changes were preserved

## High-Confidence Fixes

| ID | Area | Change |
| --- | --- | --- |
| H-DM-P-001 | Narrative wording | Reordered the opening sentence so the Academy is correctly located on the Isle of Alduin. |
| H-DM-P-002 | Spacing | Fixed clear spacing errors including `가진 것도`, `예상했던 것보다`, `모여 있는`, `후회하지 않을 거요`, and `악명 높지`. |
| H-DM-P-003 | Grammar | Corrected malformed constructions such as `오크들은 ... 피했다` to `오크들을 ... 피했다` and improved the army description against raiding orcs. |
| H-DM-P-004 | Spacing and particles | Corrected `닫아야 하는데`, `길 잃은`, `상대하는 데`, `책을`, and related sentence spacing. |
| H-DM-P-005 | Proper wording | Fixed `산 자`, `이리 와서`, `두려움 없이`, and `연관 짓지`. |
| H-DM-P-006 | Narrative spacing | Fixed `어느 날`, `분쟁 지역`, `미친 짓`, `며칠 동안`, `취할 만한`, and `소유할 만한`. |
| H-DM-P-007 | Repeated dialogue typo | Corrected active `안돼` forms to `안 돼` and `한 거냐` spacing. |

## Deferred

- Conversational `금/돈` choices where both can be valid in context.
- Broad register and sentence-style polishing where the meaning is already
  recoverable.
- Obsolete Wose entries, which remain historical data and are not active.

## Verification

- `msgfmt --check`: passed
- PO structure audit: markup `0`, placeholder `0`, newline `0`
- Glossary audit: `errors=0`, `warnings=0`
- Glossary-to-PO regression test: passed

## Next File

Continue automatically with the next PO in order, `wesnoth-dw-ko.po`.
