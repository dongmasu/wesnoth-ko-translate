# `wesnoth-wof-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-wof-ko.po`
- 활성 메시지: 817
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: 캠페인 설명·대사·목표·규칙 설명의 원문 문맥과 확정 용어
  대조

## 이번 수정

- 캠페인 소개와 초반 서술의 명백한 의미·문법 오류를 수정했다.
- `heal/healing`을 `회복`으로 적용하고, `Faerie` 관련 기존 `정령`
  표기를 `요정`으로 통일했다.
- `Wyrm`의 멸칭 문맥인 `도마뱀` 표기는 유지했다.
- `Drakes`, `Saurians` 등 명시적 종족 복수형을 `들`로 유지·정리했다.
- `No recalls are permitted`, 모집 조건, 소환 관련 규칙 설명을 실제
  게임 의미에 맞게 수정했다.
- `full movement` 계열과 근접 공격 표현, 목표 문장, 금화·턴 표기를
  자연스럽게 정리했다.
- 다수의 명백한 오탈자·띄어쓰기·조사 오류를 수정했다.
- `Faerie` 전역 문맥의 `요정` 표기를 용어집 기준에 맞췄다.

## 유지한 항목

- 기존에 반영된 `Wose`, `Wyrm` 예외 및 고유명사 병기는 유지했다.
- 모로고르 방언, 난쟁이 방언, 사우리안의 말투와 의도적인 멸칭은
  일반 문체로 평준화하지 않았다.
- `craftling`, `stonekin`처럼 별도 세계관 용어로 보이는 표현은 근거 없이
  새 이름을 만들지 않았다.
- obsolete(`#~`) 항목은 수정하지 않았다.

## 보류 및 이월

- 장문의 세계관 서술 중 문체 선택과 번역어의 세부 선호 차이는 보류했다.
- 방언 대사의 자연스러움은 화자 표현 보존을 우선했으며, 명백한 오탈자만
  수정했다.
- 다른 PO에 남은 전역 종족·고유명사 불일치는 해당 파일 검수 시 처리한다.

## 용어집 영향

- `No recalls are permitted`의 표준값을
  `소환은 허용되지 않습니다.`로 PO와 동기화했다.
- 새 용어 행은 추가하지 않았다.

## 검증

- `msgfmt --check --check-format`: 통과
- `audit_po_structure.py`: `markup_mismatches=0`,
  `placeholder_mismatches=0`, `newline_mismatches=0`
- `audit_glossary.py`: `errors=0`, `warnings=0`
- `audit_po_completion.py`: 이 파일 `untranslated=0`, `fuzzy=0`
- PO 파일 범위의 `git diff --check`: 통과
- 용어집 전체에는 기존 TSV 행의 trailing tab이 있어 전체 범위
  `git diff --check`는 별도 경고를 냈지만, 구조 감사와 용어집 감사에는
  영향이 없다.
