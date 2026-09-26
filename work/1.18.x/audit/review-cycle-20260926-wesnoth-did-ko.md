# Review Cycle 2026-09-26: `wesnoth-did-ko.po` prose follow-up

## Scope

- Target: `work/1.18.x/ko/wesnoth-did-ko.po`
- Method: English source and surrounding narrative context, current glossary,
  existing Korean usage, and structural comparison
- Obsolete(`#~`) entries were not edited
- High-confidence semantic, spelling, spacing, and name-pairing errors were
  fixed without a separate approval step

## High-Confidence Fixes

| ID | Area | Change |
| --- | --- | --- |
| H-DID-P-001 | Magic terminology | Changed `scrying` from `수정점` to `투시술`; registered the contextual term in the glossary. |
| H-DID-P-002 | Narrative prose | Removed the stray backtick in the battle description and corrected the subject of the skeletons' fetid magic and empty eyes. |
| H-DID-P-003 | Narrative prose | Reworked the Alduin passage so Malin's preference for practical magic and his expulsion are expressed naturally without changing the meaning. |
| H-DID-P-004 | Spacing | Fixed `제자... 로` to `제자...로`. |
| H-DID-P-005 | Ghoul description | Restored the meaning that ghouls are fashioned from living flesh into corpses filled with disease and poison, and that surviving ghouls are drawn to natural decay. |
| H-DID-P-006 | Seasonal narration | Corrected the summer-and-fall travel passage to natural Korean narrative prose. |
| H-DID-P-007 | Whitefang names | Replaced the malformed semantic rendering `하얀(Whitefang) 송곳니` with `화이트팽(Whitefang)` across the active DID usages, keeping generic nouns such as `산맥`, `영토`, `족장`, and `오크들` outside the parentheses. |
| H-DID-P-008 | Proper-name typo | Fixed `다큰 볼크` to `다켄 볼크(Darken Volk)` in the unit description and improved the sentence flow. |

The exact `Clan Whitefang` glossary value was also synchronized in
`wesnoth-ei-ko.po` and in the name-translation override table because the
same source term is shared across active files.

## Deferred

- `Am I the Bad Guy?`: wording preference, not an unambiguous semantic error.
- `Maimed`: trait terminology requires a shared UI review.
- `도시 벽` versus `도시 성벽`: understandable and context-dependent.
- Other fourth-wall and achievement prose whose meaning remains recoverable.

## Verification

- `msgfmt --check`: passed
- PO structure audit: markup `0`, placeholder `0`, newline `0`
- Full unittest discovery: one pre-existing glossary mismatch for `Nothing`
  remains; the DID and Whitefang-related tests pass after synchronization.
- Glossary audit: the remaining `Nothing` mismatch is unrelated to this cycle.

## Next File

If no new medium-confidence decision is required, continue with
`wesnoth-dm-ko.po`.
