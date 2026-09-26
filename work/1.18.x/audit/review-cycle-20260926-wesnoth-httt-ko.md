# Review Cycle 2026-09-26: `wesnoth-httt-ko.po` prose follow-up

## Scope

- Target: `work/1.18.x/ko/wesnoth-httt-ko.po`
- Focus: active dialogue and narrative entries with clear grammar and spacing
  errors
- Obsolete(`#~`) entries were not edited

## High-Confidence Fixes

| ID | Area | Change |
| --- | --- | --- |
| H-HTTT-P-001 | Spacing | Corrected active `안돼` forms to `안 돼`. |
| H-HTTT-P-002 | Spacing | Corrected `싸울테지만`, `싸울테니`, `한명`, `한명당`, `말탄`, and `잠깐동안`. |
| H-HTTT-P-003 | Compound verb spacing | Changed `실어나를` to `실어 나를`. |
| H-HTTT-P-004 | Auxiliary spacing | Changed `보내주겠소` to `보내 주겠소`. |

## Deferred

- Existing register choices and terminology such as `인어족`, `드워프`,
  and `검은물(Blackwater)` where the meaning remains clear.
- Broader prose style improvements requiring sentence-level comparison.

## Verification

- `msgfmt --check`: passed
- PO structure audit: markup `0`, placeholder `0`, newline `0`
- Glossary audit: `errors=0`, `warnings=0`

## Next File

Continue automatically with the next PO in order.
