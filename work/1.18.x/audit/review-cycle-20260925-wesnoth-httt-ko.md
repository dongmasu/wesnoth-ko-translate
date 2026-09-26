# Review Cycle 2026-09-25: `wesnoth-httt-ko.po`

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-httt-ko.po`
- Reviewed the complete campaign PO file for high-confidence translation
  errors and consistency with the established project rules.

## Changes

- Applied Korean-English pairing to Wose references:
  `워즈(Wose)`.
- Replaced remaining `우즈`, `요정`, and clear `족`-based plural forms with
  context-appropriate `워즈`, `엘프들`, `오크들`, and `난쟁이들`.
- Corrected `Elensefar` name corruption and preserved the English pairing.
- Improved clear spacing and grammar issues such as `여기뿐`, `끝날 때`,
  `다시 보니`, `하는 건`, and `숨 쉬`.
- Preserved dialogue intent, markup, variables, and campaign identifiers.
- Rechecked the Wose-related follow-up after the file pass:
  `Sir Wose` is a title/address for a Wose, not a personal name. The actual
  character name in this scene is `Haralamdum`.
- Updated the shared glossary for `Sir Wose`, `Ancient Wose`, and `Elder Wose`
  so the previous `나모` entries no longer conflict with the current Wose rule.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check`: passed
- Repository PO layout tests: passed, 30 tests

## Deferred and Follow-up

The Wose title ambiguity was initially carried as a follow-up question and was
resolved during the post-file review. No high-confidence issue remains
intentionally deferred in this file. Broader dialogue-style normalization
remains outside this edit pass unless an English mismatch or clear Korean error
is found.
