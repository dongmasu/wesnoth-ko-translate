# Review Cycle 2026-09-25: `wesnoth-dm-ko.po`

## Scope

- Role: reviewer, then editor for approved findings
- Target: `work/1.18.x/ko/wesnoth-dm-ko.po`
- Order: third PO file in sorted filename order
- Active messages reviewed: 731
- Baseline commit: `81198c4`
- Pre-existing dirty files: preserved; no unrelated file was changed
- PO changes during this cycle: approved scoped fixes
- Glossary changes during this cycle: none

The file was compared with the current English PO, the 2025-03-22 Korean
reference PO, related active work PO usage, and the glossary. The glossary was
treated as evidence rather than an authority. Parenthetical English proper-name
notation in the current work file was treated as an intentional current
convention, not as a defect.

## Verification Snapshot

- Active untranslated messages: `0`
- Active fuzzy messages: `0`
- `msgfmt --check`: passed
- PO structure audit: no markup, placeholder, or newline mismatches
- Structural edits: none
- Files changed by the review: `work/1.18.x/ko/wesnoth-dm-ko.po`
- `msgfmt --check`: passed after editing
- Repository PO layout tests: 30 passed

The completion check does not detect semantic errors in non-empty translations,
so the dialogue, narrative, objective, and resource terminology were reviewed
separately.

## High-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-DM-001 | `wesnoth-dm-ko.po:1005-1006` | The gameplay payment `$fee gold` was translated as `$fee 원`, repeating the real-world currency issue found in ANL. | Fixed to `$fee 금화`, preserving the `$fee` placeholder. |
| H-DM-002 | `wesnoth-dm-ko.po:1127-1128` | `Nope, I’m not giving you any more gold.` omitted the explicit gold object. | Fixed to `아니, 더 이상 금화는 주지 않겠소.` |
| H-DM-003 | `wesnoth-dm-ko.po:398-400`, `4926` | `the great Academy on Alduin` was translated as `대학원` in two active narrative entries. | Fixed both entries to `알두인(Alduin)의 마법 학원` / `알두인(Alduin)의 마법 학원을 재건하여`. |
| H-DM-004 | `wesnoth-dm-ko.po:1913` | `그들의 원하든 원하지 않든` was grammatically malformed. | Fixed to `그들이 원하든 원하지 않든`. |

## Glossary and Cross-File Evidence

- The glossary distinguishes contextual `gold` records, including `금화` for
  campaign/resource phrases and `자금` for generic UI `Gold`. This supports
  scoped contextual corrections, not a global replacement.
- The existing `금화` translations in nearby Delfador's Memoirs dialogue
  support applying the ANL/DID resource precedent to H-DM-001 and H-DM-002.
- A post-file glossary review found that active Wose references still used the
  superseded `나모` wording. Those entries were rechecked against the English
  source and changed to `워즈(Wose)` or `워즈들(Woses)` as appropriate.

## Medium-Confidence Candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| M-DM-001 | `wesnoth-dm-ko.po:1112-1113` | `금화 20 개` had a spacing issue. | Fixed to `금화 20개`. |
| M-DM-002 | `wesnoth-dm-ko.po:1070` | `거래끝이다; 너가` had spacing, punctuation, and particle/register issues. | Fixed to `거래 끝이다. 네가 ...`. Other style candidates from the broader file remain unresolved. |
| M-DM-003 | `wesnoth-dm-ko.po:1009-1011` | `Here’s the gold...` is rendered as `여기 돈이 있소...`; this may be acceptable conversational Korean, but could be aligned with `금화` if the scene requires explicit resource terminology. | Leave unchanged unless the surrounding payment UI establishes a strict term requirement. |
| M-DM-004 | `wesnoth-dm-ko.po:2159` | The line contained the typo `안드는네요` and the spacing error `둘다`. The intended meaning is that Delfador does not feel he has received such a great destiny. | Fixed the sentence to use `난 그렇게 엄청난 운명을 받았다는 느낌이 들지 않는군요. ... 둘 다 실패했어요.` |

## Correct Existing Work

The following areas were reviewed and left unchanged:

- active proper-name entries using the current `(English name)` convention;
- narrative `gold` references where `금` or `돈` can refer to physical money
  rather than the gameplay resource;
- the existing `금화` translations in the same swamp payment scene;
- obsolete fuzzy entries at the end of the file.

## Cycle Decision

- High-confidence candidates: 4
- Glossary/context findings: 3
- Medium-confidence candidates: 4
- Active messages changed: 8 entries
- Files changed: 1 PO file and this report
- Follow-up changes after glossary review: 4 active entries
- Test command note: `pytest` was unavailable; the equivalent `unittest` discovery completed successfully
- Next PO: not started automatically

The approved DM edits and the Wose follow-up are complete and validated.
`M-DM-003` (`여기 돈이 있소...`) remains unchanged because its conversational
wording is acceptable without stronger evidence. Obsolete `#~` entries were
not rewritten. Other affected PO files remain queued for the same follow-up
review and were not mass-edited.
