#!/usr/bin/env bash
# 安装 major-learning-coach 到 Claude Code / DeepSeek Harness 的技能目录。
#
#   ./install.sh                      # 两个都装
#   ./install.sh --target dsh         # 只装到 ~/.agents/skills
#   ./install.sh --dest /opt/skills   # 装到指定目录
#   ./install.sh --force              # 不备份，直接覆盖
set -euo pipefail

TARGET="both"
DEST=""
FORCE=0
STAMP="$(date +%Y%m%d-%H%M%S)"

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --dest)   DEST="${2:-}";   shift 2 ;;
    --force)  FORCE=1;         shift ;;
    -h|--help)
      sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/skills/major-learning-coach"

if [ ! -d "$SRC" ]; then
  echo "找不到技能源目录：$SRC（请在仓库根目录运行）" >&2
  exit 1
fi

DESTINATIONS=()
if [ -n "$DEST" ]; then
  DESTINATIONS+=("$DEST")
else
  case "$TARGET" in
    dsh|both)    DESTINATIONS+=("$HOME/.agents/skills") ;;
  esac
  case "$TARGET" in
    claude|both) DESTINATIONS+=("$HOME/.claude/skills") ;;
  esac
fi

for base in "${DESTINATIONS[@]}"; do
  mkdir -p "$base"
  dst="$base/major-learning-coach"
  if [ -e "$dst" ]; then
    if [ "$FORCE" -eq 0 ]; then
      cp -R "$dst" "$dst.bak.$STAMP"
      echo "已备份旧版本 -> $dst.bak.$STAMP"
    fi
    rm -rf "$dst"
  fi
  cp -R "$SRC" "$dst"
  count=$(find "$dst/majors" -mindepth 1 -maxdepth 1 -type d ! -name '_*' | wc -l | tr -d ' ')
  echo "已安装 -> $dst（$count 个专业）"
done

echo
echo "下一步：新开一个会话，说「我是计科的，想系统学一遍」，或「这道题怎么做：...」。"
echo "若技能没被触发，确认目标目录在客户端的 skills 搜索路径内，然后重启会话。"
