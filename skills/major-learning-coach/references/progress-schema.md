# 进度存储（Progress Schema）

> 进度是本技能"越用越顺手"的来源：没有它，用户每次都要重新说一遍专业和水平。
> 全部数据只存在本地，不上传、不联网。

## 1. 目录解析（按优先级）

依次尝试，用第一个**可写**的：

1. `$MAJOR_COACH_HOME`（环境变量，用户显式指定时最优先）
2. `<当前工作目录>/.major-coach/`（项目内带着走，适合学习小组共享一个仓库）
3. `~/.major-coach/`（跨项目全局）

三处都不可写（例如只读沙箱）→ **不要报错**，改为在对话里维护一份精简进度，并在每轮开头复述一行：`当前：计算机科学与技术 / L2 / K03-2`。同时告诉用户一句"这次会话结束进度不会保存，可设置 MAJOR_COACH_HOME 到可写目录"。

目录结构：

```
.major-coach/
├── profile.json          # 全局：学过哪些专业、当前默认专业
└── progress/
    ├── computer-science.json
    └── mathematics.json
```

一个用户可以有多个专业（辅修、转专业、考研跨考）。`profile.json` 里的 `active` 决定默认加载哪个；用户说"我还在学数学"时切过去，不要覆盖。

## 2. `profile.json`

```json
{
  "active": "computer-science",
  "majors": [
    {
      "slug": "computer-science",
      "display": "计算机科学与技术",
      "level": "L2",
      "goal": "考研",
      "diagnosed_at": "2026-10-20",
      "diagnosis_hits": "3/5"
    }
  ],
  "created_at": "2026-10-20",
  "schema_version": 1
}
```

- `level` ∈ `L1 | L2 | L3`，只能由诊断或用户明确指定产生，**不要**因为学得快就自动升档（升档由"连续 3 个点自测全对"触发，并要口头告知用户）。
- `goal` 用固定枚举：`考试 | 绩点 | 项目 | 转专业 | 兴趣 | 科研`。目标影响例题选材，不要省略。
- `diagnosis_hits` 保留原始命中数，方便下次对比"进步了没有"。

## 3. `progress/<slug>.json`

```json
{
  "slug": "computer-science",
  "current": { "module": "K03", "point": "K03-2" },
  "mastered": ["K01-1", "K01-2", "K02-1"],
  "in_progress": ["K03-2"],
  "struggling": [
    { "point": "K02-3", "note": "递归出口写错", "count": 2, "last": "2026-10-20" }
  ],
  "override": [
    { "point": "K05-1", "reason": "前置抽查 3/3 通过", "date": "2026-10-20" }
  ],
  "history": [
    { "date": "2026-10-20", "action": "learn", "point": "K01-1", "result": "ok" },
    { "date": "2026-10-20", "action": "quiz", "point": "K01-2", "result": "fail" }
  ],
  "updated_at": "2026-10-20T20:40:00+08:00"
}
```

字段语义：

| 字段 | 含义 | 谁写 |
|---|---|---|
| `current` | 下一次继续学习的位置 | 每次 `learn` 结束 |
| `mastered` | 自测**通过**的点（按过关标准判） | 用户答对自测后 |
| `in_progress` | 正在学、还没过的点 | 进入 `learn` 时 |
| `struggling` | 错过 ≥1 次的点，`count` 累加 | 答错时 |
| `override` | 跳过前置/调整档位的记录，必须写原因 | 跳级或用户改档时 |
| `history` | 只追加，不改写；每次交互一行 | 每次模式结束 |

`history` 最多保留 200 条，超出时丢最旧的。

## 4. 更新时机（写死，避免"记了但记错"）

| 触发 | 动作 |
|---|---|
| 用户确认诊断结果 | 建 `profile.json` + 建 `<slug>.json`，`current` = 起点 |
| 进入 `learn` | 把该点加入 `in_progress` |
| 自测全对 | 移到 `mastered`，从 `in_progress` 移除，`current` 推进到"下一步"那个点 |
| 自测有错 | 留在 `in_progress`，记 `struggling`（`count += 1`），**不推进** |
| 用户说"懂了/跳过" | 记 `override` + 原因（如"用户自述已学过"），推进 `current` |
| 用户换档位 | 改 `profile.majors[].level`，记 `override` |
| 用户切换专业 | 改 `profile.active`，不动任何 `progress/*.json` |

写入失败（权限、磁盘）→ 不要静默失败，说一句"进度没存上"，然后继续对话。

## 5. 展示给用户

每次读完进度，用一行摘要开头，不要贴 JSON：

```
📌 计算机科学与技术 · L2 进阶 · 当前 K03-2（链表边界处理）· 目标：考研
```

新会话恢复时补一句：`上次停在 K03-1，做过 1 道回炉题（错了），要不要先花 10 分钟补那个点？`

## 6. 容错与迁移

- JSON 解析失败 → 不要覆盖原文件；重命名为 `<slug>.json.broken.<时间戳>`，重建一份空进度，并告诉用户"进度文件损坏，已备份"。
- `schema_version` 升级 → 读旧版时补默认字段，写回时升级版本号；不要丢 `history`。
- 专业 slug 改名属于破坏性变更：若发现 `progress/` 下有未知 slug，提示用户"这个专业已改名"，不要静默删除。
