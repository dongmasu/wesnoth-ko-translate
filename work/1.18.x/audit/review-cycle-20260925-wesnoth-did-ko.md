# Review Cycle 2026-09-25: `wesnoth-did-ko.po`

## Scope

- Role: reviewer, then editor for approved findings
- Target: `work/1.18.x/ko/wesnoth-did-ko.po`
- Order: second PO file in sorted filename order
- Active messages reviewed: 956
- Baseline commit: `81198c4`
- PO changes during this cycle: approved high-confidence fixes only
- Glossary changes during this cycle: none

The file was compared with the current English PO, the 2025-03-22 Korean
reference PO, related active work PO usage, and the glossary. The glossary was
treated as evidence rather than an authority. Differences from the old
reference were not treated as errors by themselves; in particular, the current
file's parenthetical English proper-name notation was preserved.

## Verification Snapshot

- Active untranslated messages: `0`
- Active fuzzy messages: `0`
- `msgfmt --check`: passed
- PO structure audit: no markup, placeholder, or newline mismatches
- Structural edits: none
- Files changed by the review: `work/1.18.x/ko/wesnoth-did-ko.po`
- `msgfmt --check`: passed after editing
- Repository PO layout tests: 30 passed

The completion check does not detect non-empty translations that still contain
semantic errors, so the narrative and objective text was reviewed separately.

## High-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-DID-001 | `wesnoth-did-ko.po:4276` | `Eternity will claim your soul as its own if I do not.` had an incomplete Korean condition. | Fixed to `내가 그렇게 하지 않는다면 영원이 네 영혼을 차지할 것이다.` |
| H-DID-002 | `wesnoth-did-ko.po:1602` | The black-magic passage obscured who was guiding whom. | Rewrote the passage so Malin listens to the magic, receives its response, senses its will, and lets the magic guide him. |
| H-DID-003 | `wesnoth-did-ko.po:3966-3967` | The repeated narrator reward message used raw material `금` instead of the gameplay resource term `금화`. | Fixed to `금화를 발견했습니다!`; all four source references remain covered by the same PO entry. |

## Glossary and Cross-File Evidence

- The glossary has several context-specific `gold` records, including
  `금화` for campaign/resource phrases and `자금` for the generic UI term
  `Gold`. This supports contextual review rather than a repository-wide
  replacement.
- The DID entries `The orc was carrying some gold.` and `The mages have hidden
  their gold somewhere else.` were left unchanged as narrative references to
  gold; they are not automatically converted to the gameplay resource term.
- The global glossary audit still reports the previously known unrelated
  `Smash Cave Floor` mismatch from ANL. It is not a DID finding and was not
  changed in this cycle.

## Medium-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| M-DID-001 | `wesnoth-did-ko.po:152`, `6195-6207` | `Am I the Bad Guy?` is rendered as `내가 나쁜놈이냐?`, and `Maimed` as `불구의`; these may need terminology and spacing review, but they are not unambiguous semantic errors. | Review with the shared UI/trait terminology batch; do not change automatically. |
| M-DID-002 | `wesnoth-did-ko.po:410-413`, `2251` | `도시 벽` and `냉혈하게` are understandable but less natural than likely UI/dialogue alternatives such as `도시 성벽` and `냉혹하게`. | Compare surrounding register and existing project usage before deciding. |
| M-DID-003 | `wesnoth-did-ko.po:137`, `5285` | Some achievement and fourth-wall dialogue wording is awkward, including `제대로 숙성되지 않은 럼주` and `고용된 형편없는 배우`; the meaning is still recoverable. | Defer to a prose/style pass rather than mixing with semantic fixes. |

## Correct Existing Work

The following areas were reviewed and left unchanged:

- proper-name entries with the current `(English name)` notation;
- `Gold` references that describe narrative material rather than a gameplay
  resource;
- the four repeated `You found some gold!` references as one source entry,
  pending approval of the single scoped correction;
- obsolete fuzzy entries at the end of the file, which are not active
  translations.

## Cycle Decision

- High-confidence candidates: 3
- Glossary/context findings: 3
- Medium-confidence candidates: 3
- Active messages changed: 3 entries
- Files changed: 1 PO file and this report
- Test command note: `pytest` was unavailable; the equivalent `unittest` discovery completed successfully
- Next PO: not started automatically

The approved PO edits are complete and validated. The glossary remains
reference evidence and should not be globally reapplied. The medium-confidence
style candidates remain unresolved for a later scoped review.
