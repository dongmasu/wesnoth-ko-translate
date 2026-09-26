# `wesnoth-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: PO 원문·실제 문맥·용어집 대조

## 이번 수정

| 원문 | 수정 내용 |
| --- | --- |
| `You are not worthy of healing.` | `당신은 회복될 자격이 없습니다.` |
| `unhealable` | `회복 불가`로 통일 |
| `This unit is unhealable...` | `회복`과 `치료사` 문맥으로 정리 |
| `$unit.name ...` | 조사 띄어쓰기와 문장 자연스러움 수정 |
| `Some eras...` | `시대나` 띄어쓰기 오류 수정 |

`unhealable` 표준값은 용어집에도 `회복 불가`로 동기화했습니다.

## 보류

- 파일 전체의 긴 도움말 문장은 이번 사이클에서 의미가 명백히 어긋난 항목만 수정했습니다.
- obsolete(`#~`) 항목은 활성 번역에 영향을 주지 않으므로 수정하지 않았습니다.
- `heal=회복`, `cure=치료` 기준은 유지했습니다. `cured=치료됨`도 유지합니다.

## 검증

- `msgfmt --check --check-format`: 통과
- `tests.test_po_layout`: 30개 통과
- 용어집 감사: `errors=0`, `warnings=0`

## 추가 검수

- 도움말의 `한방에 죽일때`를 `한 방에 죽일 때`로 수정했다.
- `Frozen = 얼음 지형`, `heal = 회복`, `cure = 치료`, `unhealable =
  회복 불가` 기준은 기존 확정 규칙과 일치해 유지했다.
- 추가 고신뢰 후보는 확인되지 않았다.

## 다음 파일

`wesnoth-lib-ko.po`로 자동 진행한다.
