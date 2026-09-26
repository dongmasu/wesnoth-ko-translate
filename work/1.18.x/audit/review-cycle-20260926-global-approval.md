# 2026-09-26 전체 PO 재검수 통합 승인 리포트

## 목적과 범위

기존 PO별 검수 이후 확정된 번역 규칙이 전체 `work/1.18.x/ko/*.po`에
일관되게 적용되었는지 다시 확인했다. 이번 단계는 **검수 전용**이며,
사용자 승인 전에는 PO와 용어집을 수정하지 않는다.

검수 대상은 다음과 같다.

- 종족명·생물명과 명시적 복수형
- `heal/healing`, `cure`, `healer/curer`
- `Frozen`, `Exit/Leave/Quit`, `Close`
- 한글(영어) 병기와 중복·누락
- 이전 사이클에서 확정한 예외와 장문 수정의 전역 영향

## 자동 검증 기준선

현재 수정 전 기준선은 모두 통과했다.

```text
전체 메시지: 21,303
활성 미번역: 0
활성 fuzzy: 0
markup_mismatches: 0
placeholder_mismatches: 0
newline_mismatches: 0
용어집: rows=5034, errors=0, warnings=0
병기 감사: pairs=1262, conflicts=0, unresolved=0
전체 테스트: 142개 성공
```

자동 검증 통과는 의미 검수 완료를 뜻하지 않으므로, 아래 후보를 별도로
승인받는다.

## 승인 대상 A: 종족명 잔여 표기

활성 PO 146개 메시지에서 다음 과거 표기가 발견되었다. 한 메시지에
여러 표기가 있을 수 있으므로 표기 발생 수와 메시지 수는 다르다.

| 현재 표기 | 발생 수 | 승인 제안 |
|---|---:|---|
| `엘프족` | 41 | 영어 `Elves/elves`의 명시적 복수형이면 `엘프들`; `elven/elvish` 형용사 문맥이면 `엘프의`로 문맥별 수정 |
| `난쟁이족` | 55 | 영어 `Dwarves/dwarves`의 복수형이면 `난쟁이들`; 소유·수식 문맥은 `난쟁이의` 또는 `난쟁이들`로 원문 문법에 맞춤 |
| `드워프들` | 67 | 프로젝트 표준 `난쟁이들`로 통일. 원문 복수형은 유지하고 표기만 표준화 |

후보가 있는 파일은 다음 13개다.

```text
wesnoth-anl-ko.po       wesnoth-did-ko.po      wesnoth-dm-ko.po
wesnoth-ei-ko.po        wesnoth-httt-ko.po    wesnoth-low-ko.po
wesnoth-nr-ko.po        wesnoth-sof-ko.po     wesnoth-sota-ko.po
wesnoth-thot-ko.po      wesnoth-units-ko.po   wesnoth-utbs-ko.po
wesnoth-wof-ko.po
```

이 묶음은 기존에 확정한 “영어 복수형은 한국어도 `들`” 규칙과
`glossary.tsv`의 `Elves=엘프들`, `Dwarves=난쟁이들` 표준에 직접
어긋난다. 다만 `elven/elvish`, 소유격, 화자의 말투가 섞여 있으므로
단순 문자열 치환은 하지 않고 각 메시지의 영어 원문을 보고 수정한다.

### A-2. Wose 잔여 오역

다음 6건은 확정 표기 `워즈(Wose)/워즈들(Woses)`에 직접 어긋나는
고신뢰 수정 후보다.

- `wesnoth-ei-ko.po`: `woses` → `나무정령들`, `woses` → `나무정령`
- `wesnoth-help-ko.po`: `woses` → `워스`
- `wesnoth-multiplayer-ko.po`: 표시 문자열 `Woses` 영어 잔존
- `wesnoth-multiplayer-ko.po`: `wose/woses` → `나모/나모들`
- `wesnoth-sotbe-ko.po`: `wose-born allies` → `나모붙이 동맹군`

복합 문장에서는 `워즈/워즈들`을 문법에 맞게 사용하고, 처음부터
`한글(영어)` 병기가 필요한 표시 문자열·고유 유닛명에는 기존 병기 규칙을
적용한다. 이 항목은 A 승인에 포함한다.

## 승인 대상 B: `heal/cure/healer` 문맥 정리

활성 메시지 중 관련 영어 원문은 221개다. 현재 번역 분포는 다음과 같다.

| 원문 계열 | 회복 | 치료 | 치유 | 해독 | 기타 |
|---|---:|---:|---:|---:|---:|
| `heal/healing/healer` | 100 | 21 | 60 | 0 | 3 |
| `cure/curer` | 16 | 17 | 3 | 1 | 0 |

승인 시 다음 우선순위로 문맥별 수정한다.

- HP 회복·회복 능력·`heal/healing` → `회복`
- 독·상태 이상 제거·`cure/cures` → `치료`
- 독을 제거하는 행위가 명시된 경우 `해독`도 허용
- `healer`는 게임 유닛 역할명 기준으로 `회복사`; `curer`는 독 제거
  역할을 가리키는 문맥에서 `치료사` 또는 승인된 짧은 표현으로 별도 판단
- 서사에서 `healing senses`, `healing art`처럼 의학·치유 개념을
  묘사하는 표현은 기계적으로 `회복`으로 바꾸지 않고 보류 또는 문맥
  수정 대상으로 둔다

대표적인 고신뢰 후보는 다음과 같다.

- `wesnoth-manual-ko.po`: `Cures` → `치유`는 `치료` 검토 대상
- `wesnoth-ko.po`: 능력명 `<i>Cures</i>` → `<i>치유</i>`는 `치료` 검토 대상
- `wesnoth-help-ko.po`: `A curer can cure...`의 `치유사`와 독 제거 설명
- `wesnoth-help-ko.po`: `Villages allow ... to heal, or to be cured...`의
  `치유되거나 독에서 회복` 문장
- `wesnoth-help-ko.po`, `wesnoth-manual-ko.po`: 게임 능력 설명에서
  `healer`를 `치료사/치유사`로 쓴 항목
- `wesnoth-utbs-ko.po`: `Healers`와 탈수·HP 회복 설명의 혼용

이 묶음은 의미가 서로 다른 동사와 역할명을 포함하므로, 승인 후에도
영어 원문별로 수정한다. 전체 자동 치환은 하지 않는다.

## 승인 대상 C: UI·게임 용어

| 원문·문맥 | 현재 표기 | 판정 |
|---|---|---|
| `Frozen` 지형·색상 문맥 | `얼음 지형` | 문제 없음 |
| Editor 그룹 `frozen` | `얼음 타일` | Editor 전용 문맥 예외로 문제 없음 |
| `Always rest heals` | `상시 휴식 회복` | 문제 없음 |
| `Exit` UI | `나가기` | 문제 없음 |
| `Leave` 선택지 | `나가기` | 문제 없음 |
| `Quit` 프로그램·게임 종료 | `종료` | 문제 없음 |
| `Close` | `닫기` | 문제 없음 |
| `Cures` 능력명 | `치유` | 승인 대상 B와 함께 `치료` 여부 검토 |

## 승인 대상 D: 고유명사·병기

현재 병기 감사는 `conflicts=0`, `unresolved=0`이다. 활성 후보 94개도
단축키, 기술 식별자, 시나리오 ID, 폰트명, 외부 서비스, manpage 리터럴,
이미 병기된 이름의 부분 토큰으로 분류되었다.

새로 병기를 추가할 내부 고유명사는 확인되지 않았다. 다음은 수정하지
않는다.

- `Cmd`, `Ctrl`, `Shift`, `ESC`
- `API`, `CPU`, `URL`, `POSIX`, `GUI`, `TLS`, `ZOC`
- `Pango`, `SDL`, `D-Bus`, `Win32`, `Cocoa`
- `Discord`, `Reddit`, `Steam`
- 옵션명·경로·WML·roff·placeholder
- 이미 병기된 `웨스노스(Wesnoth)`, `모르틱(Mortic)` 등의 부분 토큰

`Saurian`, `Wose`, `Wyrm`, `Wyrms of Khrakrahs`의 활성 표기는 현재
확정 규칙과 일치한다. Wyrm의 멸칭 예외도 유지한다.

## 승인 대상 E: 장문·띄어쓰기

앞선 장문 재검수에서 확인된 고신뢰 오류 7건은 이미 수정되어 있다.
이번 전역 재검수에서는 새로 자동 확정할 장문 수정은 만들지 않았다.
다만 승인된 A·B 항목을 실제 문장에 반영할 때 다음을 함께 확인한다.

- `족` 잔존으로 인해 문장 주어·목적어가 어색해지는지
- `회복/치료/치유` 변경으로 의미가 중복되거나 반대로 바뀌지 않는지
- 화자 말투·의도적 비문을 일반 문체로 과도하게 교정하지 않는지
- 태그·placeholder·실제 개행을 유지하는지

## 아직 수정하지 않은 항목

- 모든 PO 파일
- `work/1.18.x/glossary.tsv`
- MO 파일·배포 산출물
- 설치·플레이테스트·tag

## 일괄 승인 요청

다음 두 묶음의 일괄 승인을 요청한다.

1. **A 승인**: 전체 PO의 `엘프족`·`난쟁이족`·`드워프들`을 영어 원문
   문맥에 맞게 표준 복수형·소유 표현으로 정리하고, Wose 잔여 오역
   6건을 `워즈(Wose)/워즈들(Woses)` 규칙에 맞게 수정
2. **B 승인**: 전체 PO의 `heal/cure/healer` 관련 혼용을 원문 문맥에
   맞게 `회복/치료/회복사` 중심으로 정리하고, 서사적 `치유` 표현은
   별도 보존

C는 현재 유지한다. `Quit to Menu`, `Quit to Desktop`은 화면 동작 확인
전까지 보류한다. D는 수정하지 않으며, E는 A·B 수정 과정에서만 함께
확인한다. 승인 후에도 실제 수정은 PO 순서대로 수행하지만, 사용자
승인은 이번 통합 승인 1회로 처리한다.
