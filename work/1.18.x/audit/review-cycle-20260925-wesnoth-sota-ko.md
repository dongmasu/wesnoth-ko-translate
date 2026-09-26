# Review Cycle 2026-09-25: `wesnoth-sota-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-sota-ko.po`
- Reason: shared glossary update for the Wose naming rule

## Changes

- Replaced the active `나모` rendering in `Walking Corpse (Wose)` with
  `워즈(Wose)`.
- Replaced the active plural `wose corpses` rendering with
  `워즈들(Woses)의 시체`.
- No other entries were changed.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check`: passed
- No obsolete entries were rewritten.

## Deferred and Follow-up

No active Wose-related issue remains in this file. Other PO files with
superseded Wose spellings remain queued for sequential follow-up review.
