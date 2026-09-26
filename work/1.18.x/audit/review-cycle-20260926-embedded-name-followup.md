# 2026-09-26 전역 고유명사·병기 후속 감사

## 범위

전체 작업 PO에 대해 다음 감사를 다시 실행했다.

```text
python3 tools/audit_and_pair_embedded_names.py --check
pairs=1262 conflicts=0
messages=30 unresolved=0

python3 tools/audit_and_pair_embedded_names.py --candidates
candidates=157
active_candidates=94
obsolete_candidates=63
```

자동 후보는 영문 토큰이 남아 있다는 이유만으로 병기를 요구하지 않는다.
각 후보의 원문·번역문·문맥을 확인해 내부 고유명사인지 분류했다.

## 후보 분류

### 수정하지 않는 활성 후보

- `Cmd`, `Ctrl`, `Shift`, `ESC` 등 단축키와 키 이름
- `S11`, `S12`, `S17b`, `WC2`, `SoF` 등 시나리오·진영·프로젝트 식별자
- `$gold_amount_S11` 같은 placeholder 구성요소
- `API`, `CPU`, `URL`, `POSIX`, `GUI`, `EOL`, `TLS`, `X11`, `ZOC` 등
  기술 약어
- `Bzip2`, `Gzip`, `Pango`, `SDL`, `D-Bus`, `Win32`, `Cocoa` 등
  라이브러리·백엔드·프로토콜·기술 식별자
- `Lato`, `DejaVu`, `Oldania ADF Std` 등 폰트명
- `Discord`, `Reddit`, `Steam` 등 외부 서비스·브랜드
- manpage의 옵션명, 경로, 매크로명, roff 리터럴과 URL
- 저작자·번역자 정보처럼 게임 내부 고유명사가 아닌 메타데이터
- `Dark Forecast`, `Isle of Mists`, `A New Land`, `Team Survival`처럼
  현재 번역문에서 제목 자체를 원문으로 유지한 시나리오 제목 토큰
- 이미 같은 문장 안에서 `웨스노스(Wesnoth)`, `모르틱(Mortic)`처럼
  올바르게 병기된 이름의 부분 토큰

이 분류의 영문 잔존은 번역 누락이나 병기 누락으로 보지 않는다. 기술
리터럴과 식별자를 한글(영어) 형식으로 바꾸면 오히려 실행·검색·문서
호환성을 해칠 수 있다.

### obsolete 후보

63개 obsolete 후보는 현재 활성 번역이 아니며, 역사 자료 보존 원칙에
따라 삭제하거나 새 병기 규칙으로 재작성하지 않았다. obsolete 항목의
존재는 활성 병기 감사 실패로 계산하지 않는다.

## 실제 내부 고유명사 확인 결과

활성 후보 94개를 문맥별로 확인한 결과, 새로 `한글(English)` 병기를
추가해야 하는 내부 인명·지명·세력명·고유 유닛명은 확인되지 않았다.

- 원문과 번역문이 모두 기술 식별자 또는 메타데이터인 경우: 원문 유지
- 원문 안에 시나리오 제목이 포함되지만 표시 제목 자체를 유지하는 경우:
  제목을 임의로 분해하거나 중복 병기하지 않음
- 이미 병기된 이름의 일부 단어가 후보로 잡힌 경우: 중첩 병기하지 않음
- 실제 내부 고유명사로 확인되는 항목이 새로 발견되는 경우: 용어집에
  먼저 승인 등록한 뒤 영향 범위를 지정해 수정해야 함

## 결론

이번 전역 감사에서 고신뢰 병기 수정은 없다. `--check`의
`conflicts=0`, `unresolved=0`을 유지했으며, 자동 후보 목록을 근거로
PO 전체를 일괄 수정하지 않았다.

## 검증

- PO 수정: 없음
- 용어집 수정: 없음
- 병기 구조: `pairs=1262`, `conflicts=0`, `unresolved=0`
- 다음 단계: 사용자 승인 전까지 1·2번 사이클을 종료 상태로 유지
- 이번 단계에서 하지 않은 작업: MO 생성, 설치 테스트, 플레이테스트,
  배포 및 tag
