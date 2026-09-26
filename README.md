# Wesnoth 한국어 번역 프로젝트

## 한국어

이 저장소는 [Battle for Wesnoth](https://github.com/wesnoth/wesnoth)의
한국어 번역을 만들고 유지하기 위한 프로젝트입니다.

현재 Wesnoth 1.18.x 작업용 한국어 PO, 용어집, 설치 안내와 검수
자동화가 마련되어 있습니다. 번역 완료 기준과 실제 게임 적용 절차도
문서화되어 있습니다.

### 버전 설정

현재 작업 버전은 루트의 `VERSION` 파일에 기록합니다. 도구 실행 시
`WESNOTH_VERSION` 환경 변수를 지정하면 해당 버전이 우선됩니다.
따라서 새 버전은 `po/<버전>/`과 `work/<버전>/`을 준비한 뒤 다음처럼
같은 도구를 재사용할 수 있습니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
WESNOTH_VERSION="$VERSION" tools/build_mo.sh
# PO_LAST_MODIFIED_DATE는 마지막 PO 수정 시각이며 언어 목록 식별 표식에 사용됩니다.
WESNOTH_VERSION="$VERSION" python3 tools/audit_po_completion.py
```

문서의 버전 표기는 `docs/templates/*.md.in`에서 관리합니다. 템플릿을
수정한 뒤 `python3 tools/render_docs.py`를 실행하면 이 문서와
`INSTALL.md`, `PROJECT-AI.md`, `work/README.md`가 다시 생성됩니다.
생성 문서의 수동 변경은 다음 렌더링에서 사라지므로 직접 편집하지 않습니다.
GitHub Actions는 변경 시 `render_docs.py --check`로 템플릿과 게시 문서의
일치를 검증하며, 수동 실행에 버전을 입력하면 해당 버전으로 문서를
렌더링해 커밋할 수 있습니다.

### 문서

- [프로젝트 작업 지침](PROJECT-AI.md)
- [설치 안내](INSTALL.md)
- [과거 Wesnoth 한국어화 자료](References/README.md)
- [1.18.x PO 원본과 작업 공간](work/1.18.x/README.md)
- [1.18.x 번역 용어집](work/1.18.x/glossary.tsv)

### 목표

- 게임 내 주요 텍스트의 자연스럽고 일관된 한국어 번역
- 고유명사와 게임 용어의 통일
- 원문 업데이트에 대응할 수 있는 유지보수 가능한 번역 흐름
- 번역자와 검수자가 함께 확인할 수 있는 공개 작업 과정

### 최신 번역 자료

`References/20250322_wesnoth_한국어번역/`에 있는 한국어 `.po` 파일을
현재 구할 수 있는 최신 번역 자료로 간주하며, 새로운 번역과 검토에서
가능한 한 적극적으로 활용합니다. 모든 항목을 그대로 복사하지는 않으며,
현재 영어 원문·게임 문맥·구조적 표식과 충돌하면 근거를 남기고 조정합니다.
영어 원문을 기본 기준으로 삼고, 필요할 때
`gettext.wesnoth.org`의 일본어(`ja`)와 중국어(`zh_CN`) 번역을 보조적으로
비교합니다.

### 번역 대상

번역 대상은 Wesnoth 본편과 필요에 따라 공식 또는 커뮤니티 콘텐츠의
텍스트입니다. 실제 대상 범위와 원본 버전은 번역 작업을 시작할 때
별도로 기록합니다.

### 참여

용어집과 검수 규칙을 먼저 확인한 뒤 번역 제안, 오탈자 수정, 문맥 제보,
검수 의견을 추가합니다.

### 실제 게임 적용과 공개

실제 게임에는 PO가 아니라 `msgfmt`로 생성한 `.mo` 파일을 설치합니다.
Mac App Store, Windows, Linux별 경로와 변환 명령은
[INSTALL.md](INSTALL.md)에 기록되어 있습니다.

번역 배포 ZIP의 최상위에는 `data/`와 `translations/`가 형제 디렉터리로
들어갑니다. 즉 `data/languages/ko_KR.cfg`와
`translations/ko/LC_MESSAGES/*.mo`를 사용하며,
`translations/`를 `data/` 아래에 두지 않습니다.

### MO만 필요한 사용자를 위한 다운로드

컴파일된 번역 파일만 필요한 사용자는 저장소 전체를 내려받지 말고
최신 GitHub Release의 asset ZIP을 받으면 됩니다. 현재 작업 기준 파일명은
`wesnoth-ko-translate-1.18.x-20260926.zip`입니다.

- [GitHub Release: wesnoth-ko-translate-1.18.x-20260926](https://github.com/dongmasu/wesnoth-ko-translate/releases/tag/wesnoth-ko-translate-1.18.x-20260926)
- [ZIP asset 다운로드](https://github.com/dongmasu/wesnoth-ko-translate/releases/download/wesnoth-ko-translate-1.18.x-20260926/wesnoth-ko-translate-1.18.x-20260926.zip)

ZIP에는 MO 파일, `ko_KR.cfg`, 설치 안내와 설치 스크립트가 들어갑니다.
Release asset이 게시된 뒤에는 저장소 전체를 clone하지 않고 위의 ZIP 링크만
다운로드하면 됩니다. asset 이름의 날짜는 MO 생성일이 아니라
`PO_LAST_MODIFIED_DATE`에 기록된 마지막 PO 수정 시각
(`YYYY-MM-DD HH:MM:SS+0900`, KST/JST 기준)의 날짜 부분입니다.

`References/wesnothko/`는 네이버 카페에서 확보한 HTML과 참고 자료를
포함하므로 기본적으로 공개 저장소에서 제외합니다. 공개적으로 공헌된
`References/20250322_wesnoth_한국어번역/`도 원저작자와 재배포 조건을 확인한
뒤 공개합니다. 공개되어 있었다는 사실만으로 재배포 권리가 자동으로
생기는 것은 아닙니다.

1.18.x 번역 완료 시에는 모든 활성 fuzzy와 빈 번역을 제거하고 테스트,
구조 감사, `msgfmt --check`를 통과한 뒤
`wesnoth-ko-translate-1.18.x-<최종수정일>` annotated tag를 만듭니다.
`<최종수정일>`은 KST/JST 기준 마지막 PO 수정 시각
(`YYYY-MM-DD HH:MM:SS+0900`)의 날짜 부분(`YYYYMMDD`)입니다. 태그와 공개 파일
목록을 검토한 뒤에만 GitHub로 push합니다.

### 구조 보존 규칙

- 실제 `\n`과 문단·대사 경계를 원문과 동일하게 유지합니다. PO의 여러
  인용 문자열 줄은 파일 가독성을 위한 분할일 수 있으며 게임 개행과 다릅니다.
- `<i>`, `<b>`, `<span ...>`, `<ref ...>` 같은 Pango/HTML 태그의 이름,
  속성, 짝, 개수를 유지하고 태그 안의 텍스트만 번역합니다.
- `%s`, `%d`, `$unit.name`, `$gold_cost` 같은 placeholder는 철자와
  대소문자를 바꾸거나 삭제·추가하지 않습니다. 한국어 조사는 placeholder
  뒤에 붙이며 이름 안에 포함하지 않습니다.
- 복수형 PO 항목은 `msgid_plural`을 유지하고 `msgstr[n]` 인덱스별로
  번역합니다. 단수형 언어라도 PO의 복수형 구조를 임의로 바꾸지 않습니다.
- `source_term`에 `^`가 있으면 `^` 앞은 gettext 문맥 식별자이고 `^` 뒤가
  실제 표시 문자열입니다. 문맥 식별자는 번역하지 않으며, 용어집의
  `standard_korean`과 PO의 `msgstr`에는 표시 문자열만 기록합니다.
- `^`가 있는 항목은 전체 키를 기준으로 독립적으로 관리합니다. 예를 들어
  `feature^Open`과 `filesystem^Open`은 표시 문자열이 같아도 서로 다른
  문맥이므로 합치지 않습니다.
- `#, fuzzy` 항목은 완료된 번역으로 취급하지 않습니다. 번역을 검토해
  문제가 없을 때만 fuzzy 표시를 제거합니다.
- manpage의 `B<>`, `I<>` 표식, 옵션명, 명령 구문, 파일명, URL, 경로와
  역슬래시는 그대로 유지하고 설명 텍스트만 번역합니다.
- 번역 후 `python3 tools/audit_po_structure.py`와 테스트를 실행합니다.

### 규칙과 예외의 유지보수

번역 중 새로 발견한 규칙, 반복되는 예외, 과거 번역과 현재 원문의 충돌은
개별 작업자의 기억에만 두지 않습니다. `PROJECT-AI.md`에는 모든 도구와
사람에게 적용되는 일반 원칙을, `work/README.md`에는 1.18.x 작업 절차와
판단 기준을, `glossary.tsv`에는 반복 용어의 표준 번역과 근거를 기록합니다.
같은 문제를 자동으로 검출할 수 있으면 `tests/`에도 회귀 테스트를 추가합니다.

기본 규칙과 다른 번역이 필요해 보여도 태그, placeholder, 실제 `\n`, PO
구조를 임의로 바꾸지 않습니다. 원문 오류나 문맥 충돌이 의심되면 우선
`review` 상태와 근거를 남기고 검토 후 확정합니다. 문서·용어집·PO 가운데
하나만 갱신된 상태는 작업 완료로 취급하지 않습니다.

### 문서 기반 감사

다른 검증자는 이전 대화나 작업자의 기억 없이 이 저장소의 문서만 읽고
감사를 재현할 수 있어야 합니다. 감사 대상은 `work/1.18.x/ko/*.po`의
활성 메시지입니다. 첫 번째 `msgid ""` 헤더와 `#~` obsolete 항목은
진행률에서 제외하고, 활성 `#, fuzzy`, 비-fuzzy 빈 `msgstr`, 복수형의 빈
`msgstr[n]`은 미완료로 판정합니다. `msgfmt --check`의 헤더 기본값 경고는
종료 코드가 나타내는 PO 문법 실패와 별도로 기록합니다.

```sh
VERSION="${WESNOTH_VERSION:-$(tr -d '\r\n' < VERSION)}"
python3 -m unittest discover -s tests -v
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

완료 기준은 활성 fuzzy 0, 빈 번역 0, 빈 복수형 0,
`markup_mismatches=0`, `placeholder_mismatches=0`, `newline_mismatches=0`,
용어집-PO 불일치
0건입니다. `glossary.tsv`의 `category`는 gettext `msgctxt`가 아니라
인명·지명·종족명·유닛명·UI·명령어 등 의미상 분류를 나타내며, 용어집에
등록된 항목은 별도 `confirmed` 상태 없이 표준 번역으로 취급합니다.

### 참고 자료

- [Wesnoth 공식 저장소](https://github.com/wesnoth/wesnoth)
- [Units 번역 확인 사이트](https://units.wesnoth.org/)
- [Wesnoth 번역 상태 및 담당자](https://wiki.wesnoth.org/WesnothTranslations)
- [Wesnoth 번역 안내](https://wiki.wesnoth.org/WesnothTranslationsHowTo)
- [Gettext 번역 기술 문서](https://wiki.wesnoth.org/GettextForTranslators)
- [번역 통계 대시보드](https://gettext.wesnoth.org/)
- [Wesnoth 한국어 번역 안내](https://wiki.wesnoth.org/KoreanTranslation)
- [한글화 팀 구성원](https://wiki.wesnoth.org/KoreanTranslation) — 2019년 10월 마지막 업데이트로, 현재 구성원 및 담당 정보와 다를 수 있음
- [과거 Wesnoth 한국어화 자료](References/README.md)
- [과거 Transifex 공동 번역 페이지](https://www.transifex.com/kmshts/battle-for-wesnoth)

## English

This repository is for creating and maintaining a Korean translation of
[The Battle for Wesnoth](https://github.com/wesnoth/wesnoth).

The repository contains the Wesnoth 1.18.x working Korean PO files, glossary,
installation guide, and validation tooling. The completion criteria and
actual game installation procedure are documented as well.

### Documentation

- [Project instructions](PROJECT-AI.md)
- [Installation guide](INSTALL.md)
- [Archived Wesnoth Korean translation references](References/README.md)
- [1.18.x PO snapshot and workspace](work/1.18.x/README.md)
- [1.18.x translation glossary](work/1.18.x/glossary.tsv)

### Goals

- Provide natural and consistent Korean text for the game
- Keep proper names and gameplay terminology consistent
- Maintain a workflow that can follow upstream text changes
- Keep the translation process open to translators and reviewers

### Latest translation references

The Korean `.po` files in `References/20250322_wesnoth_한국어번역/` are
the most important available Korean reference and should be actively reused
when translating or reviewing. They are not copied mechanically in every
case: when they conflict with the current English source, game context, or
structural markup, record the reason and adjust the Korean translation.
English is the primary reference; Japanese (`ja`) and Chinese (`zh_CN`) translations from
`gettext.wesnoth.org` may be consulted as secondary references.

### Translation scope

The scope includes text from the main Wesnoth game and, where appropriate,
official or community content. The exact scope and upstream version will be
recorded when translation work begins.

### Contributing

Check the glossary and validation rules before submitting translation
proposals, typo fixes, context reports, or review feedback.

### Applying and publishing the translation

The game uses `.mo` files generated by `msgfmt`, not the editable PO files.
The conversion commands and platform-specific paths for the Mac App Store,
Windows, and Linux are documented in [INSTALL.md](INSTALL.md).

The translation ZIP keeps `data/` and `translations/` as sibling directories
at its root. It contains `data/languages/ko_KR.cfg` and
`translations/ko/LC_MESSAGES/*.mo`; `translations/` must not be nested under
`data/`.

### MO-only download

Users who only need the compiled translation files can download the latest
GitHub Release asset ZIP instead of cloning the repository. The current asset
name is `wesnoth-ko-translate-1.18.x-20260926.zip`.

- [GitHub Release: wesnoth-ko-translate-1.18.x-20260926](https://github.com/dongmasu/wesnoth-ko-translate/releases/tag/wesnoth-ko-translate-1.18.x-20260926)
- [Download ZIP asset](https://github.com/dongmasu/wesnoth-ko-translate/releases/download/wesnoth-ko-translate-1.18.x-20260926/wesnoth-ko-translate-1.18.x-20260926.zip)

The ZIP contains the MO files, `ko_KR.cfg`, installation instructions, and
installation scripts. Once the Release asset is published, users only need to
download the ZIP above instead of cloning the repository. The date in the asset
name is the latest PO modification date, not the MO build date; it is recorded
in `PO_LAST_MODIFIED_DATE` using KST/JST. The metadata value is recorded as
`YYYY-MM-DD HH:MM:SS+0900`; asset names and tags use only its `YYYYMMDD` date
portion.

`References/wesnothko/` contains copied Naver Cafe HTML and reference
material, so it is excluded from the public repository by default. Even the
publicly contributed `References/20250322_wesnoth_한국어번역/` material should
be published only after checking the contributors' licensing and
redistribution conditions. Public availability alone does not automatically
grant redistribution rights.

When the 1.18.x translation is complete, remove all active fuzzy and empty
translations, pass the tests, structural audit, and `msgfmt --check`, then create
the annotated tag `wesnoth-ko-translate-1.18.x-<last-modified-date>`.
`<last-modified-date>` is the `YYYYMMDD` date portion of the latest PO
modification timestamp in KST/JST. Review
the tag and public file list before pushing to GitHub.

### Structural fidelity

- Preserve literal `\n` characters and paragraph or dialogue boundaries.
  Wrapping a PO value across multiple quoted lines is not a game line break.
- Preserve Pango/HTML tag names, attributes, pairing, and counts, including
  tags such as `<i>`, `<b>`, `<span ...>`, and `<ref ...>`.
- Preserve placeholders such as `%s`, `%d`, `$unit.name`, and `$gold_cost`
  exactly. Korean particles may follow a placeholder but must not become part
  of its name.
- For plural PO entries, preserve `msgid_plural` and translate the indexed
  `msgstr[n]` values without changing the PO structure.
- A `^` in `source_term` separates a gettext context identifier from the
  displayed text. Translate only the displayed part and retain the complete
  key in the glossary's `source_term`. This applies equally to `feature^Open`,
  `female^refreshed`, `male^`, and `race^`: do not display an invented Korean
  context prefix such as `여성^`, `남성^`, or `종족^` in `msgstr`.
- A gender context key does not by itself require a Korean gender prefix.
  Keep Korean gender-neutral job, trait, and ability names identical to their
  base entry. Preserve gender only when the displayed English word itself is
  gendered, such as `Princess`, `Queen`, `Lady`, `Priestess`, `Sorceress`,
  `Baroness`, `Watchwoman`, or a kinship title, and a natural Korean
  counterpart exists. A natural neutral term such as `야경꾼` is preferable to
  an artificial prefix such as `여성 야경꾼`. Record an explicit glossary
  exception when sex is part of an animal or character's displayed identity.
- Manage contextual entries by their complete key. For example,
  `feature^Open` and `filesystem^Open` remain separate entries even though
  their displayed text is the same.
- Treat entries marked `#, fuzzy` as incomplete until reviewed and the fuzzy
  marker is removed.
- In manpage text, preserve `B<>` and `I<>` markup, option names, command
  syntax, filenames, URLs, paths, and backslashes; translate only the prose.
- Run `python3 tools/audit_po_structure.py` and the test suite after changes.

### Maintaining rules and exceptions

New rules, recurring exceptions, and conflicts between historical Korean
translations and current source text must not remain only in an individual
translator's memory. Record general rules in `PROJECT-AI.md`, 1.18.x
workflow decisions in `work/README.md`, and recurring terminology decisions
with decision notes in `glossary.tsv`. Add a regression test under `tests/` when the
same problem can be detected automatically.

Even when a different translation seems necessary, do not arbitrarily change
tags, placeholders, literal `\n`, or PO structure. If an upstream defect or
context conflict is suspected, record the evidence and leave the item in
`review` until it is resolved. A change is not complete if only one of the
documentation, glossary, or PO layers was updated.

### References

- [Official Wesnoth repository](https://github.com/wesnoth/wesnoth)
- [Units translation viewer](https://units.wesnoth.org/)
- [Wesnoth translation status and maintainers](https://wiki.wesnoth.org/WesnothTranslations)
- [Wesnoth translation guide](https://wiki.wesnoth.org/WesnothTranslationsHowTo)
- [Gettext translation technical guide](https://wiki.wesnoth.org/GettextForTranslators)
- [Translation statistics dashboard](https://gettext.wesnoth.org/)
- [Wesnoth Korean translation guide](https://wiki.wesnoth.org/KoreanTranslation)
- [Korean translation team members](https://wiki.wesnoth.org/KoreanTranslation) — last updated in October 2019; the listed members and maintainer information may be outdated
- [Archived Wesnoth Korean translation references](References/README.md)
- [Former Transifex collaborative translation page](https://www.transifex.com/kmshts/battle-for-wesnoth)
