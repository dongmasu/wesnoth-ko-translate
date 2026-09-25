# Translation Work

이 디렉터리는 실제 번역을 수정하는 작업 공간입니다.

## 구조

```text
work/
├── README.md
└── <버전>/
    ├── README.md
    ├── glossary.tsv
    └── ko/
        └── *.po
```

- `work/<버전>/ko/`: 실제로 수정하고 검토하는 한국어 PO 파일
- `work/<버전>/glossary.tsv`: 표준 번역, 일본어·중국어 참고 표현, 의미
  분류와 근거를 기록하는 작업용 용어집
- `po/<버전>/`: Wesnoth GitHub에서 받은 locale별 원본 PO 스냅샷
- `References/`: 과거 한국어 번역과 네이버 카페 등 참고 자료
- `References/wesnothko/translation-notes.tsv`: 한글화 팀 게시판과
  자유게시판에서 선별한 용어·명칭 참고 메모
- 버전 기본값은 루트 `VERSION`에서 읽으며, 도구 실행 시
  `WESNOTH_VERSION=<버전>`으로 덮어쓸 수 있습니다. 새 버전은 같은
  `po/<버전>/`, `work/<버전>/`, `dist/<버전>-<작업일>/` 구조를 사용합니다.
- `dist/<버전>-<작업일>/`의 MO와 메타데이터는 공개 산출물로 Git에
  포함합니다. 설치 도구는 대상의 기존 `*.mo`를 삭제하고 전체 MO 세트를
  동기화하며 다른 파일은 보존합니다. 문제가 생기면 `po/<버전>/ko/` 또는
  `work/<버전>/ko/`에서 MO를 다시 생성합니다.
- 루트 문서의 버전 표기는 `docs/templates/*.md.in`에서 관리합니다.
  템플릿을 수정한 뒤 `python3 tools/render_docs.py`로 게시 문서를
  재생성하고, `--check`로 생성 결과를 검증합니다. 생성된 Markdown은
  직접 수정하지 않습니다.

## 작업 기준

- PO 파일의 구성과 `msgid`는 `po/<버전>/ko/`를 기준으로 유지합니다.
- 기존 한국어 표현은 `References/20250322_wesnoth_한국어번역/`을
  가능한 한 적극적으로 활용합니다. 다만 현재 영어 원문·게임 문맥·태그·
  placeholder와 충돌하면 그대로 복사하지 않고 근거를 남겨 조정합니다.
- 인명·지명·종족명·유닛명은 한글 표기를 우선합니다. 일본어가 영어를
  그대로 쓰더라도 한국어 영어 보존의 근거로 삼지 않습니다. 중국어는
  음역 비교용 보조 자료로 사용합니다.
- 첫 등장 여부를 사람이 판정해 병기하지 않습니다. `category` 분류를
  병기 기준으로 사용하지 않고, 용어집 각 행의 영어 원문과 한국어를
  직접 비교해 실제 음차된 부분만 `한글(English)`로 병기합니다.
  `Discord`, `Steam`, `IRC` 같은 외부 브랜드·프로토콜·식별자는 원문을
  유지합니다.
- 복합 고유명사는 전체 source_term을 괄호에 넣지 않고, 실제 고유명사
  부분만 병기합니다. `Minion of Tairach`는
  `타이라크(Tairach)의 졸개`, `Lady Dionli`는 `디온리(Dionli) 부인`입니다.
  단, `Mal Tath`처럼 여러 단어가 분리할 수 없는 하나의 이름이면
  `말 타쓰(Mal Tath)`처럼 전체를 한 번만 병기하고 구성 요소를 중첩
  병기하지 않습니다.
- 영어(`en_GB`)를 기본 원문으로 확인하고, 일본어(`ja`)와
  중국어(`zh_CN`)는 보조 참고 자료로 사용합니다.
- 번역을 수정한 뒤에는 `tests/`의 구조·문법 검사를 실행합니다.
- `glossary.tsv`에 기록된 표준 용어는 번역자가 누구든 동일하게 사용해야
  하는 표준 번역입니다.
- 용어집 1차 검수가 끝난 뒤에는 `ko/*.po` 전체를 다시 읽는 2차 전수
  번역 검수를 수행합니다. 자동 감사가 통과해도 의미, 문체, 조사,
  고유명사 병기, 문맥별 일관성 검토를 생략하지 않습니다.
- `sync_contextual_glossary.py`, `sync_glossary_korean.py`,
  `normalize_contextual_translations.py`처럼
  PO나 용어집을 수정하는 도구는 먼저 단독으로 실행하고 종료를 확인합니다.
  이 도구들과 테스트·`msgfmt`·감사 명령을 병렬 실행하지 않습니다.
- `source_term`에 `^`가 포함된 항목은 먼저 일반 문맥 키인지 Wesnoth의
  성별 표기인지 확인합니다. `feature^Open`, `filesystem^Open`처럼 일반
  문맥 키인 경우 `^` 앞부분은 식별자로 보존하고 뒤의 표시 문자열만
  번역합니다. `source_term`에는 전체 키를 기록합니다.
- `female^`, `male^`, `race^`도 gettext 문맥 식별자입니다. 원문 전체 키는
  `source_term`에 보존하지만, `msgstr`와 표준 한국어에는 `^` 뒤의 표시
  문자열만 기록합니다. `여성`, `암컷`, `종족`이 실제 번역 의미인 경우에는
  일반 한국어 단어로 남길 수 있지만 `여성^회복됨`처럼 접두사를 표시하지
  않습니다.
- 활성 메시지뿐 아니라 `#~`로 표시된 obsolete 메시지도 고유명사 병기,
  태그, placeholder 검수 대상에 포함합니다. obsolete 메시지는 삭제하지
  않고 과거 자료로 보존하되, 현재 표기 규칙에 맞지 않으면 함께 정리합니다.
- `^`가 있는 항목은 전체 키를 하나의 독립된 항목으로 취급합니다. 문맥
  접두사가 다르면 표시 문자열이 같아도 용어집 항목과 번역을 합치지 않습니다.
- 같은 `msgid`라도 PO 주석 문맥에 따라 뜻이 달라질 수 있습니다. 예를 들어
  `Music`은 `[about]`에서는 `음악 담당`, `[column]`에서는 `음악`입니다.
  이런 항목은 용어집 하나의 표준값으로 합치지 않고 PO 문맥별 번역을
  유지합니다.
- 일반 응답인 `yes`·`no`는 `예`·`아니오`로 번역합니다. `있음`·`없음`은
  존재 여부나 상태값이라는 문맥이 확인된 경우에만 사용합니다.
- 용어집에는 반복되는 용어, 고유명사, 게임 규칙 용어, 짧은 고정 UI
  표현만 기록합니다. 일반적인 긴 대사와 설명문은 해당 PO의 `msgstr`로
  번역하며 용어집에 복사하지 않습니다.
- manpage의 긴 옵션 설명도 용어집에 복사하지 않습니다. `B<>`, `I<>` 표식,
  옵션명, 명령 구문, 파일명, URL, 경로와 역슬래시는 보존하고 설명만
  해당 PO에서 번역합니다.
- 도구 이름은 원문을 보존합니다. 예를 들어 `wmllint`는 `wmllint`로
  유지하고, `wmllint mode`는 `wmllint 모드`로 번역합니다. 도구 이름에
  `교정`처럼 원문에 없는 의미를 덧붙이지 않습니다.
- `Tarek`처럼 일본어는 `Tarek`, 중국어는 음역, 한국어는 `타렉`인 경우가
  있을 수 있습니다. 이런 항목은 일본어의 영어 보존을 따라가지 않고,
  최신 한국어 참고자료의 한글 표기를 표준으로 삼습니다. `Discord`,
  `Steam`, `IRC` 같은 외부 브랜드·프로토콜·식별자는 별도 예외입니다.
- 과거 대안과 논쟁은 `forbidden_terms`, `translation-notes.tsv` 및
  참고자료에 기록하며 표준 번역으로 사용하지 않습니다.
- 용어집의 `forbidden_terms`는 과거 표현 또는 현재 검토 중인 대안이며,
  금지어로 최종 확정하기 전에는 문맥을 반드시 확인합니다.
- 용어집 열은 다음 의미로 사용합니다.
  - `source_term`: 원문 용어 또는 짧은 고정 표현입니다. 긴 대사와 설명문은
    기록하지 않습니다.
  - `standard_korean`: 최종 표준 한국어 표현입니다.
  - `reference_japanese`, `reference_chinese`: 해당 PO에 실제로 있는
    일본어·중국어 표현이며 새로 번역해 넣지 않습니다.
- `category`: 인명·지명·유닛명·일반 용어 등을 구분하는 의미 분류입니다.
    `category`(분류)이며, `person_name`, `place_name`, `race_name`,
    `proper_noun`, `unit_name`, `faction`, `ability`, `contextual`,
    `terrain`, `attack_type`, `ui`, `command`, `term` 등을 사용합니다.
    인명·지명·고유명사·UI·명령어를 모두 `term`으로 뭉뚱그리지 않습니다.
  - `forbidden_terms`: 실제로 채택하지 않을 과거 표현·오역·대안입니다.
    해당 항목이 없으면 빈 칸으로 둡니다.
  - `notes`: 병기·예외·번역 선택처럼 출처 경로만으로 설명되지 않는
    판단 근거만 기록합니다. 실제 PO 출처는 `po/<버전>/`의 locale별
    디렉터리와 프로젝트 문서로 확인하며, 자동으로 반복되는 출처·분류
    설명은 기록하지 않습니다.
- 영어 원문이 한국어에 남아 있다는 사실만으로 병기하지 않습니다. 외부
  서비스명·폰트명·프로토콜·약어·도구명·모드 식별자는 필요하면 영문 그대로
  유지하고, 내부 인명·지명·실제 이름 구성요소만 음차와 함께
  `한글(English)`로 표기합니다. 이 판정은 `category`가 아니라 원문과
  한국어 표기의 토큰을 직접 대조해 수행합니다.
- 병기 정규화 도구는 멱등적이어야 합니다. 반복 실행해도 수동으로 확정한
  표준 번역이 자동 추론에 의해 되살아나거나 다른 값으로 변하지 않아야 합니다.
- 숫자만 있는 항목, 기호만 있는 항목, 긴 문장·대사·설명문은 용어집에
  넣지 않습니다. 실제 게임 식별자나 기호 리터럴만 `identifier` 문맥으로
  예외를 둘 수 있습니다.
- 현재 수동 번역 배치는 기본 50개로 진행합니다. 처리 속도를 이유 없이
  10개, 20개 또는 40개로 줄이지 않습니다. 태그·placeholder·실제 `\n`·복수형,
  `^` 문맥 키, 고유명사 충돌, 긴 대사 또는 참고 자료 간 충돌처럼 검토
  비용이 높은 항목만 별도 소배치로 나눌 수 있습니다. 소배치가 끝나면
  다음 배치부터 다시 50개로 진행하고, 분할 사유와 항목 수를 작업 보고에
  남깁니다.
- 번역문은 원문의 구조적 표식을 보존해야 합니다. 실제 `\n`과 문단·대사
  경계를 유지하고, PO의 문자열 분할 줄과 게임 개행을 혼동하지 않습니다.
  `<i>`, `<b>`, `<span ...>`, `<ref ...>` 같은 Pango/HTML 태그의 이름,
  속성, 짝, 개수를 유지하며, `%s`, `%d`, `$unit.name`, `$gold_cost`
  같은 placeholder도 철자와 대소문자를 그대로 유지합니다. 한국어 조사는
  placeholder 뒤에 붙이되 이름 안에 포함하지 않습니다.
- 모든 일반 `^` 문맥 키의 앞부분은 UI 표시 문자열이 아닌 식별자이므로
  번역문에 넣지 않습니다. `female^`, `male^`, `race^`도 예외가 아닙니다.
  용어집에는 검색·대조를 위해 전체 `source_term`을 기록합니다.
- 복수형 항목은 `msgid_plural`과 `msgstr[n]` 구조를 유지합니다. 빈
  `msgstr[n]`은 미번역으로 보고, fuzzy 표시가 있는 항목도 검토 전에는
  완료로 세지 않습니다.

## 전체 PO 전수 검수

용어집을 먼저 확정한 뒤 `work/<버전>/ko/*.po`의 모든 활성 메시지를
다시 검토합니다. 이 단계는 미번역 개수 확인과 별개이며, 이미 번역된
문장도 다음 기준으로 재검수합니다.

- 용어집 표준 번역과 고유명사 음차·병기 규칙이 적용되었는가
- 영어 의미와 게임 문맥이 보존되었는가
- 일본어·중국어 및 `References/20250322_wesnoth_한국어번역/`과 비교해
  누락·과역·문체 불일치가 없는가
- 조사, 존대, 명령형, 수식어 위치가 자연스러운가
- `^`, 실제 `\n`, 태그, placeholder, 복수형, roff 표식이 보존되었는가

전수 검수 중 용어집을 수정하면 관련 PO 전체에 표준 번역을 재적용하고,
변경 항목을 다시 검토한 뒤 테스트와 구조 감사를 실행합니다.

## 규칙·예외 유지보수

번역 작업 중 발견한 판단 기준은 다음 범위에 맞춰 기록합니다.

- 모든 AI·사람 작업자에게 적용되는 규칙: `PROJECT-AI.md`
- 버전별 작업 흐름, 우선순위, 반복되는 예외: 이 문서
- 반복 용어의 표준 한국어, 일본어·중국어 참고값, 금지 표현과 근거:
  `work/<버전>/glossary.tsv`
- 자동으로 재현할 수 있는 구조·형식 문제: `tests/`
- 특정 번역문에만 필요한 설명: 해당 PO의 기존 주석 또는 검토 기록

예외를 추가할 때는 `왜 기본 규칙을 적용할 수 없는지`, `어떤 파일과
문자열에 영향을 주는지`, `다음 작업자가 어떻게 재현·검증할 수 있는지`를
함께 적습니다. 원문 오류처럼 보이는 태그·placeholder·개행·공백은
번역 예외로 처리하지 않고 먼저 검토 상태로 둡니다. `^` 문맥 키, 복수형,
manpage 표식, 명령어·경로 리터럴은 일반 문장과 다른 구조를 갖지만,
그 구조를 보존하는 것이 규칙이지 임의 변경을 허용하는 예외가 아닙니다.

용어집을 수정한 경우에는 관련 PO의 표준 번역 반영 여부를 확인하고,
문서 규칙이 바뀐 경우에는 해당 규칙을 검증하는 테스트를 함께 추가하거나
기존 테스트를 갱신합니다. 배치가 끝날 때는 변경 범위, 참고한 자료,
검증 명령과 남은 검토 대상을 작업 보고에 남깁니다.

## 용어집과 PO 동기화

gettext 문맥 항목을 재검토하거나 용어집을 갱신한 뒤에는 다음 도구를
실행해 용어집과 작업용 한국어 PO를 함께 맞춥니다.

```sh
python3 tools/sync_contextual_glossary.py
python3 tools/audit_and_pair_embedded_names.py
python3 tools/normalize_glossary_labels.py
python3 tools/sync_glossary_korean.py
python3 tools/audit_po_structure.py
```

## 검증

프로젝트 루트에서 실행합니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
python3 -m unittest discover -s tests -v
python3 tools/audit_glossary.py
python3 tools/audit_and_pair_embedded_names.py --check
python3 tools/audit_po_completion.py
python3 tools/audit_po_structure.py
find "work/$VERSION/ko" -name '*.po' -print0 |
  xargs -0 -n1 msgfmt --check --output-file=/dev/null
```

`audit_po_structure.py`는 현재 작업 PO에 남은 태그·placeholder 불일치를
보고하는 감사 도구입니다. 결과가 0이 아니면 번역을 완료로 표시하지 않고
파일과 `msgid`를 검토 목록으로 남깁니다. 원문 자체가 불균형한 태그를
가지거나 도구의 인식 범위를 벗어난 특수 표식인 경우에도 임의로 삭제하지
말고, 원문·번역문·참고 locale을 대조한 뒤 규칙 또는 테스트를 갱신합니다.
`msgfmt --check`의 기본 헤더 경고는 PO 문법 오류와 구분하여 보고하되,
새 작업 파일의 헤더를 확인합니다.

## 문서만으로 하는 감사

새 작업자는 대화 기록 없이 `PROJECT-AI.md`, 루트 `README.md`,
`INSTALL.md`, 이 문서, 버전별 README와 `glossary.tsv`만 읽고도 결과를
검증할 수 있어야 합니다.

감사 대상은 `work/<버전>/ko/*.po`의 활성 메시지입니다. 첫 번째
`msgid ""` 헤더와 `#~` obsolete 항목은 진행률에서 제외합니다. 활성
`#, fuzzy`는 번역문이 있어도 미확정으로 세며, 비-fuzzy `msgstr ""`와
복수형의 빈 `msgstr[n]`은 미번역으로 셉니다. `msgfmt --check`의 헤더
기본값 경고는 종료 코드와 분리해 기록합니다.

감사할 때는 활성 PO의 빈 번역·빈 복수형·`fuzzy`, 용어집-PO 불일치,
금지 대안 재등장, 고유명사 병기 누락, `^` 문맥 접두사 누출,
태그·placeholder·실제 `\n` 불일치를 확인합니다. `#~` obsolete 항목은
활성 진행률에서는 제외하지만, 고유명사 병기·태그·placeholder 감사에는
포함합니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
python3 -m unittest discover -s tests -v
python3 tools/audit_glossary.py
python3 tools/audit_po_structure.py
python3 tools/audit_and_pair_embedded_names.py --candidates \
  | tee "work/$VERSION/audit/embedded-name-candidates-$(date +%Y%m%d).txt"
python3 tools/audit_and_pair_embedded_names.py --check
find "work/$VERSION/ko" -name '*.po' -print0 |
  xargs -0 -n1 msgfmt --check --output-file=/dev/null
```

활성 빈 번역과 fuzzy를 파일별로 확인하려면 다음을 추가로 실행합니다.

```sh
for po in "work/$VERSION/ko"/*.po; do
    untranslated="$(
        msgattrib --untranslated --no-fuzzy --no-obsolete "$po" |
        awk '$1 == "msgid" { count++ } END { print count + 0 }'
    )"
    fuzzy="$(
        msgattrib --only-fuzzy --no-obsolete "$po" |
        awk '$1 == "msgid" { count++ } END { print count + 0 }'
    )"
    printf '%s untranslated=%s fuzzy=%s\n' "$po" "$untranslated" "$fuzzy"
done
```

정상 결과는 활성 fuzzy 0, 빈 번역 0, 빈 복수형 0,
`markup_mismatches=0`, `placeholder_mismatches=0`, 용어집-PO 불일치
0건입니다.

## MO 빌드와 설치 도구

- `tools/build_mo.sh [version] [output_dir]`: macOS·Linux에서
  `work/<version>/ko/*.po`를 `msgfmt --check`로 검사하고 MO를 생성합니다.
  마지막 PO 수정일을 `dist/<version>-<work-date>/ko/PO_LAST_MODIFIED_DATE`에 기록합니다.
- `tools/build_mo.bat [version] [output_dir]`: Windows에서 같은 작업을
  수행하고 MO 생성 날짜를 같은 메타데이터 파일에 기록합니다.
- `tools/install_mo.sh <target_dir> [source_dir]`: macOS·Linux에서
  명시한 `translations/ko/LC_MESSAGES`에 MO를 설치합니다.
- `tools/install_mo.bat <target_dir> [source_dir]`: Windows에서 같은
  작업을 수행합니다.
- `tools/mark_korean_locale.sh <ko_KR.cfg>` 및
  `tools/mark_korean_locale.bat <ko_KR.cfg>`: 게임 언어 목록에
  `한국어 (<작업버전>-<작업날짜>)` 표식을 기록합니다. Windows ZIP판은
  `data\languages\ko_KR.cfg`를 직접 지정합니다.

설치 도구는 대상 경로를 자동 추측하지 않습니다. 기존 `*.mo`가 있으면
삭제 후 새 MO 전체를 복사하므로, 잘못된 Wesnoth 설치본에 복사하지 않도록
게임의 데이터 경로를 먼저 확인합니다. 문제가 생기면
`po/<버전>/ko/` 또는 `work/<버전>/ko/`에서 MO를 다시 생성합니다.
게임에 적용하기 전에는
`INSTALL.md`의 운영체제별 경로 확인 절차를 먼저 수행합니다.

## 용어집 판정 규칙

`work/<버전>/glossary.tsv`는 다음 순서로 검수합니다.

1. `source_term`은 PO의 실제 `msgid`를 대소문자까지 그대로 기록합니다.
   `^`가 있으면 전체 키를 기록하고 다른 문맥의 같은 표시 문자열과
   합치지 않습니다.
2. 반복 용어, 고유명사, 게임 규칙 용어, 짧은 고정 UI만 기록합니다.
   긴 문장·대사·설명문·숫자만 있는 값은 기록하지 않습니다.
3. `standard_korean`은 실제 표시 문자열이며 같은 `source_term`의 모든
   작업 PO에서 동일해야 합니다. 문맥별 의미가 다른 항목은 합치지 않습니다.
4. `category`는 인명·지명·종족명·유닛명·일반 용어 등을 설명하는 분류일
   뿐이며, 번역 여부나 병기 여부를 결정하는 기준이 아닙니다.
5. 영문 잔존만으로 병기하지 않습니다. 외부 브랜드·서비스명·폰트명·
   프로토콜·약어·도구명·모드 식별자는 영문 그대로 둘 수 있습니다.
6. 내부 인명·지명·실제 이름 구성요소를 음차한 경우에만 그 부분을
   `한글(English)`로 병기합니다. 복합어 전체를 괄호에 넣지 않으며
   조사·호칭·수식어는 괄호 밖에 둡니다.
   - `Garard II` → `가라르드(Garard) 2세`
   - `Garard’s Hold` → `가라르드(Garard)의 요새`
   - `Fire Dragon` → `불의 드래곤(Dragon)`
   - `Masked Dwarf` → `가면 쓴 난쟁이`
   약어·일반 명칭·편집기 좌표 레이블은 음차가 아니므로 원문을
   괄호로 반복하지 않습니다. `AToTB` → `형제`, `Northerners` →
   `북부인`, `Base.x` → `기준점 X`처럼 기록합니다.
7. `forbidden_terms`는 폐기 표현·오역·검토에서 제외한 대안이 있을 때만
   기록하고, 없으면 빈 칸으로 둡니다. `notes`도 병기·예외·번역 선택처럼
   재검수에 필요한 결정만 기록합니다.
8. 일본어·중국어 열은 실제 PO의 참고값이며 한국어 자동 번역 규칙이
   아닙니다. 최우선 한국어 참고자료와 현재 영어 문맥을 함께 확인합니다.

## 영어·일본어·중국어 전수 대조

전체 활성 PO 항목은 다음 명령으로 동일한 gettext 키를 맞춰 비교합니다.
출력은 영어와 동일한 한국어, 영어 잔존, 누락된 placeholder 후보를
찾기 위한 검토 목록입니다. 후보를 자동으로 덮어쓰지 않습니다.

```sh
python3 tools/audit_locale_comparison.py --limit 200
```

이 도구의 영어 잔존 후보는 자동 실패 목록이 아니다. 폰트명(`Lato`),
압축 방식(`Bzip2`, `Gzip`), 명령어·식별자·변수·생성용 문법은 원문을
유지할 수 있다. 반면 지도 제목·UI 문구·설명문에 영어가 남아 있으면
일본어·중국어와 대조해 실제 누락인지 확인하고 한국어로 수정한다.
후보를 예외 처리할 때도 placeholder, 태그, `^` 문맥 키의 구조는
변경하지 않는다.

고유명사 후보 감사 결과는 `work/<버전>/audit/`에 날짜별로 저장한다.
각 후보를 영어·일본어·중국어·기존 참고 번역과 대조한 뒤 용어집에
등록하거나 정당한 영어 잔존 예외로 판정한다.
문장형 용어집 후보도 `work/<버전>/audit/`에 별도로 기록하고,
PO 문맥을 확인한 뒤 용어집에서 제거하거나 짧은 UI 고정 문구로 남긴다.

2026-09-25 전수 대조에서 활성 키 20,564개를 영어·일본어·중국어와
맞췄고, 구조·placeholder 감사는 통과했다. 남은 후보는 기술 문자열,
생성 문자열, 고유명사와 일부 영어 잔존을 포함하므로 후보별 의미 검토를
계속한다.
9. 용어집 수정 후 PO를 동기화하고, 정규화 도구를 두 번 실행해도 파일이
   변하지 않는지 확인합니다. 테스트·구조 감사·`msgfmt --check`까지
   통과해야 해당 검수를 완료로 기록합니다.

검수 체크리스트:

- [ ] 실제 PO `msgid`와 대소문자까지 일치하는가?
- [ ] 중복·문장·대사·숫자 전용 항목이 없는가?
- [ ] 표준 번역이 모든 관련 PO와 일치하는가?
- [ ] 기술 식별자와 음차 누락을 구분했는가?
- [ ] 병기된 괄호 안에는 실제 음차 원문만 있는가?
- [ ] 조사·호칭·수식어가 괄호 밖에 있는가?
- [ ] `^` 문맥 키와 `msgctxt`를 다른 항목과 합치지 않았는가?
- [ ] `forbidden_terms`와 `notes`가 필요한 경우에만 있는가?
- [ ] PO 동기화와 반복 실행 검사를 마쳤는가?
