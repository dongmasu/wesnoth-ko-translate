# Review Cycle 2026-09-25: `wesnoth-manpages-ko.po`

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-manpages-ko.po`
- Reviewed the complete man-page translation as one PO file.

## Changes

- Improved the opening description and corrected awkward terminology such as
  `턴제`, `적 지도자`, and `플레이해 보세요`.
- Corrected technical wording and spacing including `I/O`, `와일드카드`,
  `주 버전과 부 버전`, and `다시 불러옵니다`.
- Repaired the malformed translated `withB` expression by using the proper
  `B<-u>` option markup.
- Rewrote unclear descriptions for the new widget toolkit, plugin execution,
  test multiplayer scenarios, and server configuration options.
- Preserved command names, option names, placeholders, and man-page markup.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check`: passed
- Repository PO layout tests: passed, 30 tests

## Deferred

No category was intentionally deferred in this file. Remaining English tokens
are command names, placeholders, markup, or established technical identifiers.
