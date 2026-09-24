# Wesnoth 1.18.x PO Snapshot

이 디렉터리는 Wesnoth Stable 1.18.x의 PO 파일을 원본 상태로 보관하는
로컬 스냅샷입니다. 번역 작업을 위해 이 디렉터리의 PO 파일을 직접
수정하지 않습니다. 실제 작업 파일은 `work/1.18.x/ko/`에 둡니다.

## 디렉터리와 실제 locale

| 디렉터리 | 실제 locale | 내용 |
| --- | --- | --- |
| `ko/` | `ko` | Stable 1.18 GitHub 한국어 PO 원본 |
| `ja/` | `ja` | Stable 1.18 일본어 PO |
| `zh_CN/` | `zh_CN` | Stable 1.18 중국어 PO |
| `en_GB/` | `en_GB` | Stable 1.18 영어 원문 PO |

폴더 이름은 Wesnoth에서 사용하는 실제 locale 식별자와 일치시킵니다.

## 출처

- 번역 통계: <https://gettext.wesnoth.org>
- 원본 PO 경로: <https://github.com/wesnoth/wesnoth/tree/1.18/po>
- 기준 버전: `1.18`
- 다운로드 확인일: 2026-09-24

## 예외

최신 한국어 자료에는 `wesnoth-tdg-ko.po`가 포함되어 있지만, Stable 1.18
원본의 `wesnoth-tdg`에는 `ja`, `zh_CN`, `en_GB` PO가 존재하지 않아
해당 세 locale 디렉터리에는 넣지 않았습니다.

모든 PO 파일은 Wesnoth GitHub `1.18` 브랜치에서 받은 원본 스냅샷입니다.
번역 작업은 `work/1.18.x/ko/`에서 수행합니다.
