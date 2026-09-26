# 설치 및 적용 안내 / Installation and Usage Guide

이 문서는 `wesnoth-ko-translate`의 Wesnoth 1.18.x 한국어 PO를 실제
게임에 적용하는 방법을 설명합니다. 게임은 실행 시 PO가 아니라 gettext
바이너리 파일인 `.mo`를 읽습니다.

현재 기본 버전은 루트 `VERSION` 파일에서 읽습니다. 다른 버전은
`WESNOTH_VERSION=<버전>`처럼 환경 변수로 지정할 수 있으며, 해당 버전의
`po/<버전>/`과 `work/<버전>/` 디렉터리가 먼저 준비되어 있어야 합니다.

문서 버전은 `docs/templates/*.md.in`에서 관리합니다. 템플릿을 직접
수정한 뒤 프로젝트 루트에서 `python3 tools/render_docs.py`를 실행하면
게시용 Markdown이 생성됩니다. 생성된 `README.md`, `INSTALL.md`,
`PROJECT-AI.md`, `work/README.md`를 직접 편집하지 말고 템플릿을
수정합니다. 생성 결과는 다음 명령으로 검증할 수 있습니다.

```sh
python3 tools/render_docs.py --check
```

## 한국어

### 1. 준비

필요한 도구:

- GNU gettext의 `msgfmt`
- Wesnoth 1.18.x 설치본
- 이 저장소

`msgfmt`가 없다면 운영체제별로 다음 방법 중 하나로 설치합니다.

```sh
# macOS (Homebrew)
brew install gettext

# Debian/Ubuntu
sudo apt install gettext

# Fedora
sudo dnf install gettext
```

Windows에서는 gettext가 포함된 MSYS2 환경 또는 WSL을 사용하고,
PowerShell에서 `msgfmt --version`이 실행되는지 먼저 확인합니다.

게임 데이터 경로는 설치 방식과 운영체제에 따라 다릅니다. 가능하면
터미널에서 다음 명령으로 Wesnoth가 사용하는 데이터 경로를 확인합니다.

```sh
wesnoth --path
```

명령을 찾을 수 없으면 게임 설치 폴더에서 `translations` 디렉터리를
검색합니다. 최종 번역 파일 경로는 데이터 경로 아래의 다음 구조입니다.

```text
<Wesnoth 데이터 경로>/translations/ko/LC_MESSAGES/
```

### 2. PO를 MO로 변환

프로젝트 루트에서 실행합니다.

```sh
tools/build_mo.sh
```

이 스크립트는 `work/<버전>/ko/*.po`를 검사하고
`dist/<버전>-<최종수정일>/ko/LC_MESSAGES/`에 MO를 생성합니다. 버전과 출력 경로를
바꾸려면 `tools/build_mo.sh <버전> /path/to/output`처럼 실행합니다.
`msgfmt --check`가 실패하면 MO를 설치하지 말고 해당 PO의 문법과
placeholder를 먼저 수정합니다. 생성되는 파일명은 `wesnoth-ko.po`에서
`wesnoth.mo`처럼 마지막 `-ko`를 제거한 textdomain 이름이어야 합니다.
즉 PO 파일명은 번역 작업용 이름이고, 게임은 같은 basename의 `.mo`를
`translations/ko/LC_MESSAGES/`에서 읽습니다. 설치 스크립트는 대상 경로의
기존 `*.mo`를 모두 제거한 뒤 새 MO 전체를 복사해 동기화합니다. 따라서
삭제되거나 이름이 바뀐 textdomain의 찌꺼기가 남지 않습니다. 다른 확장자의
파일은 건드리지 않습니다. 문제가 생기면 `po/<버전>/ko/`의 원본 PO 또는
`work/<버전>/ko/`의 작업 PO에서 MO를 다시 생성합니다. 빌드가 끝나면
`dist/<버전>-<최종수정일>/ko/PO_LAST_MODIFIED_DATE`에 전체 작업 PO 중 가장 최근
수정 시각(`YYYY-MM-DD HH:MM:SS+0900`)이 기록됩니다. 언어 목록의 작업 표식과
배포 경로는 이 값의 날짜 부분만 사용하므로 `한국어 (<작업버전>-<최종수정일>)`
형식으로 실제 번역 자료의 세대를 식별할 수 있습니다. 재현 가능한 시각이
필요하면 `WESNOTH_PO_TIMESTAMP="YYYY-MM-DD HH:MM:SS+0900" tools/build_mo.sh`처럼
지정합니다. 날짜만 고정하려면 `WESNOTH_PO_DATE=YYYYMMDD`를 사용할 수 있으며,
이 경우 해당 날짜의 `00:00:00+0900`으로 기록됩니다. 시각은 KST/JST(UTC+9)
기준으로 계산됩니다.

MO와 언어 설정 파일을 배포 ZIP으로 묶으려면 다음처럼 실행합니다.

```sh
tools/build_asset.sh <버전> <최종수정일> /path/to/ko_KR.cfg
```

버전 작업 공간에 포함된 기본 언어 설정 파일
`work/<버전>/ko_KR.cfg`를 사용하려면 세 번째 인자를 생략할 수 있습니다.
다른 설정 파일을 사용해야 할 때만 세 번째 인자 또는
`WESNOTH_KO_CONFIG`를 지정합니다.

예를 들어 현재 작업본은
`tools/build_asset.sh 1.18.x 20260926 /path/to/ko_KR.cfg`로 생성하며,
`dist/1.18.x-20260926/wesnoth-ko-translate-1.18.x-20260926.zip`에
기록됩니다. ZIP 안의 `install.sh`와 `install.bat`은 첫 번째 인자로
게임 루트 또는 macOS 앱의 `Contents/Resources` 경로를 받아 기존 MO 세트를
동기화합니다.

### 배포 ZIP의 내부 구조

번역 ZIP은 게임 설치에 사용할 상대 경로를 유지합니다. `data/`와
`translations/`는 ZIP 최상위의 형제 디렉터리이며,
`translations/`를 `data/` 아래에 넣지 않습니다.

```text
wesnoth-ko-translate-<버전>-<최종수정일>/
├── VERSION
├── README.md
├── INSTALL.md
├── install.sh
├── install.bat
├── data/
│   └── languages/
│       └── ko_KR.cfg
└── translations/
    └── ko/
        └── LC_MESSAGES/
            └── *.mo
```

이 구조는 번역 배포 ZIP의 구조입니다. Windows 게임 설치 폴더 자체에서
사용하는 `data/translations/` 경로와 혼동하지 않습니다.
`data/languages/ko_KR.cfg`는 언어 목록 표시용이고,
`translations/ko/LC_MESSAGES/*.mo`는 실제 번역 바이너리입니다.

### 3. macOS

macOS에서는 원본 서명 앱을 직접 수정하지 않고, standalone 앱의 복사본에
번역을 설치하는 방법을 기본 절차로 사용합니다. 이 프로젝트에서 실제로
확인한 실행 대상은 다음과 같습니다.

```text
~/Applications/Wesnoth-1.18.8-unsigned.app/
```

#### unsigned 앱을 만들거나 갱신하는 경우

스크립트가 대상 앱의 존재 여부를 자동으로 판단합니다. 대상이 없으면
원본 standalone 앱을 복사해 unsigned 앱을 만들고, 대상이 이미 있으면
기존 unsigned 앱의 MO와 `ko_KR.cfg`만 갱신합니다. 두 경우 모두 마지막에
ad-hoc 서명을 다시 생성합니다.

```sh
tools/install_mo_macos_app.sh \
  "$HOME/Downloads/The Battle for Wesnoth.app" \
  "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

```text
Wesnoth-1.18.8-unsigned.app/
└── Contents/Resources/
    ├── data/languages/ko_KR.cfg
    └── translations/ko/LC_MESSAGES/*.mo
```

실행은 다음처럼 합니다. 원본 앱 번들은 수정하지 않습니다.

```sh
open "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

#### 원본 macOS 앱을 수정하지 않는 대안

macOS 앱은 서명된 리소스를 포함하므로 앱 내부의 MO를 바꾸면
“앱이 손상되어 열 수 없습니다” 또는 `sealed resource is missing or invalid`
오류가 발생할 수 있습니다. App Store 앱과 standalone 앱 모두 번들 내부를
수정하지 않습니다. 대신 `--data-dir`로 사용자 소유의 외부 데이터
디렉터리를 지정합니다.

```sh
tools/install_mo_macos_external.sh \
  "$HOME/Downloads/The Battle for Wesnoth.app" \
  "$HOME/Applications/Wesnoth-1.18.8-data"

open "$HOME/Downloads/The Battle for Wesnoth.app" \
  --args "--data-dir=$HOME/Applications/Wesnoth-1.18.8-data"
```

이 스크립트는 앱의 `Contents/Resources`를 외부 데이터 디렉터리에 복사하고
그 안의 `translations/ko/LC_MESSAGES/`에 MO를 설치합니다. 원본 앱과
서명 파일은 변경하지 않습니다.

이 프로젝트에서 실제로 확인한 1.18.x standalone 실행 명령은
다음과 같습니다. 앱을 완전히 종료한 뒤 실행해야 합니다.

```sh
open "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

앱을 외부 데이터 없이 실행해도 즉시 종료되거나 종료 코드 `134`가
나오면 MO 설치 문제가 아닙니다. 먼저 원본 앱의 호환성을 확인하고,
macOS 버전과 Wesnoth 버전에 맞는 다른 공식 빌드 또는 소스 빌드를
사용합니다. 예를 들어 macOS `26.6.2`에서 Wesnoth `1.18.8` standalone
앱은 이 프로젝트에서 데이터 경로와 무관하게 `134`로 종료되는 현상이
관찰되었습니다.

#### 번역 적용 확인용 언어 이름 표시

언어 목록의 `한국어 (Hangugeo)`는 PO 헤더가 아니라 게임 데이터의
`data/languages/ko_KR.cfg`에 있는 locale 메타데이터에서 생성됩니다.
따라서 PO만 바꾸어서는 이 표시를 바꿀 수 없습니다. 외부 데이터 디렉터리
또는 서명을 제거한 standalone 앱 복사본에서 다음처럼 표시용 표식을
추가할 수 있습니다.

```sh
APP="$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
tools/mark_korean_locale.sh \
  "$APP/Contents/Resources/data/languages/ko_KR.cfg"
codesign --force --deep --sign - "$APP"
```

standalone 앱의 `ko_KR.cfg`를 서명한 뒤 수정했다면 반드시 위처럼 다시
ad-hoc 서명해야 합니다. 외부 `--data-dir` 방식에서는 앱 번들을 수정하지
않으므로 재서명이 필요하지 않습니다.

기본적으로 언어 선택 창에 `한국어 (<작업버전>-<최종수정일>)` 형식으로
표시됩니다. `PO_LAST_MODIFIED_DATE`가 있으면 실행일이 아니라 마지막 PO
수정일을 사용합니다. 특정 표식을 사용하려면 두 번째 인자로 지정할 수
있습니다. `mark_korean_locale` 스크립트는 이 프로젝트의 활성 PO가
완료되었다는 기준에 맞춰 locale 블록의 `percent`도 `100`으로 갱신하므로,
실제 설정값은 `percent=100`이 되고, 진행 중 번역 표시 옵션을 켜지 않아도
언어 목록에서 보이게 합니다.
정렬용 `sort_name`은 항상 `Hangugeo`로 유지되며 작업 표식으로 바뀌지
않습니다.

```sh
tools/mark_korean_locale.sh \
  "$HOME/Applications/Wesnoth-1.18.8-data/data/languages/ko_KR.cfg" \
  "1.18.x-20260924"
```

스크립트는
수정 전 `ko_KR.cfg`를 같은 디렉터리에 백업하며, 원본 앱 번들의 파일에는
사용하지 않습니다. 다른 표식을 쓰려면 두 번째 인자를 바꾸거나
`WESNOTH_KO_LOCALE_MARKER` 환경 변수로 지정합니다. 이 표식은 번역
내용을 바꾸지 않고, 현재 수정된 데이터 디렉터리를 식별하기 위한
시각적 확인용입니다.

### 4. Windows

설치 폴더 또는 `wesnoth --path`가 출력한 데이터 경로 아래에서 다음
디렉터리를 찾습니다.

```text
<Wesnoth 데이터 경로>\translations\ko\LC_MESSAGES\
```

일반적인 설치 예시는 다음과 같지만 설치 방식과 설치 위치에 따라
달라질 수 있습니다.

```text
C:\Program Files\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES\
C:\Program Files (x86)\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES\
```

ZIP 압축판은 압축을 푼 폴더가 곧 게임 폴더입니다. 예를 들어 압축을
`C:\Games\Wesnoth-1.18`에 풀었다면 대상 경로는
다음과 같습니다.

```text
C:\Games\Wesnoth-1.18\data\translations\ko\LC_MESSAGES\
```

프로젝트의 배치 스크립트는 기존 `*.mo`를 별도 백업하지 않고 삭제한 뒤
새 MO 전체를 복사합니다. 문제가 생기면 아래 복구 절차를 사용합니다.

PowerShell 또는 명령 프롬프트에서 MO를 생성합니다.

```bat
call tools\build_mo.bat
```

생성된 MO를 게임에 적용합니다. 대상 경로를 인자로 명시해야 합니다.

```bat
call tools\install_mo.bat "C:\Program Files\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES"
```

스크립트는 기존 `*.mo`를 삭제한 뒤 새 MO 전체를 복사합니다.
`Program Files` 아래에 설치되어 있으면 관리자 권한이 필요할 수 있습니다.

압축판의 언어 목록에 작업 버전을 표시하려면 `data\languages\ko_KR.cfg`도
다음처럼 수정합니다. 이 스크립트는 `PO_LAST_MODIFIED_DATE`를 사용해
`한국어 (<작업버전>-<최종수정일>)`을 기록하고 원본 설정 파일을 백업합니다.

```bat
call tools\mark_korean_locale.bat "C:\Games\Wesnoth-1.18\data\languages\ko_KR.cfg"
```

이후 게임을 완전히 종료하고 다시 실행한 뒤 언어 선택 창에서
`한국어 (1.18.x-<최종수정일>)`를 선택합니다.
`percent=100`으로 갱신하므로 보통 **Show in-progress or abandoned
translations** 옵션을 체크할 필요가 없습니다. 목록에 표시되지 않을 때만
해당 옵션을 체크합니다. 기존 표시로 되돌리려면 같은 디렉터리에 생성된
`ko_KR.cfg.backup-YYYYMMDD-HHMMSS`를 복원합니다.

### 5. Linux

먼저 다음 명령으로 실제 데이터 경로를 확인합니다.

```sh
wesnoth --path
```

배포판 패키지에서는 다음과 같은 경로가 흔하지만, 고정 경로로 가정하지
말고 `wesnoth --path` 결과를 우선합니다.

```text
/usr/share/games/wesnoth/translations/ko/LC_MESSAGES/
/usr/share/wesnoth/translations/ko/LC_MESSAGES/
/usr/local/share/wesnoth/translations/ko/LC_MESSAGES/
```

생성 및 설치를 다음처럼 실행합니다. 시스템 경로에 쓰려면 관리자 권한이
필요할 수 있습니다.

```sh
tools/build_mo.sh
sudo tools/install_mo.sh \
  "$(wesnoth --path)/translations/ko/LC_MESSAGES"
```

### 6. 확인 및 문제 해결

1. 게임을 완전히 종료한 뒤 다시 실행합니다.
2. 메인 화면 우측 하단의 **언어 설정**을 선택한 뒤 **언어 선택**을
   선택합니다.
3. 목록에서 **한국어 (1.18.x-<최종수정일>)**를 선택하고
   게임을 재시작합니다.
4. 번역이 보이지 않으면 좌측 하단의 **Show in-progress or abandoned
   translations**를 체크한 뒤 다시 확인합니다. 게임 버전이
   1.18.x인지, MO 파일명이
   `wesnoth*.mo` textdomain 이름과 일치하는지 확인합니다.
5. 문제가 생기면 `po/1.18.x/ko/` 또는
   `work/1.18.x/ko/`의 PO를 기준으로
   `tools/build_mo.sh` 또는 `tools\build_mo.bat`를 다시 실행한 뒤,
   올바른 게임 데이터 경로에 재설치합니다.
6. 여러 Wesnoth 설치본이 있으면 실행 중인 게임의 데이터 경로에 복사했는지
   확인합니다.

게임에 설치하는 파일은 `.mo`이며, `.po`는 번역 작업과 검토를 위한
원본입니다. PO를 게임 디렉터리에 그대로 복사해도 번역이 적용되지
않습니다.

### 7. 배포 전 감사

MO를 실제 게임에 설치하거나 완료 tag를 만들기 전에 프로젝트 루트에서
다음 검사를 실행합니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
python3 -m unittest discover -s tests -v
python3 tools/audit_glossary.py
python3 tools/audit_and_pair_embedded_names.py --check
python3 tools/audit_po_completion.py
python3 tools/audit_po_structure.py
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
find "work/$VERSION/ko" -name '*.po' -print0 |
  xargs -0 -n1 msgfmt --check --output-file=/dev/null
```

첫 번째 `msgid ""` 헤더와 `#~` obsolete 항목은 활성 진행률에서 제외합니다.
활성 `#, fuzzy`, 비-fuzzy 빈 `msgstr`, 복수형의 빈 `msgstr[n]`은 실패로
판정합니다. `msgfmt --check`가 종료 코드 0을 반환하면 PO 문법은
통과한 것이며, `Language`나 `Project-Id-Version`의 기본값 경고는 별도로
기록하고 배포 전에 헤더를 검토합니다. 구조 감사의 정상 결과는
`markup_mismatches=0`, `placeholder_mismatches=0`입니다.

### 8. 공개 저장소와 참고 자료

공개 저장소에는 번역 결과와 재현 가능한 작업 도구를 우선 올립니다.

- 공개 후보: `work/<버전>/ko/`, `work/<버전>/glossary.tsv`,
  `po/<버전>/`, `dist/<버전>-<최종수정일>/`, `tools/`, `tests/`,
  프로젝트 문서
- 기본 제외: `References/wesnothko/`와 그 아래의 네이버 카페 HTML
  보관본
- `References/20250322_wesnoth_한국어번역/`은 공개적으로 공헌된 PO
  자료라도 원저작자와 재배포 조건을 확인한 뒤 공개합니다. 공개되어
  있었다는 사실만으로 재배포 권리가 자동으로 생기는 것은 아닙니다.

카페 자료는 로컬 참고용으로 유지하고, 공개 저장소에는 필요한 사실과
번역 결론만 출처를 표시해 재기록하는 방식을 권장합니다. `.gitignore`는
`References/wesnothko/`를 기본 제외하지만, 이미 추적 중인 파일에는
영향이 없으므로 공개 전에 `git status`와 `git ls-files`로 반드시 확인합니다.

### 9. 1.18.x 완료 태그

모든 활성 fuzzy가 검토되고, 비-fuzzy 빈 번역이 없으며, 테스트·구조
감사·`msgfmt --check`가 통과한 시점에만 완료 태그를 만듭니다.

권장 태그 형식은 `wesnoth-ko-translate-1.18.x-<최종수정일>`입니다.
`<최종수정일>`은 KST/JST 기준 마지막 PO 수정 시각의 날짜 부분(`YYYYMMDD`)이며,
`dist/<버전>-<최종수정일>/ko/PO_LAST_MODIFIED_DATE`의
`YYYY-MM-DD HH:MM:SS+0900` 값에서 읽습니다. 같은 날짜에
수정 릴리스가 필요하면 PO를 다시 빌드해 새 마지막 수정일을 반영합니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
PO_TIMESTAMP="$(tr -d '\r\n' < "dist/${VERSION}-"*/ko/PO_LAST_MODIFIED_DATE)"
LAST_MODIFIED_DATE="$(printf '%s' "$PO_TIMESTAMP" | cut -c1-10 | tr -d '-')"
TAG="wesnoth-ko-translate-${VERSION}-${LAST_MODIFIED_DATE}"

git add README.md INSTALL.md PROJECT-AI.md .gitignore \
    References/20250322_wesnoth_한국어번역 po work tools tests
git commit -m "Complete Wesnoth 1.18.x Korean translation"
git tag -a "$TAG" -m "Wesnoth ${VERSION} Korean translation ${LAST_MODIFIED_DATE}"
git push origin main
git push origin "$TAG"
```

카페 HTML을 공개하지 않을 경우 위 `git add` 명령에
`References/wesnothko`를 포함하지 않습니다. 태그를 만들기 전에는
`git diff --cached`, `git status`, 공개 대상 파일 목록을 검토합니다.

## English

This document explains how to apply the Wesnoth 1.18.x Korean PO files to
the actual game. Wesnoth loads gettext binary `.mo` files at runtime, not
the editable `.po` files.

### 1. Prerequisites

You need:

- GNU gettext's `msgfmt`
- An installed Wesnoth 1.18.x copy
- This repository

Install gettext if `msgfmt` is unavailable:

```sh
# macOS (Homebrew)
brew install gettext

# Debian/Ubuntu
sudo apt install gettext

# Fedora
sudo dnf install gettext
```

On Windows, use an MSYS2 environment containing gettext or WSL, then verify
that `msgfmt --version` works in the shell used for conversion.

The data directory depends on the operating system and distribution method.
If available, use the following command first:

```sh
wesnoth --path
```

The final installation directory is:

```text
<Wesnoth data directory>/translations/ko/LC_MESSAGES/
```

### 2. Convert PO to MO

Run this from the repository root:

```sh
tools/build_mo.sh
```

The script validates `work/<version>/ko/*.po` and writes MO files to
`dist/<version>-<last-modified-date>/ko/LC_MESSAGES/`. Pass a version and output directory to
override the defaults, for example `tools/build_mo.sh <version> /tmp/mo`.
The `--check` option validates each PO while producing the MO. The generated
file removes the final `-ko` from the PO filename: for example,
`wesnoth-ko.po` becomes `wesnoth.mo`.
The PO basename is the work-file name; the game loads the corresponding MO
from `translations/ko/LC_MESSAGES/`. Back up existing MO files before
overwriting them. Each build records the latest PO modification timestamp as
`dist/<version>-<last-modified-date>/ko/PO_LAST_MODIFIED_DATE` in
`YYYY-MM-DD HH:MM:SS+0900` form. The directory name and language-list marker use
only its date portion, producing `한국어 (<work-version>-<last-modified-date>)`.
Set `WESNOTH_PO_TIMESTAMP="YYYY-MM-DD HH:MM:SS+0900"` when a reproducible
timestamp is required. `WESNOTH_PO_DATE=YYYYMMDD` remains available and records
midnight at `+0900`. Dates and timestamps are calculated in KST/JST (UTC+9).

### Translation ZIP layout

The translation ZIP preserves game-relative paths. `data/` and
`translations/` are sibling directories directly below the ZIP root;
`translations/` must not be nested under `data/`.

```text
wesnoth-ko-translate-<version>-<last-modified-date>/
├── VERSION
├── README.md
├── INSTALL.md
├── install_mo.sh
├── install_mo.bat
├── data/
│   └── languages/
│       └── ko_KR.cfg
└── translations/
    └── ko/
        └── LC_MESSAGES/
            └── *.mo
```

This is the translation ZIP layout, not the installed Windows game's
`data/translations/` layout. The included `ko_KR.cfg` controls the language
list label; the `.mo` files under `translations/ko/LC_MESSAGES/` contain the
translated messages.

### 3. macOS

On macOS, the default procedure is to install the translation into a copy of
the standalone app rather than modifying the original signed app. The verified
target for this project is:

```text
~/Applications/Wesnoth-1.18.8-unsigned.app/
```

#### Creating or updating the unsigned app

The script checks whether the target app already exists. If it does not, the
script copies the original standalone app and creates the unsigned app. If it
does, it updates only the existing unsigned app's MO files and `ko_KR.cfg`.
Both paths recreate the local ad-hoc signature.

```sh
tools/install_mo_macos_app.sh \
  "$HOME/Downloads/The Battle for Wesnoth.app" \
  "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

```text
Wesnoth-1.18.8-unsigned.app/
└── Contents/Resources/
    ├── data/languages/ko_KR.cfg
    └── translations/ko/LC_MESSAGES/*.mo
```

Launch it with:

```sh
open "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

Do not modify the original app bundle.

#### Alternative that preserves the original macOS app

If the original app must not be modified at all, use Wesnoth's `--data-dir`
option with a writable external data directory:

```sh
tools/install_mo_macos_external.sh \
  "$HOME/Downloads/The Battle for Wesnoth.app" \
  "$HOME/Applications/Wesnoth-1.18.8-data"

open "$HOME/Downloads/The Battle for Wesnoth.app" \
  --args "--data-dir=$HOME/Applications/Wesnoth-1.18.8-data"
```

The helper copies `Contents/Resources` outside the application and installs MO
files under its `translations/ko/LC_MESSAGES/` directory. The original app
and its signing files remain unchanged.

#### Marking the language name for visual verification

The `한국어 (Hangugeo)` label is generated from the locale metadata in
`data/languages/ko_KR.cfg`, not from the PO header. Therefore, changing a PO
file alone does not change this label. On an external data directory or a
standalone app copy with its signature removed, run:

```sh
tools/mark_korean_locale.sh \
  "$HOME/Applications/Wesnoth-1.18.8-data/data/languages/ko_KR.cfg"
```

By default, the language list shows `한국어 (<작업버전>-<최종수정일>)`. When
`PO_LAST_MODIFIED_DATE` exists, the helper uses the latest PO modification
date rather than the script execution date. Pass a second argument to use a
specific marker. The `mark_korean_locale` helpers also set the locale block's
`percent` value to `100`, so the language is visible without enabling the
in-progress or abandoned translations filter.
The sorting field `sort_name` remains the fixed value `Hangugeo` and is not
changed to the work marker.
The helper
creates a backup beside the configuration file and must not be used on the
original signed application bundle. This marker changes no translation text;
it only identifies the modified data directory visually.

If you modify `ko_KR.cfg` inside a standalone app copy after it was signed,
sign the copy again before launching it:

```sh
APP="$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
codesign --force --deep --sign - "$APP"
```

The verified standalone launch command for this project is:

```sh
open "$HOME/Applications/Wesnoth-1.18.8-unsigned.app"
```

If the app exits immediately even with its original data directory, or exits
with code `134`, the MO installation is not the cause. Check compatibility
between the macOS and Wesnoth versions and use another official build or a
source build when necessary. In this project, the Wesnoth `1.18.8` standalone
app was observed to exit with code `134` on macOS `26.6.2` regardless of the
data directory.

### 4. Windows

Find the installation data directory or use the output of `wesnoth --path`.
The translation directory is:

```text
<Wesnoth data directory>\translations\ko\LC_MESSAGES\
```

Common examples include:

```text
C:\Program Files\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES\
C:\Program Files (x86)\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES\
```

Build and install with the Windows helpers:

```bat
call tools\build_mo.bat
call tools\install_mo.bat "C:\Program Files\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES"
```

For the ZIP distribution, the extracted directory is the game directory
itself. For example, if it was extracted to
`C:\Games\Wesnoth-1.18`, use:

```bat
call tools\install_mo.bat "C:\Games\Wesnoth-1.18\data\translations\ko\LC_MESSAGES"
call tools\mark_korean_locale.bat "C:\Games\Wesnoth-1.18\data\languages\ko_KR.cfg"
```

The first helper overwrites existing MO files without creating a backup. The
second helper backs up `ko_KR.cfg` and writes the language label as
`한국어 (<work-version>-<last-modified-date>)`, using `PO_LAST_MODIFIED_DATE`.

The install helper overwrites existing MO files without creating a backup.
If a translation problem appears, rebuild the MO files from
`po/<version>/ko/` or `work/<version>/ko/` and install them again. Windows
may request administrator permission under `Program Files`.

### 5. Linux

Use `wesnoth --path` to find the actual data directory. Common package or
source-install locations include:

```text
/usr/share/games/wesnoth/translations/ko/LC_MESSAGES/
/usr/share/wesnoth/translations/ko/LC_MESSAGES/
/usr/local/share/wesnoth/translations/ko/LC_MESSAGES/
```

Build and install with the shell helpers. A system installation may require:

```sh
tools/build_mo.sh
sudo tools/install_mo.sh \
  "$(wesnoth --path)/translations/ko/LC_MESSAGES"
```

### 6. Verification and troubleshooting

1. Exit the game completely and restart it.
2. On the main screen, select **언어 설정** at the bottom right, then select
   **언어 선택**.
3. Select **한국어 (1.18.x-<last-modified-date>)** and restart the
   game.
4. If it is not listed, enable **Show in-progress or abandoned
   translations** at the bottom left and check again. Verify that the game is
   1.18.x and that the MO filenames match the `wesnoth*.mo`
   textdomains.
5. Restore the backed-up MO files to undo the change.
6. If multiple Wesnoth copies are installed, verify that the files were
   copied into the data directory used by the running executable.

The game uses `.mo` files. Copying `.po` files into the game directory does
not apply the translation.

### 7. Pre-release audit

Before installing MO files into the game or creating the completion tag, run
the following from the repository root:

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
python3 -m unittest discover -s tests -v
python3 tools/audit_glossary.py
python3 tools/audit_and_pair_embedded_names.py --check
python3 tools/audit_po_completion.py
python3 tools/audit_po_structure.py
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
find "work/$VERSION/ko" -name '*.po' -print0 |
  xargs -0 -n1 msgfmt --check --output-file=/dev/null
```

Exclude the first `msgid ""` header and `#~` obsolete entries from active
progress counts. Any active `#, fuzzy`, non-fuzzy empty `msgstr`, or empty
plural `msgstr[n]` is a failure. An exit code of zero from `msgfmt --check`
means the PO syntax passed; header-default warnings such as `Language` or
`Project-Id-Version` are reported separately and should be reviewed before
release. The structural audit must report
`markup_mismatches=0` and `placeholder_mismatches=0`.

### 8. Public repository and references

Publish the translation result and reproducible tooling first:

- Public candidates: `work/<version>/ko/`, `work/<version>/glossary.tsv`,
  `po/<version>/`, `tools/`, `tests/`, and project documentation
- Exclude by default: `References/wesnothko/` and its copied Naver Cafe HTML
  archive
- Before publishing `References/20250322_wesnoth_한국어번역/`, verify the
  contributors' licensing and redistribution conditions. Public availability
  alone does not automatically grant redistribution rights.

Keep the Cafe archive local and record only the necessary conclusions with
source attribution in the public repository. Versioned `dist/<version>-<last-modified-date>/`
MO files and metadata are published. The
`.gitignore` excludes `References/wesnothko/` by default, but inspect
`git status` and `git ls-files` before publishing.

### 9. Completion tag for 1.18.x

Create the completion tag only after all active fuzzy entries have been
reviewed, no non-fuzzy empty translations remain, and the tests, structural
audit, and `msgfmt --check` all pass.

The recommended tag format is `wesnoth-ko-translate-1.18.x-<last-modified-date>`.
`<last-modified-date>` is the date portion (`YYYYMMDD`) of the latest PO
modification timestamp in KST/JST and is read from
`dist/<version>-<last-modified-date>/ko/PO_LAST_MODIFIED_DATE`. For a correction
on the same date, rebuild from the updated PO files so the latest modification
timestamp is reflected.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
PO_TIMESTAMP="$(tr -d '\r\n' < "dist/${VERSION}-"*/ko/PO_LAST_MODIFIED_DATE)"
LAST_MODIFIED_DATE="$(printf '%s' "$PO_TIMESTAMP" | cut -c1-10 | tr -d '-')"
TAG="wesnoth-ko-translate-${VERSION}-${LAST_MODIFIED_DATE}"

git add README.md INSTALL.md PROJECT-AI.md .gitignore \
    References/20250322_wesnoth_한국어번역 po work tools tests
git commit -m "Complete Wesnoth 1.18.x Korean translation"
git tag -a "$TAG" -m "Wesnoth ${VERSION} Korean translation ${LAST_MODIFIED_DATE}"
git push origin main
git push origin "$TAG"
```

Do not include `References/wesnothko` in `git add` if the Cafe archive is to
remain private. Review `git diff --cached`, `git status`, and the final public
file list before creating or pushing the tag.
