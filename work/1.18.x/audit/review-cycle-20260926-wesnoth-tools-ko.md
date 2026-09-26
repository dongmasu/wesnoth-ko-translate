# `wesnoth-tools-ko.po` 검수 리포트

- 검수일: 2026-09-26
- 대상: `work/1.18.x/ko/wesnoth-tools-ko.po`
- 활성 미번역: 0
- 활성 fuzzy: 0
- 검수 방식: WML 도구 GUI 문맥·영어 원문·일본어·중국어 참고 PO·용어집 대조

## 이번 수정

- `WML 도구에 대한 ... 열기`를 `WML 도구용 ... 열기`로 자연스럽게 수정
- 로케일 오류 문구의 placeholder 주변 표현을 `"{0} 로케일"`로 정리
- `작업 디렉토리`, `출력 디렉토리`, 핵심 디렉토리 관련 표현을
  `디렉터리`로 통일
- `지움`, `출력물을 지움`, `나가기` 등 GUI 버튼 표현을
  `지우기`, `출력 지우기`, `종료`로 정리
- `Verbosity level`, `Quiet mode`, `Options`, `Package version`,
  `Initial textdomain` 등 도구 GUI 용어를 자연스러운 한국어로 수정
- `side= keys`, `사용 안함 설정`, `지정하지 않는 매개변수` 등 직역·혼용
  표현을 각각 `side= 키`, `비활성화`, `형식 매개변수`로 정리
- 매크로·파일 보고 옵션의 문장을 명령형 UI 표현에 맞게 다듬음
- 선택한 디렉터리가 존재하지 않는 경우와 선택되지 않은 경우를 구분
- 파일 덮어쓰기와 실행 오류 문구의 조사·띄어쓰기를 수정
- `wesnoth-tools-ko.po`에서 실제 사용한 16개 용어를 용어집과 동기화

## 유지한 항목

- `wmllint`, `wmlscope`, `wmlindent`, `wmlxgettext`, `WML`, `GUI`,
  `EOL`, `side=` 등 도구명·식별자·기술 리터럴은 원문을 보존했다.
- 이미 의미가 분명한 `시험 실행`, `변환`, `백업 파일`, `매크로`,
  `텍스트 파일` 등의 표현은 변경하지 않았다.
- obsolete(`#~`) 항목은 수정하지 않았다.

## 보류 및 이월

- `Drakes`의 종족 복수형 표기와 `Frozen`의 전역 표기는 이번 파일의
  직접 문맥이 아니므로 수정하지 않았다. 이전 전역 검수의 잔여 항목으로
  별도 처리해야 한다.
- 도구 GUI 전체 문체를 새로 통일하는 광범위한 재번역은 수행하지 않았다.

## 용어집 영향

다음 항목의 표준값을 이번 PO의 고신뢰 수정에 맞춰 갱신했다.

`Advanced options`, `Clear`, `Clear output`, `Disable spellchecking`,
`Name files before processing`, `Options`, `Package version`, `Quiet mode`,
`Report unchanged files`, `Report unresolved macro references`,
`Scan subdirectories`, `Show changes`, `Skip core directory`,
`Terminate script`, `Verbosity level`, `Working directory`

## 검증

- `msgfmt --check --check-format`: 통과
- `audit_po_structure.py`: `markup_mismatches=0`,
  `placeholder_mismatches=0`, `newline_mismatches=0`
- `audit_glossary.py`: `errors=0`, `warnings=0`
- 도구 GUI·WML 도구명 관련 대상 테스트: 통과
