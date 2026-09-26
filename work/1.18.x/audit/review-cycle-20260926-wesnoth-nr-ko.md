# `wesnoth-nr-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-nr-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: PO 원문·대사 문맥·띄어쓰기·종족 복수형 대조

## 이번 수정

- 캠페인 소개문과 초반 서술문의 부자연스러운 표현 개선
- Dwarven Doors의 교역 공동체·요새 건설·오크 침공 배경 서술을 원문 정보에 맞게 복원
- 크날가 터널, 숲길잡이, 난쟁이의 문 탈출과 광산 귀환 서술의 주어·행위·인과관계 수정
- 리치 마법사와 요정 공주 구출 과정에서 누락되거나 어긋난 정보와 띄어쓰기 수정
- 탈린 일행의 동맹 협상, 하이델의 죽음, 라크샤스 추적과 에필로그 장문 서술을 전면 대조·수정
- 인명·지명 병기와 `Ro’Arthian`, `Ro’Sothian`, `Angthurim`, `Highbrook Pass` 표기 보완
- `숲속을 달리는 자`처럼 의미를 알기 어려운 표현을 문맥에 맞는 `숲길잡이`로 정리
- 기존의 `선택해야했다`, `끊어진채`, `하기위해`, `부서져있` 등 띄어쓰기와 오탈자 수정
- 재검수에서 남은 고신뢰 오류를 추가 수정: `다른곳/있을수`, `두명의`,
  `하기위해`, `조종 할`, `우리편`, `구조 유출 메모`, 문장 주어·조사 오류
- `Hamel`·`Tallin`·`Morvin`·`Thera` 대화의 명백히 깨진 문장과
  `공주의 우리가 있는는` 오타를 원문 의미에 맞게 복구

## 보류

- 화자별 방언, 말투, 의도적인 비문은 원문의 캐릭터성을 보존하기 위해 유지했습니다.
- obsolete(`#~`) 항목은 활성 번역이 아니므로 수정하지 않았습니다.
- 이번 장문 재검토에서 별도의 용어집 표준값 변경은 필요하지 않았습니다.

## 우선순위 후속 수정

`utils/herodeaths.cfg`에서 의미가 붕괴된 기계 번역과 명백한 오역을
추가로 수정했습니다.

- `You monsters think...`, `You incompetent fools...`,
  `Your efforts to destroy us...`의 적대적 대사를 자연스러운 한국어로
  복원했습니다.
- `life is nothing but a drama`, `be grateful that you are alive`,
  `payback time`의 부부 간 대화를 문맥에 맞게 수정했습니다.
- `hard on the constitution`을 정부의 헌법이 아닌 신체적 부담으로
  해석해 `몸에 좀 무리가 가네요`로 수정했습니다.
- `Your wife just got killed`, `I’ll get you cleaned up good`,
  `give him an incentive to drown himself`, `in my next life`의
  문장 구조와 의미를 복원했습니다.
- `My wanderings have come to an end`, `join my fallen brothers`,
  `Your death shall not go unavenged`의 오역과 서식 태그 불일치를
  수정했습니다.
- `당신` 자체를 일괄 치환하지 않고, 원문 의미가 명백히 확인되는
  항목만 수정했습니다.

## 검증

- `msgfmt --check --check-format`: 통과
- `tests.test_po_layout`: 30개 통과
- 구조 감사: `markup_mismatches=0`, `placeholder_mismatches=0`, `newline_mismatches=0`
- 용어집 감사: `errors=0`, `warnings=0`
