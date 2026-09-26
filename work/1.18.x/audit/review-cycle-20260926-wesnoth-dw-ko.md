# Review Cycle 2026-09-26: `wesnoth-dw-ko.po`

## Scope

- Target: `work/1.18.x/ko/wesnoth-dw-ko.po`
- Focus: active narrative and dialogue entries with high-confidence semantic,
  grammar, and spacing errors
- Obsolete(`#~`) entries were not edited

## High-Confidence Fixes

| ID | Area | Change |
| --- | --- | --- |
| H-DW-001 | Terminology | Changed `Saurian Slavers` from `사우리안 노예장들` to `사우리안 노예상들`; synchronized the glossary. |
| H-DW-002 | Dialogue meaning | Corrected `wish you had minded your own affairs` from a wrong negative construction to `자기 일에나 신경 썼어야 했다고 후회하게 될 거다`. |
| H-DW-003 | Narrative prose | Corrected the malformed Mal-Govon history sentence so `first`, `last`, and `every king in between` are represented correctly. |
| H-DW-004 | Spacing | Fixed clear active errors including `공격해 오지`, `몇 시간`, `한 시간`, `위엄 있는`, `도와줄 거라`, `안 돼`, `200여 년`, and `어디에 있는지`. |

## Deferred

- Broader register and colloquial style choices.
- Remaining long-sentence spacing candidates that require surrounding syntax
  review rather than blind replacement.
- Existing choices such as `인어족` where the source may describe a people
  rather than an explicit plural noun.

## Verification

- `msgfmt --check`: passed
- PO structure audit: markup `0`, placeholder `0`, newline `0`
- Glossary audit: synchronized after the `Saurian Slavers` update

## Next File

Continue automatically with the next PO in order.
