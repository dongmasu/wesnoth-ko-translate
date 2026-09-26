# `wesnoth-manpages-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-manpages-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: PO 원문·manpage 서식·명령줄 문맥·용어집 대조

## 이번 수정

- 실행 파일명 `wesnoth`를 번역하지 않고 원문 그대로 유지
- `Battle for B<Wesnoth>`의 roff 강조 태그를 보존해 `B<웨스노스(Wesnoth)>`로 수정
- 용어집의 `wesnoth` 항목을 명령줄 실행 파일명 문맥에 맞게 원문 유지로 동기화

## 보류

- 옵션명, 파일명, WML 태그, Lua·서버 설정 키는 기술 식별자로 보아 원문을 유지했습니다.
- 긴 manpage 설명문은 의미가 명백히 틀린 항목이 없어 전면 개정하지 않았습니다.
- URL과 명령 예시는 변경하지 않았습니다.

## 검증

- `msgfmt --check --check-format`: 통과
- `tests.test_po_layout`: 30개 통과
- 구조 감사: `markup_mismatches=0`, `placeholder_mismatches=0`, `newline_mismatches=0`
- 용어집 감사: `errors=0`, `warnings=0`
