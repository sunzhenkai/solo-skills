# task-explore：台账布局、索引、绑定与进展提示

由 [../SKILL.md](../SKILL.md)「台账与绑定」引用；任何命令写台账或绑定任务前读本文件。

## 布局

默认 `TASKS_ROOT` = 当前工作目录下的 `tasks/`。

```text
tasks/
├── INDEX.md             # 派生索引：快速检索/查看
├── ongoing/{task-name}/
│   ├── TASK.md          # 主文档：phase/status/判据、目标、进展、决策、交接
│   ├── wizard/plan.md   # taskrail wizard 落盘（若有）
│   ├── SUMMARY.md       # 归档时生成的人读时间线总结
│   ├── glossary.md      # 任务内术语（惰性）
│   ├── design/          # 方案、ADR
│   ├── approve/         # APPROVED.md、评审意见
│   └── {sub}/           # 子任务（expand/split 创建，只一层）
└── archive/{yyyy-mm-dd}/{task-name}/
```

- `{task-name}`：kebab-case，由输入推断，不追问；描述为空才问「要探索什么？」
- 子任务目录 = 含 `TASK.md` 的子目录（`design/`、`glossary.md` 不算）；只一层，子任务不得再有子任务。
- `{sub}` 全局唯一（跨所有父任务），`split` 时扫全树校验；driver 名规则不变（`{sub}-driver`）。
- 没有 `tasks/` 目录时 **必须先获得确认再创建**。已有 `tasks/` 则可直接建 `ongoing/`、任务目录与缺失的 `INDEX.md`。
- 单任务产物只写当前任务目录。`tasks/INDEX.md` 是唯一允许的根级任务文件；评审、委派回收等产物只写绑定的 `{taskRoot}`（如 `design/review-<slug>.md`），禁止在 `tasks/` 根级创建任务目录之外的新目录（如 `tasks/reviews/`）。禁止写到仓库 `docs/design/`、`docs/adr/`、根 `CONTEXT.md`。
- 是否把 `tasks/` 纳入 git 由项目决定，不要擅自改 `.gitignore`。

## 索引

`tasks/INDEX.md` 供快速检索与查看，**不是第二份真相**。

- 单任务真相只在 `{taskRoot}/TASK.md`
- 列出、选择、搜索任务时 **先读 INDEX.md**
- `new` / `split` / `expand` / `save` / `approve` / `decide` / `handoff` / `archive` / `reopen` 必须同步对应行：任务名、标题、日期、一句话目标、相对 `tasks/` 的路径；写入纪律见 [references/ledger-write-discipline.md](ledger-write-discipline.md)
- 不要把进展日志或对话抄进索引
- 子任务行的任务列写 `{parent}/{sub}`、路径列写嵌套路径；父归档整树搬家后把子行路径批量更新为新位置
- 发现漂移（目录有、索引无，或索引指向不存在的路径）：按 `ongoing/` 与 `archive/` 下的 `TASK.md`（含 `ongoing/{parent}/{sub}/` 一层子目录）**重建** INDEX，再继续
- 已有 `tasks/` 但没有 INDEX：在需要列表或下一次会写 INDEX 的阶段重建，不必再问
- `handed-off` 行（含子任务）的一句话以 `→ {task-name}-driver` 结尾；父任务行一句话聚合子任务状态（如「3 子任务：2 已交接、1 设计中」）

## 绑定（强制）

会话绑定 `{task-name}` + `{taskRoot}` = `tasks/ongoing/{task-name}`（`reopen` 完成前 `{taskRoot}` 仍在 archive）。绑定子任务时任务名显示为 `{parent}/{sub}`，`{taskRoot}` = `tasks/ongoing/{parent}/{sub}/`。

**无 task 上下文时，应提示创建或者恢复（给出 ongoing 列表选择），在确认后进行 new/resume 命令。** 归档要拉回则走 `reopen`。不得猜测任务、不得先聊后补目录。

1. 先读 `tasks/INDEX.md` 的 Ongoing 表；无 INDEX 或发现漂移则扫 `ongoing/` 并重建。列出任务名 + 标题/一句话。无 `tasks/` 或 Ongoing 为空则说明「当前没有进行中的任务」。
2. 请用户选择：**创建**（`new`）或 **恢复**（`resume`，从列表选）。
3. 用户确认前不进入 `chat` / `explore` / `design` / `approve` / `decide` / `save` / `handoff` / `archive`。

例外：用户本轮已明确 `new`/`resume`/`reopen`/`handoff` 及对象。`ongoing/` 仅一项且用户说「继续/恢复」→ 可直接 `resume` 该项。

同名 `ongoing/{task-name}` 已存在时，禁止覆盖；改为提议 `resume` 或换名。

## 进展提示

**在任务有进展时提示是否更新任务文档。** 适用于 `explore` / `chat` / `design` / `approve` / `decide` 之后出现了新目标、新发现、新决策或新缺口。

- 提示一次即可，不阻断继续问答。
- 用户同意 → 按 `save` 写回（含 INDEX）。
- 用户点名 `save` → 直接写，不必再问。
