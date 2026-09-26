# Review Cycle 2026-09-26: 의미역 가능한 고유 지명 병기

## 확인

- `Clearwater`는 일반 영어 표현처럼 보이지만 `Clearwater Port`와
  `Clearwater Lake`에서 특정 항구·호수의 고유 지명으로 사용된다.
- 따라서 `맑은물`만 쓰면 한국어 의미는 전달되지만 원문 식별 정보가
  사라진다.

## 적용

- `Clearwater Port` → `맑은물(Clearwater) 항구`
- `Clearwater Lake` → `맑은물(Clearwater) 호수`
- 용어집에 의미역 가능한 고유 지명도 원문을 병기한다는 notes를 추가했다.
- `TRANSLATION-RULES.md`에 일반명사처럼 보이는 고유 지명의 판정과
  복합 표현 병기 규칙을 추가했다.

## 범위와 보류

- 기존 PO에서 이미 `맑은물(Clearwater)`로 통일된 활성 표기는 유지했다.
- 이번 수정은 규칙과 용어집 기록 중심으로 진행했으며, 다른 의미역
  가능 지명은 각 PO의 원문 문맥을 확인하면서 후보를 확정한다.
- 일반 문장의 `clear water`는 고유 지명이 아니므로 병기하지 않는다.

## 검증

- `audit_glossary.py`: `rows=5035`, `errors=0`, `warnings=0`
- 규칙·용어집 변경의 의미상 검증 완료
- 전체 `glossary.tsv`에는 기존 trailing tab이 다수 있어 `git diff --check`
  전체 검사는 기존 항목에서 경고가 발생한다. 이번 추가 notes 자체의
  용어집 감사에는 오류가 없다.
