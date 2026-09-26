# 2026-09-26 Knight의 Defense Cap 의미 확인

## 확인 대상

게임의 Knight 유닛 설명에 `Defense`와 `Defense Cap`이 함께 표시되는
이유를 1.18.8의 실제 설정과 도움말에서 확인했다.

## 확인 결과

- Knight는 `movement_type=mounted`를 사용한다.
- `mounted` 이동형은 내부적으로 숲의 방어값을 70, 언덕의 방어값을
  60으로 가진다. 게임 화면의 방어율로는 각각 30%와 40%에 해당한다.
- `Defense Cap`은 특정 기본 지형이 포함된 혼합 지형에서 더 좋은 방어율을
  사용하지 못하게 하는 상한이다.
- 따라서 숲 언덕에서는 언덕의 40%가 아니라 숲의 방어율 30%가 적용된다.

## 번역 결정

`Defense`는 공격력과 달리 지형별 백분율로 표시되는 수치이므로 수치
문맥에서는 `방어율`로 번역한다. `Defense Cap`은 `Defense`와 구분되는
그 방어율의 상한이므로 `방어율 상한`으로 번역한다.

근거 파일:

- `data/core/units/humans/Horse_Knight.cfg`
- `data/core/units.cfg`의 `mounted` 이동형
- `data/core/help.cfg`의 `Defense Caps` 설명
