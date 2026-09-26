# Review Cycle 2026-09-25: `wesnoth-help-ko.po` First 20 Active Entries

## Scope

- Role: reviewer only
- Target: `work/1.18.x/ko/wesnoth-help-ko.po`
- Range: first 20 active entries after the PO header
- Baseline commit: `81198c4`
- Baseline worktree: dirty only because of the role/workflow documentation
  changes; no PO or glossary changes were present
- Translation and glossary files changed by this cycle: none

The first 20 entries cover damage type, plague, steadfast, illumination, and
healing ability labels and descriptions. Existing Korean reference PO files,
the current glossary, related occurrences in the work PO files, and the
English/Japanese/Chinese locale entries were compared.

## Results

| ID | Confidence | Entry | Finding | Proposed action |
| --- | --- | --- | --- | --- |
| H-001 | high | `This attack combines the arcane type ...` (`wesnoth-help-ko.po:34`) | The same sentence uses `신령 유형` for the first `arcane` occurrence and `신비 유형` for the second. The glossary and repeated damage-type entries use `arcane = 신령`. | Replace only `신비 유형` with `신령 유형` after approval. |
| M-001 | medium | Healing entries at `wesnoth-help-ko.po:133-136`, `172-173`, `208-209` | The same `heals` ability family alternates between `치료`, `치료사`, and `치유사`. The glossary records `heals = 치유` and `치료` as a former alternative, but the older reference PO also uses mixed wording. | Do not edit in this cycle. Decide the project-wide `healing`/`healer`/`cure` policy first, then review all related entries together. |
| M-002 | medium | `This unit is capable of basic healing and slowing dehydration.` (`wesnoth-help-ko.po:145`) | `basic healing` is translated as `기본적인 치료`, while related active entries and the glossary favor `치유` for the `heals` ability family. The reference PO has the same wording, so this is a consistency question rather than a confirmed error. | Do not edit in this cycle. Include in the healing terminology review if that review is approved. |

## Accepted Without Change

The following 17 entries had no high-confidence defect in this bounded pass:

- `arcane`
- `This unit can use the arcane type ...`
- `Underground`
- `undead`
- `fearless`
- `plague`
- `When a unit is killed by a Plague attack ...`
- `steadfast`
- `female^steadfast`
- `female^illuminates`
- `heals +4`
- `female^heals +4`
- `heals +8`
- `female^heals +8`
- `heals +12`
- `female^heals +12`
- the structural treatment of the healing descriptions, including their
  preserved paragraph breaks and placeholders (none are present in this
  range)

The plague description and the healing descriptions match the available
2025-03-22 Korean reference closely. The `female^` entries correctly omit the
gettext context prefix from the Korean display text.

## Cycle Decision

- High-confidence candidates: 1
- Medium-confidence candidates: 2
- Low-confidence candidates: 0
- Entries changed: 0
- Files changed: 0
- Next cycle: not started automatically

The only candidate suitable for an editor handoff is H-001. M-001 and M-002
are intentionally held because changing them requires a broader terminology
decision and could cause the type of cross-file rewrite this workflow is meant
to prevent.
