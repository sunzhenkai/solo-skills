# 台账：布局、索引、绑定与写入纪律

<!-- 原 ledger.md -->
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
- `new` / `split` / `expand` / `save` / `approve` / `decide` / `handoff` / `archive` / `reopen` 必须同步对应行：任务名、标题、日期、一句话目标、相对 `tasks/` 的路径；写入纪律见 [references/ledger.md](ledger.md)
- 不要把进展日志或对话抄进索引
- 子任务行的任务列写 `{parent}/{sub}`、路径列写嵌套路径；父归档整树搬家后把子行路径批量更新为新位置
- 发现漂移（目录有、索引无，或索引指向不存在的路径）：按 `ongoing/` 与 `archive/` 下的 `TASK.md`（含 `ongoing/{parent}/{sub}/` 一层子目录）**重建** INDEX，再继续
- 已有 `tasks/` 但没有 INDEX：在需要列表或下一次会写 INDEX 的阶段重建，不必再问
- `handed-off` 行（含子任务）的一句话以 `→ {task-name}-driver` 结尾；父任务行一句话聚合子任务状态（如「3 子任务：2 已交接、1 设计中」）

## 绑定（强制）

会话绑定 `{task-name}` + `{taskRoot}` = `tasks/ongoing/{task-name}`（`reopen` 完成前 `{taskRoot}` 仍在 archive）。绑定子任务时任务名显示为 `{parent}/{sub}`，`{taskRoot}` = `tasks/ongoing/{parent}/{sub}/`。

**无 task 上下文时，自行判定新建还是恢复：用户这次说的和某个进行中任务是同一件事就恢复它，否则新建（slug 自拟）。一句话说出决定和理由，例如「新建任务 mcp-admin-tools，因为和进行中的 i18n 无关；接下来进意图确认」，记入新任务 `TASK.md`「已做决定」，直接往下走，不提问、不列选项。** 归档要拉回则走 `reopen`。不得先聊后补目录。

1. 先读 `tasks/INDEX.md` 的 Ongoing 表；无 INDEX 或发现漂移则扫 `ongoing/` 并重建。列出任务名 + 标题/一句话。无 `tasks/` 或 Ongoing 为空则说明「当前没有进行中的任务」。
2. 对照 Ongoing 列表自行判定：同一件事 → `resume` 它；无关 → `new`；用户只说「继续」→ 恢复最近更新的那项。用户本轮已点名 `new`/`resume`/`reopen`/`handoff` 及对象时照办。
3. 用一句话说出决定和理由，不列选项、不加「理解偏了请纠正」之类的邀请，然后直接进入下一步。

同名 `ongoing/{task-name}` 已存在时，禁止覆盖；是同一件事就 `resume`，否则换名并说明。

## 进展提示

**在任务有进展时直接更新任务文档。** 适用于 `explore` / `chat` / `design` / `approve` / `decide` 之后出现了新目标、新发现、新决定或新缺口：按 `save` 写回（含 INDEX），一句话告知写了什么，不先问（属记账）。


<!-- 原 ledger-write-discipline.md -->
# 台账写入纪律（并发安全）

写 `tasks/INDEX.md` 或 `{taskRoot}/TASK.md` 前必读本文件。适用阶段：`new` / `save` / `split` / `expand` / `approve` / `decide` / `handoff` / `archive` / `reopen`。多会话、多 agent 并发写同一台账是常态，下列五条是硬步骤，任一不过即停，不靠事后重建兜底。

## 1. 锚点唯一才动手

- 写前重读**目标小节**，不凭上一轮记忆。
- 确定锚点串：插入位置的唯一标识文本（小节标题、表头行、或被替换的整行原文）。
- 用 grep 或计数确认锚点串在该文件中出现次数**恰为 1**。
- 出现 0 次或 ≥2 次即停止，重读全文重新定位；不猜、不取第一个匹配。

## 2. 索引行只整行替换 + 三断言

- `INDEX.md` 表格行只允许**整行替换**，禁止只改个别单元格。
- 替换后立即断言三件事：
  1. 该行按 `|` 分列后的列数与表头一致（Ongoing、Archived 表均 5 列）；
  2. 该行任务列仍以预期任务前缀开头（子任务为 `{parent}/{sub}`）；
  3. 文件总行数变化与本次意图相符：追加 = +1，原地更新 = 0，移动 = 0。
- 任一不符，用改前读到的整行原文改回，停止本次 INDEX 后续写入并报告冲突。不继续写、不「先这样」。

## 3. 删除只许精确整行等值

- 删除索引行只允许**精确整行等值**匹配（整行文本完全相同），删除后校验文件行数**恰减少 1**。
- 禁止「按内容过滤后批量删除」的写法：条件过窄会误删他任务刚写入的行。
- 批量**更新**路径不在此禁列。`archive` / `reopen` 整树搬家时子任务行路径批量改写，按 `references/archive-reopen.md` / `references/archive-reopen.md` 执行，但匹配条件用**父路径前缀**而非精确等值，且断言被改行数等于该父任务的子任务数；不符即停。

## 4. 编号列表先读最大号

- 向编号列表（`TASK.md`「已做决定」的 `D-n`、子任务登记行等）追加前，先读当前最大编号。
- 追加后校验无重复编号。
- 新内容一律**整块插入目标小节末尾**，不得追加到文件尾。

## 5. 并发冲突不静默覆盖

- 工具告警「目标文件自上次读取后已被修改」，或重读发现内容与预期不符，即重读目标小节，仅在锚点仍唯一时写入自己的新块。
- 与既有内容矛盾处，用显式「更正」或「冲突」条目写出并注明日期；不静默改写他人小节、不抹掉仍有效的旧内容。
- 无法安全合并即停止并报告，不强行写入。
