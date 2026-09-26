# Review Cycle 2026-09-26: `wesnoth-manual-ko.po`

## Scope

- Target: `work/1.18.x/ko/wesnoth-manual-ko.po`
- Policy: high-confidence corrections applied without approval
- Review focus: English source comparison, long-form descriptions, terminology,
  plural forms, spacing, and sentence-level errors

## Changes

- Preserved and rechecked the existing `워즈(Wose)` and `워즈들(Woses)`
  terminology.
- Kept `회복` for `heal/healing` and `치료` for `cure/cures`, correcting the
  affected ability and healing explanations.
- Corrected the `Heals +4/+8` descriptions so the subject correctly restores
  adjacent allied units.
- Normalized healing amounts such as `체력(HP) 4점`, `체력 8점`, and removed
  awkward `체력 +8` prose in explanatory sentences.
- Replaced remaining race-plural `오크족` forms with `오크들` and aligned nearby
  `엘프들` references.
- Rechecked previously corrected proper-name pairings and long manual passages.

## Deferred

- No high-confidence issue was intentionally deferred in this pass.
- Broad stylistic choices such as globally replacing every `당신` or
  `플레이` remain for cross-file consistency review, not speculative editing
  of this file.

## Verification

- `msgfmt --check --check-format`: passed
- PO structure audit: `markup_mismatches=0`,
  `placeholder_mismatches=0`, `newline_mismatches=0`
- Glossary audit: `errors=0`, `warnings=0`
- Targeted layout and glossary tests: 137 passed
- `git diff --check` for the target PO: passed
