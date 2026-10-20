#!/usr/bin/env python3
"""校验 major-learning-coach 仓库：结构、索引一致性、知识点表、先修图。

用法：
    python tools/validate.py            # 全量校验
    python tools/validate.py --quiet    # 只打印问题

退出码：0 全部通过；1 有错误。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "major-learning-coach"
MAJORS_DIR = SKILL_DIR / "majors"
INDEX_MD = SKILL_DIR / "references" / "major-index.md"
README = ROOT / "README.md"
SKILL_MD = SKILL_DIR / "SKILL.md"

REQUIRED_REFS = [
    "major-index.md",
    "curriculum-rules.md",
    "diagnosis.md",
    "learning-card-template.md",
    "progress-schema.md",
]
REQUIRED_MAJOR_SECTIONS = list(range(1, 10))  # ## 1. ... ## 9.
DIFFS = {"L1", "L2", "L3"}
ROW_RE = re.compile(
    r"^\|\s*(K\d{2}(?:-\d+)?)\s*\|\s*([^|]*?)\s*\|\s*(L[123])\s*\|\s*([^|]*?)\s*\|"
)
ID_RE = re.compile(r"K\d{2}(?:-\d+)?")
NUM_RE = re.compile(r"^\|\s*(\d+)\s*\|")

errors: list[str] = []
warns: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    body = text[3:end]
    data: dict[str, str] = {}
    key = None
    for line in body.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+\S", line) and key:  # 折叠块续行
            data[key] += " " + line.strip()
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2).strip()
    return data


def section_numbers(text: str) -> set[int]:
    found = set()
    for m in re.finditer(r"^##\s*(\d)\.", text, re.MULTILINE):
        found.add(int(m.group(1)))
    return found


def check_skill_md() -> None:
    if not SKILL_MD.exists():
        err("缺少 skills/major-learning-coach/SKILL.md")
        return
    text = read(SKILL_MD)
    lines = text.count("\n") + 1
    if lines > 200:
        err(f"SKILL.md 有 {lines} 行，超过 200 行上限（路由文件必须瘦）")
    fm = parse_frontmatter(text)
    if fm.get("name") != "major-learning-coach":
        err(f"SKILL.md frontmatter name 应为 major-learning-coach，实际 {fm.get('name')!r}")
    desc = fm.get("description", "")
    if len(desc) < 80:
        err(f"SKILL.md description 太短（{len(desc)} 字符），触发会不稳")
    if "major-index.md" not in text:
        err("SKILL.md 没有指向 references/major-index.md")
    for ref in REQUIRED_REFS:
        if not (SKILL_DIR / "references" / ref).exists():
            err(f"缺少 references/{ref}")
    # 路由文件里不应堆具体知识点
    if len(ID_RE.findall(text)) > 3:
        err("SKILL.md 里出现大量知识点 ID，说明内容漏进了路由文件")


def index_slugs() -> list[str]:
    if not INDEX_MD.exists():
        err("缺少 references/major-index.md")
        return []
    slugs = re.findall(r"`([a-z][a-z0-9-]+)`", read(INDEX_MD))
    # 只保留形如专业 slug 的（排除 Kxx 等）
    return sorted({s for s in slugs if not s.startswith("major-")})


def check_index_vs_dirs() -> None:
    if not MAJORS_DIR.exists():
        err("缺少 majors/ 目录")
        return
    dirs = sorted(
        p.name for p in MAJORS_DIR.iterdir() if p.is_dir() and not p.name.startswith("_")
    )
    idx = index_slugs()
    if not idx:
        err("major-index.md 里解析不到任何 slug")
        return
    missing_dirs = sorted(set(idx) - set(dirs))
    orphan_dirs = sorted(set(dirs) - set(idx))
    if missing_dirs:
        err(f"索引里有 {len(missing_dirs)} 个专业没有目录：{', '.join(missing_dirs[:8])}")
    if orphan_dirs:
        err(f"{len(orphan_dirs)} 个专业目录没进索引：{', '.join(orphan_dirs[:8])}")


def check_major(slug: str) -> dict:
    path = MAJORS_DIR / slug / "SKILL.md"
    info = {"slug": slug, "points": 0, "max_depth": 0, "ok": True}
    if not path.exists():
        err(f"[{slug}] 缺少 SKILL.md")
        info["ok"] = False
        return info
    text = read(path)
    lines = text.count("\n") + 1
    if lines > 300:
        err(f"[{slug}] 有 {lines} 行，超过 300 行上限")
    fm = parse_frontmatter(text)
    if fm.get("name") != f"major-{slug}":
        err(f"[{slug}] frontmatter name 应为 major-{slug}，实际 {fm.get('name')!r}")
    if len(fm.get("description", "")) < 60:
        err(f"[{slug}] description 太短")
    secs = section_numbers(text)
    missing = [n for n in REQUIRED_MAJOR_SECTIONS if n not in secs]
    if missing:
        err(f"[{slug}] 缺少章节：{missing}")
    if "过关标准" not in text:
        err(f"[{slug}] 知识点表缺少「过关标准」列")

    rows: dict[str, dict] = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        kid, name, diff, pre = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
        if kid in rows:
            err(f"[{slug}] 知识点 ID 重复：{kid}")
        rows[kid] = {
            "name": name,
            "diff": diff,
            "pre": [p for p in ID_RE.findall(pre) if p != kid],
        }
    info["points"] = len(rows)
    if len(rows) < 20:
        err(f"[{slug}] 知识点只有 {len(rows)} 个，少于 20")
    for kid, row in rows.items():
        if not row["name"]:
            err(f"[{slug}] {kid} 缺少名称")
        for p in row["pre"]:
            if p not in rows:
                err(f"[{slug}] {kid} 的前置 {p} 不在知识点表内")

    # 环检测 + 深度
    state: dict[str, int] = {}

    def dfs(k: str) -> int:
        if state.get(k) == 1:
            err(f"[{slug}] 先修图存在环，涉及 {k}")
            return 0
        if state.get(k) == 2:
            return info.setdefault("_depth", {}).get(k, 1)
        state[k] = 1
        depth = 1
        for p in rows[k]["pre"]:
            if p in rows:
                depth = max(depth, dfs(p) + 1)
        state[k] = 2
        info.setdefault("_depth", {})[k] = depth
        return depth

    sys.setrecursionlimit(10000)
    for k in rows:
        if k not in state:
            info["max_depth"] = max(info["max_depth"], dfs(k))
    if info["max_depth"] < 3:
        warn(f"[{slug}] 先修链最深处只有 {info['max_depth']} 层，坡度可能太平")
    l1_no_pre = [k for k, r in rows.items() if r["diff"] == "L1" and not r["pre"]]
    if not l1_no_pre:
        warn(f"[{slug}] 没有无前置的 L1 入口点，新手不知道从哪开始")
    bad = [
        f"{k}({r['diff']}←{'/'.join(r['pre'])})"
        for k, r in rows.items()
        if any(rows[p]["diff"] > r["diff"] for p in r["pre"] if p in rows)
    ]
    if bad:
        warn(f"[{slug}] 前置难度高于本点（按拓扑序处理即可）：{', '.join(bad[:5])}")
    return info


def check_placeholders() -> None:
    """只扫描技能内容（会被加载进上下文的部分）；docs/ 里讨论占位符规则不算违规。"""
    pat = re.compile(r"\bTODO\b|\bFIXME\b|待补充|待补写|XXX")
    for path in SKILL_DIR.rglob("*.md"):
        for i, line in enumerate(read(path).splitlines(), 1):
            if pat.search(line):
                err(f"{path.relative_to(ROOT)}:{i} 仍有占位内容：{line.strip()[:60]}")


def check_readme(count: int) -> None:
    if not README.exists():
        warn("README.md 还没写，发布前必须补")
        return
    text = read(README)
    rows = re.findall(r"\]\(\.?/?skills/major-learning-coach/majors/([a-z0-9-]+)/", text)
    if len(set(rows)) != count:
        err(f"README 专业表格有 {len(set(rows))} 行，应为 {count} 行")


def check_install_scripts() -> None:
    for name in ("install.ps1", "install.sh"):
        if not (ROOT / name).exists():
            warn(f"缺少 {name}")


def main() -> int:
    quiet = "--quiet" in sys.argv
    check_skill_md()
    check_index_vs_dirs()

    infos = []
    if MAJORS_DIR.exists():
        for d in sorted(MAJORS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                infos.append(check_major(d.name))

    check_placeholders()
    check_readme(len(infos))
    check_install_scripts()

    total_points = sum(i["points"] for i in infos)
    if not quiet:
        print(f"仓库根目录：{ROOT}")
        print(f"专业数：{len(infos)}   知识点总数：{total_points}")
        print(f"知识点最多的专业：{max(infos, key=lambda i: i['points'])['slug'] if infos else '-'}")
        deep = [i for i in infos if i["max_depth"] >= 4]
        print(f"先修链 ≥4 层的专业：{len(deep)}/{len(infos)}")
        print("-" * 60)

    for w in warns:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    if errors:
        print(f"\n失败：{len(errors)} 个错误，{len(warns)} 个警告")
        return 1
    print(f"\n通过：{len(infos)} 个专业，{total_points} 个知识点，{len(warns)} 个警告")
    return 0


if __name__ == "__main__":
    sys.exit(main())
