# Review Cycle 2026-09-25: `wesnoth-wof-ko.po`

## Scope

- Role: follow-up reviewer and editor
- Target: `work/1.18.x/ko/wesnoth-wof-ko.po`
- Reason: shared glossary update for the Wose naming rule

## Changes

- Updated the active `Woses` faction label to `워즈들(Woses)`.
- Updated the active long title containing `Woses` to
  `워즈들(Woses)`.
- Corrected the active objective wording `18 차례` and `24 차례` to
  `18차례` and `24차례`.
- No unrelated campaign dialogue was changed.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check` for the PO: passed

## Deferred and Follow-up

No active Wose-related issue remains in this file.
