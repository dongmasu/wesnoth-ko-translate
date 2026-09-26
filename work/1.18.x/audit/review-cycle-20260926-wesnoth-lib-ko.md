# `wesnoth-lib-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-lib-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: PO 원문·지형 문맥·기존 용어 대조

## 이번 수정

- `Overgrown Cobbles` → `풀이 무성한 자갈길`
- `Flowering Water Lilies` → `피어 있는 연꽃`
- `Dry Impassable Mountains` → `건조한 통과 불가 산맥`
- `Snowy ...` 지형명 5건의 `눈덮인` → `눈 덮인`

`Impassable Overlay=통과 불가 오버레이`와 `Unwalkable Overlay=통과 불능 오버레이`는 원문이 서로 달라 구분을 유지했습니다.

## 보류

- 지형 설명문의 긴 문장 전체는 의미가 명백히 어긋난 경우가 아니어서 유지했습니다.
- `heal=회복`, `cure=치료` 문맥은 기존 번역이 규칙과 충돌하지 않아 변경하지 않았습니다.
- 용어집 변경은 필요하지 않았습니다.

## 검증

- `msgfmt --check --check-format`: 통과
- `tests.test_po_layout`: 30개 통과
