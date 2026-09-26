# Review Cycle 2026-09-25: `wesnoth-dw-ko.po`

## Scope

- Role: reviewer, then editor for approved findings
- Target: `work/1.18.x/ko/wesnoth-dw-ko.po`
- Order: fourth PO file in sorted filename order
- Active messages reviewed: 464
- Baseline commit: `81198c4`
- Pre-existing dirty change: `Also kill Marg-Tonz` objective currently reads
  `Marg-Tonz도 처치하라`; this was preserved and not treated as a new edit
- PO changes during this cycle: approved scoped fixes
- Glossary changes during this cycle: none

The file was compared with the current English PO, the 2025-03-22 Korean
reference PO, related active work PO usage, and the glossary. The glossary was
treated as evidence rather than an authority. Differences in parenthetical
English proper-name notation were not treated as errors by themselves.

## Verification Snapshot

- Active untranslated messages: `0`
- Active fuzzy messages: `0`
- `msgfmt --check`: passed
- PO structure audit: no markup, placeholder, or newline mismatches
- Structural edits: none
- Files changed by the review: `work/1.18.x/ko/wesnoth-dw-ko.po`
- `msgfmt --check`: passed after editing
- Repository PO layout tests: 30 passed

## High-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-DW-001 | `wesnoth-dw-ko.po:2517-2518` | `Also, I have a little gold I can bring along.` reversed the speaker's first-person offer into an order to the listener. | Fixed to `그리고 내가 가진 금화도 조금 가져갈 수 있소.` |
| H-DW-002 | `wesnoth-dw-ko.po:1553`, `2717-2718` | The name sentence had `먹물이 라고해`, and the later line had `누가가서`. | Fixed the name to `잉키(Inky)라고 해` and the line to `잉키가 뭔가를 찾았다. 누가 가서 확인하라.` |

## Glossary and Cross-File Evidence

- The campaign resource messages already use `금화` for explicit gameplay
  rewards such as `You receive 120 gold`, `100 gold`, and `55 gold`.
- The `Also, I have a little gold...` line is narrative dialogue but still
  clearly describes the speaker's own money; the primary error is the reversed
  grammatical subject, not merely the choice between `금` and `금화`.
- The global glossary audit still reports the previously known unrelated
  `Smash Cave Floor` mismatch and a parenthetical-name warning. Neither is a
  new DW-specific finding.

## Medium-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| M-DW-001 | `wesnoth-dw-ko.po:1591-1592`, `1553`, `2717`, `2869` | `Inky` had mixed `잉키(Inky)` and older `먹물` forms. | Decision applied: retain `잉키(Inky)` and use English parenthetical notation rather than selectively naturalizing only this name. |
| M-DW-002 | `wesnoth-dw-ko.po:892-893` | The trident description contains doubled spaces and an awkward order: `원거리 공격을 하며,  14×2의 ...  마법 피해`. | Review as UI prose; a possible rewrite is `이 삼지창은 마법이 걸린 원거리 무기로, <i>불</i> 피해를 14×2 가합니다.` |
| M-DW-003 | `wesnoth-dw-ko.po:768-769`, `1126-1127`, `2522-2523` | Numeric reward formatting varies between `120 금화를`, `100 금화를`, and `55 금화를`. The resource term is consistent, but spacing and sentence endings vary. | Normalize only as a shared reward-message batch after confirming the project-wide number/unit style. |

## Correct Existing Work

The following areas were reviewed and left unchanged:

- the existing one-line `Marg-Tonz` objective change;
- explicit reward messages using `금화`;
- proper-name parenthetical notation where it is consistent within an
  individual entry;
- the existing `Saurians` translations, which are contextually acceptable;
- obsolete fuzzy entries at the end of the file.

## Cycle Decision

- High-confidence candidates: 2
- Glossary/context findings: 1
- Medium-confidence candidates: 3
- Active messages changed: 4
- Files changed: 1 PO file and this report
- Test command note: `pytest` was unavailable; the equivalent `unittest` discovery completed successfully
- Next PO: not started automatically

The approved DW edits are complete and validated. The `Inky` naming policy is
now applied as `잉키(Inky)` with English parenthetical context. The trident
prose and numeric reward formatting remain unresolved medium-confidence items.
The pre-existing objective change and all other dirty worktree changes remain
untouched.
