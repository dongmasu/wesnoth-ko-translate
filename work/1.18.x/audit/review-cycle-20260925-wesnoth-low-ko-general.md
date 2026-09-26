# Review Cycle 2026-09-25: `wesnoth-low-ko.po` general corrections

## Scope

- Role: approved edit and verification
- Target: `work/1.18.x/ko/wesnoth-low-ko.po`
- This cycle reviewed the file after the race-plural pass.
- Existing unrelated changes were preserved.

## High-confidence changes

- Corrected spacing in fixed expressions such as `피치 못할`, `몇 주`,
  `돌아올 때`, `지원이 올 때`, `무찌를 것`, and `안 돼`.
- Corrected sentence-level spacing such as `행군 능력`, `도착했을 때`,
  `되찾기 위해`, `포위한 것`, `대책 없이`, and `상처 입은`.
- Fixed clear errors including `오크족지` → `오크족이지`,
  `란다르(Landar)가가` → `란다르(Landar)가`, `보이일` → `보일`,
  and `나모` → `워즈(Wose)` according to the name-bilingualization rule.
- Improved the clearly incomplete Grugl sentence while preserving its
  speaker-specific rough tone.

## Verification

- `msgfmt --check --check-format`: passed
- `git diff --check`: passed
- `python3 -m unittest tests.test_po_layout -q`: passed, 30 tests

## Resolution

The previously deferred items in this file were reviewed in context rather
than left as a separate prose-review task:

- Explicit English plural groups were changed to Korean `들`.
- Location names were kept in the bilingual form where the Korean name is a
  transliteration, including the existing `워즈(Wose)` correction.
- Sentence naturalness, spacing, and clear prose errors were corrected.
- Longer narrative paragraphs were reviewed as ordinary PO entries.

Conceptual uses such as `우리 종족` and references to a race as a tradition or
way of life were retained where `들` would change the meaning.
