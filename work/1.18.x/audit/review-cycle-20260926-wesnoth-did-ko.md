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

## 장문 대화 후속 검수

- 다켄 볼크가 제자와 마을 사람들에게 말하는 장면에서 관계에 맞지 않는
  기계적인 `당신`을 `자네`로 조정했다.
- `네 마법이 우리보다 더 중요하다고 결정했어`, `오크들은 언덕에서
  강력하며`, `냉혈하게 살해`처럼 직역으로 어색해진 대사를 자연스럽게
  고쳤다.
- 다켄 볼크의 견습생 훈련 지시문을 스승의 말투에 맞게 정리하고,
  `추방을 심각하게 받아들이지`, `말해 주겠다` 등의 표현을 다듬었다.
- 말린의 장문 독백에서 `이 모든 시간과 ... 후에`의 부자연스러운 구조를
  원문 의미에 맞는 자연스러운 서술로 수정했다.

## Next File

If no new medium-confidence decision is required, continue with
`wesnoth-dm-ko.po`.
