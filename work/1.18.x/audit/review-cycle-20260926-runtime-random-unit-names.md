# 2026-09-26 런타임 랜덤 유닛 이름 확인

## 관찰

게임에서 상대 유닛 이름으로 `Losel`이 표시되었지만, 한국어 PO에는
`msgid "Losel"` 항목이 없다.

## 확인 결과

- 작업 PO와 설치된 1.18.8 앱의 번역 데이터에서 `Losel` 독립 항목을
  찾을 수 없다.
- 핵심 이름 데이터는 `data/core/macros/names.cfg`의 쉼표 구분 이름 목록과
  context-free grammar 규칙으로 구성된다.
- World Conquest 등 일부 콘텐츠는 `random_names.lua`의 런타임 이름
  목록을 사용한다.
- 따라서 `Losel`은 PO에 없는 이름 누락이라기보다 이름 생성기가 실행 중
  조합하거나 선택한 결과로 판단한다.

## 결정

이름 생성기 문법·토큰·랜덤 이름 목록은 번역하지 않고 원문을 유지한다.
`Losel` 자체를 PO에 추가하거나 `로셀(Losel)`로 치환하지 않는다. 생성
문법을 번역하면 랜덤 이름 생성 결과와 문법 호환성을 손상할 수 있다.

## 규칙 반영

- `work/1.18.x/TRANSLATION-RULES.md`
- `work/README.md`
- `docs/templates/work-README.md.in`
