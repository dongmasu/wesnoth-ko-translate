# 2026-09-26 전체 PO 승인 항목 반영 리포트

## 적용 범위

`review-cycle-20260926-global-approval.md`에서 승인된 항목만 활성
`work/1.18.x/ko/*.po`에 반영했다.

- `엘프족` → `엘프들`
- `난쟁이족` → `난쟁이들`
- `드워프들` → `난쟁이들`
- Wose 잔여 오역 → `워즈(Wose)` 또는 `워즈들(Woses)`
- 게임 규칙 문맥의 `heal/healing/healer` → `회복/회복사`
- 게임 규칙 문맥의 `cure/curer/Cures` → `치료/치료사`
- 서사적 `치유`와 `healing senses`, `healing art`는 보존

단순 문자열 치환으로 처리하지 않고 원문 `msgid`, PO 참조 문맥,
단수·복수에 따라 적용했다. 비활성(`#~`) 항목은 수정하지 않았다.

## 용어집 반영

다음 표준값을 `work/1.18.x/glossary.tsv`에 동기화했다.

- `Cures` → `치료`
- `Dealing with Dwarves` → `난쟁이들과의 거래`
- `Meeting With Dwarves` → `난쟁이들과 만남`
- `a fully-healed Dust Devil` → `완전히 회복된 먼지 악마`
- `female^heals Kalenz +4` → `칼렌츠(Kalenz) 회복효과 +4`

기존 Wose, Saurian, Wyrm 예외와 병기 규칙은 유지했다.

## 검증 결과

```text
전체 메시지: 21,303
활성 미번역: 0
활성 fuzzy: 0
markup_mismatches: 0
placeholder_mismatches: 0
newline_mismatches: 0
용어집: rows=5034, errors=0, warnings=0
msgfmt --check: 성공
전체 테스트: 142개 성공
```

활성 PO에서 승인 대상의 구 표기 잔여 검색 결과는 0건이다. 검색에
남은 `나모`, `드워프들`, `엘프족`, `난쟁이족`은 모두 비활성(`#~`)
과거 항목이며, 현재 게임 메시지에는 사용되지 않는다.

## 남은 작업과 위험

- MO 생성·설치·플레이테스트·배포·tag는 수행하지 않았다.
- `Quit to Menu`와 `Quit to Desktop`의 실제 UI 동작 확인은 계속 보류한다.
- `pytest` 명령과 `python3 -m pytest`는 환경에 패키지가 없어 실행하지
  못했지만, 저장소 공식 방식인 `unittest` 142개는 모두 성공했다.
- 장문 전체 재작성이나 서사적 `치유`의 추가 통일은 이번 승인 범위에
  포함하지 않았다.

