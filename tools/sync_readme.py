#!/usr/bin/env python3
"""根据 references/major-index.md 重建 README 里的专业表。

用法：
    python tools/sync_readme.py          # 写入 README.md
    python tools/sync_readme.py --check  # 只检查是否已同步（CI 用），不同步则退出码 1
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "skills/major-learning-coach/references/major-index.md"
README = ROOT / "README.md"

BEGIN = "<!-- BEGIN:MAJORS -->"
END = "<!-- END:MAJORS -->"
ROW = re.compile(r"^\|\s*\d+\s*\|")


def parse_index() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if line.startswith("| # |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table:
            if not ROW.match(line):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 7:
                continue
            rows.append(
                {
                    "no": cells[0],
                    "group": cells[1],
                    "name": cells[2],
                    "slug": cells[3].strip("`"),
                    "courses": cells[4],
                    "summary": cells[5],
                }
            )
    return rows


def build_table(rows: list[dict[str, str]]) -> str:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row["group"], []).append(row)

    out: list[str] = []
    for group, items in groups.items():
        out.append(f"### {group}（{len(items)}）")
        out.append("")
        out.append("| 专业 | 这个专业在训练什么 | 核心课 |")
        out.append("|------|--------------------|--------|")
        for it in items:
            link = f"[{it['name']}](skills/major-learning-coach/majors/{it['slug']}/)"
            out.append(f"| {link} | {it['summary']} | {it['courses']} |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    check_only = "--check" in sys.argv
    rows = parse_index()
    if not rows:
        print("ERROR 从 major-index.md 解析不到专业表")
        return 1

    table = build_table(rows)
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"ERROR README.md 缺少标记 {BEGIN} / {END}")
        return 1

    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{BEGIN}\n{table}{END}{tail}"

    if new == text:
        print(f"已是最新：{len(rows)} 个专业")
        return 0

    if check_only:
        print(f"README 专业表未同步（索引 {len(rows)} 个专业），请运行 python tools/sync_readme.py")
        return 1

    README.write_text(new, encoding="utf-8")
    print(f"已更新 README 专业表：{len(rows)} 个专业，{len({r['group'] for r in rows})} 个门类")
    return 0


if __name__ == "__main__":
    sys.exit(main())
