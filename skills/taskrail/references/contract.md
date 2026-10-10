# taskrail 契约（阶段 / 载荷 / 闸口 / 目录）

本文件是 task* 族重组后的**唯一真源**。`taskrail` / `task-confirm` / `task-explore` / `taskflow` 与本文有出入时，以本文为准；各 skill 正文只写执行细则，不另造阶段枚举。

## 流程

```text
confirm_mode: human | goal

wizard → explore(+grill) → design → approve → propose → apply → archive
         ↑ expand 可插在 explore / design 之后
```

| 档位 (`tier`) | 路径 |
|---------------|------|
| simple | wizard → grill → approve(轻) → 实现（可单 change）→ 收口 |
| medium | wizard → grill → design(可轻) → approve → propose → apply → archive |
| complex | wizard → explore(+grill) → design → approve → handoff/propose → apply → archive |

简单/中等是**跳过**中间阶段，不是另一套 skill。

## 目录

```text
tasks/
├── INDEX.md
├── ongoing/{slug}/
│   ├── TASK.md
│   ├── wizard/plan.md
│   ├── explore/                 # grill 纪要等（可选）
│   ├── design/
│   ├── approve/                 # 评审意见 + APPROVED.md
│   ├── handoff.md               # 交接摘要（可选；也可写在 TASK.md 交接节）
│   ├── glossary.md              # 惰性
│   └── {sub}/                   # expand：只一层
└── archive/{yyyy-mm-dd}/{slug}/
```

- 凡经 `taskrail` 推进的任务一律建 `tasks/ongoing/{slug}/`（含简单档）。
- 无 `tasks/` 时须先获确认再建（沿用 task-explore 纪律）。
- 运行产物（证据、确认计数器）落**仓外**；`TASK.md` 只存指针（如 `evidence_root`）。
- 单任务产物只写当前任务目录；禁止写仓库根 `CONTEXT.md`、`docs/adr/`、`docs/design/`。

## TASK.md 元信息（封闭字段）

```yaml
slug: <kebab-case>
parent: <父 slug；仅子任务>
status: ongoing | handed-off | blocked | done | archived
phase: wizard | explore | design | approve | propose | apply | archive | done
confirm_mode: human | goal
tier: simple | medium | complex
criterion: "<完成判据原文一条>"
driver: null | "{slug}-driver"
evidence_root: <仓外路径或 null>
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

- `phase` + 各阶段目录产物 = wizard→approve 区间的进度真相。
- propose 之后进度只认 OpenSpec checkbox（driver / 子 change）。
- `handed-off` 只表示账本已换到 taskflow，**不等于** `done`。
- `done` 仅当完成判据成立且交付标准全过（复杂档另要求质量画像齐全、降级无 `pending`/`provisional`）。

## 阶段载荷契约

阶段跳转必须带齐；缺则停在上一 `phase`，禁止下游猜意图：

| 进入阶段 | 必须已有 |
|----------|----------|
| explore / design | `criterion` + `wizard/plan.md`（或 TASK.md「方案」节等价正文） |
| approve | design 产出路径（或简单档的 plan）+ `criterion` + 「不做的事」 |
| propose / handoff | `approve/APPROVED.md`（或 TASK.md 决策节已冻结）+ 判据原文；复杂档含质量画像与显式降级原文快照 |
| apply | driver `tasks.md` 已由 propose 产出 |
| archive（探索侧） | 用户确认关闭；子任务均已结 |

## 确认闸口（封闭）

一律委托 `task-confirm`，不在各 skill 复制第二份规则：

| 闸口 | 说明 |
|------|------|
| wizard 定稿 | 方案落盘前 |
| explore 关键 | 探索方向/范围收敛 |
| design 定稿 | 方案稿可审前 |
| approve | 结构门 + 评审门 + 冻结（必经；简单档可轻量） |
| expand 创建 | 拆子任务前 |
| 危险类退出点 | 线上 / 泄密 / 未点名危险操作等 |

- **human**：列选项 / 等人确认。
- **goal**：写推荐默认 → 派审 → 收敛即放行，同轮继续。
- 线上、泄密、破坏性 git、未点名危险操作：**永不**因审阅收敛自动放行。
- 同闸口连败 2 次 → 停并升级 human，或标 `blocked`。

## Skill 归属

| Skill | 职责 |
|-------|------|
| `taskrail` | 唯一编排入口；绑定任务；推进阶段；完成门 |
| `task-confirm` | human/goal 确认与审阅；退出点；质量画像字段规范 |
| `task-explore` | 台账与 explore/design/expand/approve/handoff/archive |
| `taskflow` | driver + propose/apply/archive；交付 checkbox |

已删除的旧 id（`task-wizard` / `task-goal` / `task-delivery`）勿再引用；统一用上表四 skill。
