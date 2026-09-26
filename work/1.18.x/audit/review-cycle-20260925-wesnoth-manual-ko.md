# Review Cycle 2026-09-25: `wesnoth-manual-ko.po`

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-manual-ko.po`
- Reviewed the remaining high-confidence issues in the manual translation.

## Changes

- Applied Korean-English name pairing to `Wose` references:
  `워즈(Wose)` and `워즈들(Woses)`.
- Corrected the malformed `나모들는` sentence and aligned the Wose plural
  forms with the project rule.
- Added missing English pairings for `Aethenwood`, `Dulatus`, and
  `Bay of Pearls` in the reviewed passages.
- Corrected clear sentence and spacing problems, including
  `군대의 강화를 구축`, `강하고/강하거나`, and
  `오래전에는 웨스노스(Wesnoth)는`.
- Repaired one existing `msgid`/`msgstr` mismatch in the strategy section.
- Preserved markup, placeholders, and the original English message IDs.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check`: passed
- Repository PO layout tests: passed, 30 tests

## Deferred

No high-confidence issue identified during this pass was intentionally
deferred. Broader stylistic consistency remains subject to later cross-file
review, without replacing established translations speculatively.
