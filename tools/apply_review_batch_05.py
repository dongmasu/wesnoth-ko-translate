#!/usr/bin/env python3
"""Apply the reviewed Arcanclave Citadel prose and name spellings."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.merge_reference_translations import parse_field_values, replace_msgstr_fields
from tools.project_config import WORK_KO


def apply_file(path: Path) -> int:
    blocks = path.read_text(encoding="utf-8").split("\n\n")
    changed = 0
    output: list[str] = []
    for block in blocks:
        values = parse_field_values(block)
        source = values.get("msgid", "")
        translation: str | None = None
        if source == "2p — Arcanclave Citadel":
            translation = "2p — 아르칸클레이브(Arcanclave) 요새"
        elif source.startswith("Long ago, countless centuries before the time of Haldric,"):
            translation = (
                "아주 오래전, 할드릭(Haldric)의 시대보다 수없이 많은 세기 전, "
                "린타니르(Lintanir) 숲의 가장 동쪽 끝 너머 먼 곳에서 위대하고 "
                "끔찍한 전쟁이 벌어졌습니다. 기록에 따르면 강력한 전투 마법사이자 "
                "뛰어난 전술가이며 비전 마법의 실천가인 인물이 있었고, 추종자들은 "
                "그에게 무적자라는 칭호를 붙였습니다. 아르칸클레이브(Arcanclave) "
                "전투에서 무적자와 그의 군대는 카 루크(Kah Ruuk)라고 알려진 "
                "잔혹한 마법사 악마 종족과 싸웠습니다. 수만 명의 카 루크(Kah Ruuk)에게 "
                "포위된 무적자는 강력한 대지 정령을 소환했습니다. 알 수 없는 "
                "이유로 그 정령은 무적자에게 감사의 빚을 지고 있었습니다. 정령은 "
                "땅 깊은 곳에서 거대한 바위를 들어 올려 눈 깜짝할 사이에 거대한 "
                "요새의 성벽과 방벽으로 만들었습니다. 수천 명의 카 루크(Kah Ruuk)가 "
                "아르칸클레이브(Arcanclave) 요새를 함락하려다 목숨을 잃었고, 그날 "
                "무적자와 그의 병사들이 승리했습니다. 천 년이 넘게 지난 뒤, 전사 "
                "여왕 신사운(Cynsaun) 1세는 아르칸클레이브(Arcanclave) 요새의 "
                "폐허에서 강령술사 부족을 몰아냈고, 그 후 몇 년에 걸쳐 이 지역을 "
                "군사 요새로 바꾸었습니다. 위대한 마법사 무적자의 통치기에 남겨진 "
                "강력한 유물 몇 점이 아직도 아르칸클레이브(Arcanclave) 요새의 "
                "화강암과 흑요석 성벽 어딘가에 숨겨진 채 잊혀 있다는 소문이 있습니다. "
                "닥 패터슨(Doc Paterson) 제작."
            )
        if translation is not None:
            updated = replace_msgstr_fields(block, {"msgstr": translation})
            if updated != block:
                block = updated
                changed += 1
        output.append(block)
    if changed:
        path.write_text("\n\n".join(output), encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=WORK_KO)
    args = parser.parse_args()
    total = 0
    for path in sorted(args.work.glob("*.po")):
        changed = apply_file(path)
        if changed:
            print(f"{path.name}: {changed} entries reviewed")
            total += changed
    print(f"total: {total} entries reviewed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
