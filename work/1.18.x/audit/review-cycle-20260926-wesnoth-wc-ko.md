# `wesnoth-wc-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-wc-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: 세계 정복 UI·게임 규칙 설명·아이템 효과·훈련 효과·대사의
  원문 문맥과 기존 용어집 대조

## 이번 수정

- `Northerners`를 `북부인들`로 수정하고, 명시적 복수형 `Drakes`를
  `반룡들`로 통일했다.
- 사령관 설명의 쉼표 연결 오류와 금화·거점 표현을 수정했다.
- 조기 종료 보너스, 소환 비용, 보너스 포인트 생성 설명의 의미와 문장을
  바로잡았다.
- `Items`를 UI 제목에 맞게 `아이템`으로 수정하고, 진영 설명의
  `파벌/당파` 혼용을 `진영`으로 정리했다.
- `heal/heals`를 `회복`, `cure/cures`를 `치료`로 적용했다.
- `Root of the Elder Wose`와 설명의 `Wose`를 `워즈(Wose)`로 수정했다.
- `full movement`를 `완전 이동`, `melee`를 `근접`, `arcane`을 `비전`으로
  정리했다.
- `fiery power`의 오역인 `불사의 힘`을 `불의 힘`으로 수정했다.

## 유지한 항목

- `Saurian`의 `사우리안` 표기는 이전 사이클의 확정 변경을 유지했다.
- 기존의 고유명사 병기와 변수·마크업 구조는 변경하지 않았다.
- 장문 대사는 의미가 명백히 어긋난 부분만 수정하고, 화자 말투나 단순한
  문체 선호 차이는 유지했다.
- obsolete(`#~`) 항목은 수정하지 않았다.

## 보류 및 이월

- 다른 PO에 남아 있는 독립 `Ogres` 항목의 복수형 표기는 전역 종족 검수
  범위에서 처리한다. 현재 `wc` 파일에는 해당 독립 항목이 없다.
- `Northerners`의 단독 표기와 진영명·음악 제목 문맥의 차이는 용어집
  기존 기준을 유지했다.
- 일부 캠페인 대사의 높임말·구어체 차이는 의미 오류가 아니므로 보류했다.

## 용어집 영향

- 이번 수정은 이미 용어집에 등록된 `Drakes`, `Wose`, `heal`,
  `cure`, `melee`, `arcane`의 표준값을 적용한 것으로, 새 용어 행은
  추가하지 않았다.
- 용어집은 고정 불변 데이터가 아니므로 이후 다른 PO의 실제 문맥에서
  예외가 확인되면 해당 파일과 함께 갱신한다.

## 검증

- `msgfmt --check --check-format`: 통과
- `audit_po_structure.py`: `markup_mismatches=0`,
  `placeholder_mismatches=0`, `newline_mismatches=0`
- `audit_glossary.py`: `errors=0`, `warnings=0`
- 변경 범위의 `git diff --check`: 통과
- 보조 테스트 `tests/test_glossary.py tests/test_po_layout.py`: 전체
  137개 중 14개 실패. 실패는 `Drakes`, `Frozen`, `EI`, `Estmark`,
  기존 고유명사·장문 규칙 및 `wesnoth-units-ko.po`의 전역 잔여 항목으로,
  이번 `wc` 수정과 직접 관련된 실패는 확인되지 않았다.
