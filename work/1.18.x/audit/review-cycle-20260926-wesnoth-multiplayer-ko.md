# `wesnoth-multiplayer-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-multiplayer-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: PO 원문·진영명·종족 복수형·고유명사 병기·용어집 대조

## 이번 수정

- `Drakes` 진영명을 `반룡족`에서 `반룡들`로 변경
- 본문 속 `Wesnoth`를 `웨스노스(Wesnoth)`로 병기
- 용어집의 `Drakes` 표준값과 금지 대안을 동기화
- `두명의`를 `두 명의`로 수정
- `시나리오 입니다`를 `시나리오입니다`로 수정

## 보류

- 진영 설명문의 긴 문장은 의미가 명백히 틀린 항목이 없어 유지했습니다.
- `<ref>`, `<bold>`, `<i>` 등 게임 내부 링크·표식은 구조를 보존했습니다.
- 시나리오 제목의 영어 표기는 식별 가능한 콘텐츠명으로 보고 임의 번역하지 않았습니다.

## 검증

- `msgfmt --check --check-format`: 통과
- `tests.test_po_layout`: 30개 통과
- 구조 감사: `markup_mismatches=0`, `placeholder_mismatches=0`, `newline_mismatches=0`
- 용어집 감사: `errors=0`, `warnings=0`
