# 2026-09-26 Actions UI 라벨 확인

## 결정

- 원문 `Actions`에 `Menu`가 없으면 `행동`으로 번역한다.
- 원문 `Actions button`은 `행동 버튼`으로 번역한다.
- 원문에 메뉴가 명시된 문맥의 `행동 메뉴`는 이 규칙의 대상이 아니다.

## 적용

- `wesnoth-ko.po`: `data/themes/default.cfg:116`
- `wesnoth-lib-ko.po`: `data/gui/window/formula_debugger.cfg:94`
- `wesnoth-manual-ko.po`: `doc/manual/manual.en.xml:416`

## 전수 확인

활성 PO 전체에서 직접 원문이 `Actions` 또는 `Actions button`인 항목은
위 세 항목 외에 확인되지 않았다. `Action`, `Execute Action`,
`Action Bonus`, `military action` 등은 별도 문맥이므로 일괄 치환하지
않았다.
