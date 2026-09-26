# Review Cycle 2026-09-25: `wesnoth-help-ko.po`

## Scope

- Role: reviewer only
- Target: `work/1.18.x/ko/wesnoth-help-ko.po`
- Existing bounded review: first 20 active entries were covered by
  `review-cycle-20260925-help-first20.md` and are not repeated here.
- This cycle reviewed the remaining active help entries for meaning,
  grammar, spacing, markup/placeholder preservation, and terminology.
- No PO entry or glossary entry was changed in this cycle.

## Verification

- Active untranslated entries: none
- Active fuzzy entries: none
- `msgfmt --check --check-format`: passed
- No placeholder or markup changes were made.

## High-confidence candidates

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-001 | `wesnoth-help-ko.po:34` | The same sentence translates `arcane` as `신령 유형` and `신비 유형`. The glossary and the repeated damage-type entries use `신령`. | Change only `신비 유형` to `신령 유형`. |
| H-002 | `wesnoth-help-ko.po:2236` | `유지 비용또한` has a clear spacing error. The sentence also uses the established `유지비` term in the linked label. | Change to `유지비 또한`. |
| H-003 | `wesnoth-help-ko.po:2373` | An internal translator note, `변역확인: ...`, remains in an active user-visible translation. | Remove only the translator note after confirming the visible sentence remains correct. |
| H-004 | `wesnoth-help-ko.po:2422` | Multiple clear spacing errors: `3 까지`, `그런것`, `4 레벨`, `모았을때`, and `중첩될때`. | Correct to `3까지`, `그런 것은`, `4레벨`, `모았을 때`, and `중첩될 때`. |
| H-005 | `wesnoth-help-ko.po:2536` | Clear spacing errors in `범위입니다.(...)`, `없습니다.(...)`, `않는 한(...)`, and `종료될때까지`. | Add the required spaces after sentence punctuation and before/after the dependent expressions. |
| H-006 | `wesnoth-help-ko.po:2865` | `유닛들간` and `타격회수` are respectively a spacing error and an incorrect word. | Change to `유닛들 간` and `타격 횟수`. |
| H-007 | `wesnoth-help-ko.po:2935` | `2 가지` and `공격시에` have clear spacing errors. | Change to `2가지` and `공격 시에`. |
| H-008 | `wesnoth-help-ko.po:3018` | Both occurrences of `3 가지` have a clear spacing error. | Change both to `3가지`. |
| H-009 | `wesnoth-help-ko.po:3417` | `마을,재생` lacks a space after the comma. | Change to `마을, 재생`. |
| H-010 | `wesnoth-help-ko.po:3458` | `기본설명` should be spaced as `기본 설명`. | Change only that phrase. |
| H-011 | `wesnoth-help-ko.po:5240` | `재소집시에는` has a clear spacing error. | Change to `재소집 시에는`. |
| H-012 | `wesnoth-help-ko.po:5248` | `끝날때마다` and `유지비용` are awkward/incorrect in this established terminology context. | Change to `끝날 때마다` and `유지비`. |
| H-013 | `wesnoth-help-ko.po:5788` | `타격횟수` lacks spacing, and `상처를 입어갈때마다` is an unnatural rendering of “when the unit is wounded”. | Change to `타격 횟수` and `상처를 입을 때마다`. |

## Medium-confidence candidates held

| ID | Location | Finding | Decision |
| --- | --- | --- | --- |
| M-001 | `wesnoth-help-ko.po:114-219`, `3297-3437`, and related entries | `heals`, `healing`, `healer`, and `cures` alternate between `치료`, `치유`, `치료사`, and `치유사`. | Do not edit in this file cycle. Decide the project-wide healing terminology first, then review all related PO files together. |
| M-002 | `wesnoth-help-ko.po:145`, `4963`, `4968` | `basic healing` and related ability descriptions use `치료`/`치유` inconsistently, but the current wording is semantically understandable and matches older reference material in places. | Hold for the terminology review; no blanket normalization. |
| M-003 | `wesnoth-help-ko.po:242`, `301`, and glossary | `Always rest heals` and `Frozen` are already translated, but their display context differs between trait/terrain strings. | Preserve for now; verify against the corresponding UI contexts when the related files are reviewed. |
| M-004 | Long narrative entries around `5998-7041` | Several passages contain awkward or mixed-register wording, including isolated English residue, but correcting them requires sentence-level comparison with the source and should not be automated. | Defer to a dedicated narrative pass rather than making broad edits in this cycle. |

## Accepted without change

- No active untranslated or fuzzy entries were found.
- Existing markup, reference links, and line breaks were preserved.
- `Frozen = 동결` was not changed here: this file contains the World Conquest
  terrain-name string, while the editor-context decision `얼음 타일` belongs
  to the editor file already reviewed.
- `Always rest heals = 항상 휴식 회복` was not changed because it is a
  trait label and no high-confidence defect was established.
- Healing terminology was not normalized because doing so would repeat the
  cross-file rewrite risk this workflow is intended to prevent.

## Cycle decision

- High-confidence candidates: 13
- Medium-confidence candidates: 4
- Entries changed: 13
- Files changed: 2 (the PO file and this audit report)
- `msgfmt --check --check-format`: passed after edits
- PO layout test suite: 30 tests passed via
  `python3 -m unittest discover -s tests -p 'test_po_layout.py'`
- `git diff --check`: passed
- Full test suite: 5 existing glossary failures remain, involving `Ford of
  Alyas`, `Ford of Tifranur`, `Smash Cave Floor`, `EI`, and `Estmark Hills`;
  none involve this PO file's changes.
- Next step: review the resulting diff before moving to the next PO file.

## Narrative Review Addendum

The long race and world-description entries were reviewed instead of being
deferred to an undefined later pass. The following high-confidence candidates
were found. No PO text was changed for these items yet.

| ID | Location | Finding | Proposed action |
| --- | --- | --- | --- |
| H-014 | `wesnoth-help-ko.po:5998` | The English word `trespass` remains in an otherwise Korean sentence. | Translate it as `침범하다`, producing `침범하거나 다른 주요 종족이 이미 점유한 지역에 들어가는 일은`. |
| H-015 | `wesnoth-help-ko.po:6003` | The `Morogor` reference has an extra apostrophe in `dst='morogor''`, unlike the source and other entries. | Remove the extra apostrophe and preserve the existing target text. |
| H-016 | `wesnoth-help-ko.po:6003` | The established race name `반룡` switches to `드레이크` in `드레이크의 식민지`. | Change to `반룡의 식민지`. |
| H-017 | `wesnoth-help-ko.po:6451` | `모래를 헤쳐나(Naga)는` is a proper-name pairing contamination error. The source sentence contains no `Naga`; the valid `나가(Naga)` occurrence belongs to the following sentence about neighboring Naga tribes. | Remove the misplaced pairing and change to `모래를 헤쳐 나가는`. |
| H-018 | `wesnoth-help-ko.po:6367` | `많은 다양한 인간들 집단` and `대륙의 대부분은 ... 살고` do not express the source’s subject correctly. | Rewrite the sentence as `다양한 인간 집단이 존재하지만, 대륙에 사는 인간의 대부분은 ...`. |
| H-019 | `wesnoth-help-ko.po:7057-7063` | The same race was labeled `나모` but described four times as `워즈`; the user decided to use the English-paired form consistently. | Use `워즈(Wose)` consistently in the labels and body. |
| H-020 | `wesnoth-help-ko.po:7057` | `the woses share a connection to the woodlands deeper than even the elves’` is mistranslated as a comparison with fairies. | Change to `나모는 엘프보다도 숲과 더 깊은 연결을 공유합니다`. |
| H-021 | `wesnoth-help-ko.po:6773` | `상호 적이 그들의 존재를 위협하거나 ...` is grammatically incomplete and obscures the “mutual enemy” condition. | Rewrite the clause to `공동의 적이 그들의 존재를 위협하거나 막대한 약탈의 기회가 서로 간의 적대감을 압도하는 경우를 제외하면`. |

## Terminology Decisions To Apply With PO Edits

- `heal`, `heals`, and `healing` use `회복` for HP recovery.
- `cure`, `cures`, `curing`, and `cured` use `치료` or `치료됨` for poison
  and status-effect removal.
- `Frozen` terrain will use `얼음 지형` in terrain/help contexts.
- The editor group `frozen` remains `얼음 타일`, because it labels an editor
  palette group rather than the terrain itself.
- `Always rest heals` will use `상시 휴식 회복`. The `healthy` trait means the
  unit receives the 2 HP rest-healing effect every turn even if it fought on
  the previous turn; it does not mean the unit must refrain from acting.
- The corresponding glossary rows were updated together with the approved PO
  changes, because the glossary is a reference and must follow actual context
  rather than override it.
- `Wose` follows the user-approved pairing form `워즈(Wose)`; the plural
  label is `워즈들(Woses)`.

### Addendum Decision

- Additional high-confidence candidates: 8
- Additional narrative entries changed: 6
- Additional terminology/help entries changed: 5
- Additional entries changed: 11
- Scope: active race and world-description entries in this PO
- `msgfmt --check --check-format`: passed after the addendum edits
- PO layout test suite: 30 tests passed via
  `python3 -m unittest discover -s tests -p 'test_po_layout.py'`
- `git diff --check`: passed
- The glossary now records the `heal`/`cure` distinction, and the direct
  ability labels in this PO were updated accordingly. Longer explanatory
  sentences remain queued for sentence-level review rather than blanket
  replacement.
- The help PO is ready for final review before moving to the next PO file.
