# 설치 및 적용 안내 / Installation and Usage Guide

이 문서는 `wesnoth-ko-translate`의 Wesnoth 1.18.x 한국어 PO를 실제
게임에 적용하는 방법을 설명합니다. 게임은 실행 시 PO가 아니라 gettext
바이너리 파일인 `.mo`를 읽습니다.

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

이 스크립트는 `work/1.18.x/ko/*.po`를 검사하고
`dist/1.18.x/ko/LC_MESSAGES/`에 MO를 생성합니다. 버전과 출력 경로를
바꾸려면 `tools/build_mo.sh 1.18.x /path/to/output`처럼 실행합니다.
`msgfmt --check`가 실패하면 MO를 설치하지 말고 해당 PO의 문법과
placeholder를 먼저 수정합니다. 생성되는 파일명은 `wesnoth-ko.po`에서
`wesnoth.mo`처럼 마지막 `-ko`를 제거한 textdomain 이름이어야 합니다.
즉 PO 파일명은 번역 작업용 이름이고, 게임은 같은 basename의 `.mo`를
`translations/ko/LC_MESSAGES/`에서 읽습니다. 기존 MO를 덮어쓰기 전에
반드시 별도 디렉터리에 백업합니다.

### 3. macOS

Mac App Store 패키지를 사용하는 경우 Finder에서 앱을 선택하고
**패키지 내용 보기**를 선택합니다. 사용자가 확인한 경로는 다음과
같습니다.

```text
The Battle for Wesnoth.app/
└── Contents/Resources/translations/ko/LC_MESSAGES/
```

`%The Battle for Wesnoth%`는 Finder에서 **응용 프로그램**에 있는
`The Battle for Wesnoth.app`를 뜻합니다. `dist/1.18.x/ko/LC_MESSAGES/*.mo`를
이 디렉터리에 복사합니다. 예를 들어 터미널에서는 다음처럼 백업 후
복사할 수 있습니다.

```sh
tools/install_mo.sh \
  "/Applications/The Battle for Wesnoth.app/Contents/Resources/translations/ko/LC_MESSAGES"
```

대상 경로는 반드시 실제 앱의 경로로 확인합니다. 스크립트는 기존 MO가
있을 때만 `*.backup-YYYYMMDD-HHMMSS` 디렉터리를 만들고 백업한 뒤
복사합니다. 앱
업데이트로 원본 파일이 바뀔 수 있으므로 기존 디렉터리를 먼저 백업하고,
복사 후 게임을 완전히 종료했다가 다시 실행합니다. 앱 패키지가 쓰기
금지 상태이면 관리자 권한이 필요할 수 있습니다.

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

PowerShell 또는 명령 프롬프트에서 MO를 생성합니다.

```bat
call tools\build_mo.bat
```

생성된 MO를 게임에 적용합니다. 대상 경로를 인자로 명시해야 합니다.

```bat
call tools\install_mo.bat "C:\Program Files\Battle for Wesnoth 1.18\data\translations\ko\LC_MESSAGES"
```

스크립트는 기존 MO를 `*.backup-YYYYMMDD-HHMMSS` 디렉터리에 백업합니다.
`Program Files` 아래에 설치되어 있으면 관리자 권한이 필요할 수 있습니다.

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
2. 게임 언어를 한국어로 선택합니다.
3. 번역이 보이지 않으면 게임 버전이 1.18.x인지, MO 파일명이
   `wesnoth*.mo` textdomain 이름과 일치하는지 확인합니다.
4. 기존 MO를 백업했다면 원래 파일을 복원해 변경 전 상태로 되돌릴 수
   있습니다.
5. 여러 Wesnoth 설치본이 있으면 실행 중인 게임의 데이터 경로에 복사했는지
   확인합니다.

게임에 설치하는 파일은 `.mo`이며, `.po`는 번역 작업과 검토를 위한
원본입니다. PO를 게임 디렉터리에 그대로 복사해도 번역이 적용되지
않습니다.

### 7. 배포 전 감사

MO를 실제 게임에 설치하거나 완료 tag를 만들기 전에 프로젝트 루트에서
다음 검사를 실행합니다.

```sh
python3 -m unittest discover -s tests -v
python3 tools/audit_po_completion.py
python3 tools/audit_po_structure.py
for po in work/1.18.x/ko/*.po; do
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
find work/1.18.x/ko -name '*.po' -print0 |
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

- 공개 후보: `work/1.18.x/ko/`, `work/1.18.x/glossary.tsv`,
  `po/1.18.x/`, `tools/`, `tests/`, 프로젝트 문서
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

권장 태그 형식은 `wesnoth-1.18.x-ko.1`입니다. 같은 Wesnoth 버전의
번역 수정 릴리스는 `.2`, `.3`처럼 증가시킵니다.

```sh
git add README.md INSTALL.md PROJECT-AI.md .gitignore \
    References/20250322_wesnoth_한국어번역 po work tools tests
git commit -m "Complete Wesnoth 1.18.x Korean translation"
git tag -a wesnoth-1.18.x-ko.1 \
    -m "Wesnoth 1.18.x Korean translation"
git push origin main
git push origin wesnoth-1.18.x-ko.1
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

The script validates `work/1.18.x/ko/*.po` and writes MO files to
`dist/1.18.x/ko/LC_MESSAGES/`. Pass a version and output directory to
override the defaults, for example `tools/build_mo.sh 1.18.x /tmp/mo`.
The `--check` option validates each PO while producing the MO. The generated
file removes the final `-ko` from the PO filename: for example,
`wesnoth-ko.po` becomes `wesnoth.mo`.
The PO basename is the work-file name; the game loads the corresponding MO
from `translations/ko/LC_MESSAGES/`. Back up existing MO files before
overwriting them.

### 3. macOS

For the Mac App Store package, use Finder's **Show Package Contents** on the
application. The verified path is:

```text
The Battle for Wesnoth.app/Contents/Resources/translations/ko/LC_MESSAGES/
```

Run the install helper after confirming the bundle path:

```sh
tools/install_mo.sh \
  "/Applications/The Battle for Wesnoth.app/Contents/Resources/translations/ko/LC_MESSAGES"
```

The helper backs up existing MO files into a timestamped
`*.backup-YYYYMMDD-HHMMSS` directory before copying. `%The Battle for
Wesnoth%` means the `The Battle for Wesnoth.app` bundle under `/Applications`
when using the default install location. App updates may replace the files.
Administrator permission may be required if the application bundle is not
writable.

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

The install helper backs up existing MO files before copying. Windows may
request administrator permission under `Program Files`.

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
2. Select Korean in the language settings.
3. If the translation does not appear, verify the game is 1.18.x and that
   the MO filenames match the `wesnoth*.mo` textdomains.
4. Restore the backed-up MO files to undo the change.
5. If multiple Wesnoth copies are installed, verify that the files were
   copied into the data directory used by the running executable.

The game uses `.mo` files. Copying `.po` files into the game directory does
not apply the translation.

### 7. Pre-release audit

Before installing MO files into the game or creating the completion tag, run
the following from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/audit_po_completion.py
python3 tools/audit_po_structure.py
for po in work/1.18.x/ko/*.po; do
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
find work/1.18.x/ko -name '*.po' -print0 |
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

- Public candidates: `work/1.18.x/ko/`, `work/1.18.x/glossary.tsv`,
  `po/1.18.x/`, `tools/`, `tests/`, and project documentation
- Exclude by default: `References/wesnothko/` and its copied Naver Cafe HTML
  archive
- Before publishing `References/20250322_wesnoth_한국어번역/`, verify the
  contributors' licensing and redistribution conditions. Public availability
  alone does not automatically grant redistribution rights.

Keep the Cafe archive local and record only the necessary conclusions with
source attribution in the public repository. The `.gitignore` excludes
`References/wesnothko/` by default, but inspect `git status` and
`git ls-files` before publishing.

### 9. Completion tag for 1.18.x

Create the completion tag only after all active fuzzy entries have been
reviewed, no non-fuzzy empty translations remain, and the tests, structural
audit, and `msgfmt --check` all pass.

The recommended tag format is `wesnoth-1.18.x-ko.1`; increment the suffix
for later translation-only corrections.

```sh
git add README.md INSTALL.md PROJECT-AI.md .gitignore \
    References/20250322_wesnoth_한국어번역 po work tools tests
git commit -m "Complete Wesnoth 1.18.x Korean translation"
git tag -a wesnoth-1.18.x-ko.1 \
    -m "Wesnoth 1.18.x Korean translation"
git push origin main
git push origin wesnoth-1.18.x-ko.1
```

Do not include `References/wesnothko` in `git add` if the Cafe archive is to
remain private. Review `git diff --cached`, `git status`, and the final public
file list before creating or pushing the tag.
