# Review Cycle 2026-09-25: `wesnoth-anl-ko.po`

## Scope

- Role: reviewer, then editor for approved findings
- Target: `work/1.18.x/ko/wesnoth-anl-ko.po`
- Order: first PO file in sorted filename order
- Active messages reviewed: 124
- Baseline commit: `81198c4`
- PO changes during this cycle: approved high-confidence fixes only
- Glossary changes during this cycle: none

The file was compared with the current English PO, the 2025-03-22 Korean
reference PO, related active work PO usage, and the glossary. The glossary was
treated as evidence rather than an authority.

## Verification Snapshot

- Active untranslated messages: `0`
- Active fuzzy messages: `0`
- `msgfmt --check`: passed
- Structural edits: none
- Files changed by the review: `work/1.18.x/ko/wesnoth-anl-ko.po`
- Repository PO layout tests: 30 passed

The completion check does not detect non-empty translations that still contain
English source text, so semantic review was still required.

## High-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-ANL-001 | `wesnoth-anl-ko.po:568-574` | The translated research status message left `Our farms produce ...` and `Our mines produce ...` in English. | Fixed the two residual lines as Korean text, preserving both placeholders, the `g`-derived values, and the real newlines. |
| H-ANL-002 | `wesnoth-anl-ko.po:787-788` | `Smash Cave Floor` was translated as `동굴 벽을 부순다`, changing “floor” to “wall”. | Fixed to `동굴 바닥을 부순다`. |
| H-ANL-003 | `wesnoth-anl-ko.po:338-339`, `410-415`, `583-646`, `685-818` | Wesnoth `gold` was repeatedly translated as the real-world currency `원` across donations, production, income, and costs. This affected 18 active entries. | Fixed the affected active entries to use the in-game currency term `금화`. |

## Glossary Conflicts

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| G-ANL-001 | `glossary.tsv:3242` and `wesnoth-anl-ko.po:787-788` | The glossary also records `Smash Cave Floor` as `동굴 벽을 부순다`, confirming that the glossary propagated the same source-level semantic error. | Correct the PO and glossary as separate approved changes; do not run a repository-wide glossary reapplication. |
| G-ANL-002 | `glossary.tsv:4887` and `wesnoth-anl-ko.po:99-100` | The glossary has `teamname^Monsters` with `forbidden_terms=레지스탕스`, while the current PO correctly uses `괴물들`. The old Korean reference PO incorrectly used `레지스탕스` for several distinct team names. | Remove or revise the stale forbidden-term record after confirming all active usages. Do not change the current PO entry. |

## Medium-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| M-ANL-001 | `wesnoth-anl-ko.po:252`, `406`, `519`, `696`, `706` | `초지 뿐`, `아무것도 안한다`, `실마리들`, and `마을/성채 건축` are spacing or UI-naturalness issues. | Review as a small Korean UI style batch; do not mix with the high-confidence semantic fixes automatically. |
| M-ANL-002 | `wesnoth-anl-ko.po:477`, `484` | `우리의 대화는 끝났소` is a literal rendering of completed negotiations and sounds unnatural in context. | Compare the surrounding diplomacy messages and decide whether `협상이 끝났소` better preserves the scene. |
| M-ANL-003 | `wesnoth-anl-ko.po:361`, `420`, `477-484` | Register varies between formal polite UI text and archaic/plain dialogue. Some variation is appropriate by speaker, but these lines should be checked together if the file is edited. | Keep as a style review item; no automatic normalization. |

## Correct Existing Work

The following areas were reviewed and left unchanged:

- `teamname^Settlers` → `정착민`
- `teamname^Enemies` → `적`
- `teamname^Prisoners` → `포로`
- `teamname^Monsters` → `괴물들`
- proper names `Mal Sevu`, `Gol Goroth`, `Greg`, and `Mal Shiki`
- the active objective text `In this scenario you build up an economy`
- placeholders, tags, and real newlines in the reviewed messages

These entries demonstrate that the current PO can be better than the older
Korean reference. The reference value must not be copied back over the current
translation without new evidence.

## Cycle Decision

- High-confidence candidates: 3
- Glossary conflicts requiring separate review: 2
- Medium-confidence candidates: 3
- Active messages changed: 20 total (18 currency entries, 1 research-status entry, and 1 cave-floor entry)
- Files changed: 1 PO file and this report
- Test command note: `pytest` was unavailable; the equivalent `unittest` discovery completed successfully
- Next PO: not started automatically

The approved PO edits are complete and validated. The glossary conflicts remain
separate follow-up items and were not changed. The currency issue and glossary
conflicts should continue to be handled as explicitly scoped changes, not by
running a global normalization tool.
