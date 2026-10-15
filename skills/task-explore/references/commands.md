# task-explore：各命令门禁与步骤

由 [../SKILL.md](../SKILL.md)「命令」表引用；进入某命令时只读该命令小节与其 phase 详情。

## `new`

1. 若没有 `tasks/`：在当前仓库根直接创建，一句话说明。
2. 推断 `{task-name}`。同名已存在：是同一件事就 resume，否则换名，一句话说明。在已有任务下拆子方向不属于 `new`，走 `split`。
3. 创建 `tasks/ongoing/{task-name}/TASK.md`（用模板，填已知目标与 `phase`/`confirm_mode`/`tier`/`criterion` 元信息）。输入含现成方案（含上游 taskrail wizard 的流程总览方案）时，把完成判据、事实、假设、质量属性、流程总览、阻塞点、坑一并登记进「方案」小节，并可落 `wizard/plan.md`，不丢上游产物。输入里没有完成判据时不要编造。
4. 在 `tasks/INDEX.md` 的 Ongoing 表追加一行（无 INDEX 则按模板创建或按目录重建）。
5. 绑定该任务。报告路径，并说明下一步默认进 `explore`，想先随便聊就说 `chat`。不要自动开始 grill。

## `explore`

不断探索预期目标，委托 `grilling`。进入本命令后 **先读** [references/explore-design.md](explore-design.md)，再开始 grill（自问自答，见该文件）。未读完不要 grill。禁止调用 `grill-with-docs` / `domain-modeling`。

- **仅 grill**（simple / medium，经 taskrail）：只做 grilling 澄清，不强制写 glossary/ADR 全套。
- **grill 在意图确认之后**：`wizard/intent.md` 已确认的目标与边界不重问，grill 只追细节；冲突回 `task-intent` 纠偏。
- **完整 explore**（complex）：按 phase-explore 全文（含外部参照、术语/ADR 落盘）。

## `chat`（默认）

对任务进行问答：解释、排查、对照代码与已有笔记。先读任务文档再答。

- 只读本仓代码与任务里已有笔记，不做外部参照；不要开始实现。
- 不要把 `chat` 默认为 `explore`（不自动 grill）或 `design`（不写方案稿）。
- 用户要把方案写下来 → 转 `design`。目标仍糊 → 建议 `explore`。路径已清、要交付 → `approve` 然后 `handoff`，不要直接开一个无关名字的 driver。
- 发现任务含多个可独立推进的方向 → 提示一次可 `expand`（别名 `split`）拆子任务，不阻断，用户确认才建。
- 用户要看有哪些任务 → 打印 INDEX，不进入 `new`。
- 有进展则直接更新任务文档并一句话告知（记账，不先问）。

## `resume`

恢复进行中的探索任务。**任务文档只读**；发现 INDEX 漂移时允许重建 `INDEX.md`，不要改 `TASK.md` / `glossary.md` / `design/`。

1. 未指定名字：按用户这次说的话对上 Ongoing 表里的任务；对不上就恢复最近更新的那项，一句话说明恢复了哪个。指定了则用该名字。
2. 任务不在 `ongoing/`：先查 INDEX 的 Archived 表，再扫 `tasks/archive/`。告知已归档路径；**不要自动恢复**，拉回走 `reopen`。找不到则说明，改走 `new`。
3. 读 `TASK.md`、`glossary.md`、`design/`（有则读索引与最新稿）。恢复子任务时先只读父 `TASK.md` 的目标与「已做决定」防方向漂移，再读子任务全套；父文档不被修改。
4. 按 [user-report.md](../../taskrail/references/user-report.md) 的 resume 模板口语恢复：目标、做到哪、还卡着什么、接下来我做什么（白话动作，不报命令名或 phase）、我定了什么（难回头的单独一行）、真阻塞时需要什么。内部命令选择留给自己。然后等用户。

## `design`

方案写入 `{taskRoot}/design/`，不写 `docs/design/`。**方案不明朗时主动打断，提示缺口。** 进入本阶段后 **先读** [references/explore-design.md](explore-design.md)；落盘时再读 [references/templates.md](templates.md)。写对比表之前按阶段详情做一次外部参照。复杂档在此产出质量画像草稿（字段见 taskrail 确认协议）。命中交付类别门包时，本阶段另落 `design/contract.md`（契约文件指针与证据计划；判定与门包内容见 taskrail 确认协议 门包表）。Web UI：complex 无 frozen Active Instance 则停下，先在交付项目根建立 Active Instance 至 freeze；`design/contract.md` 须含根路径与三条 digest。方案成形后走 `approve`。发现 ≥2 独立方向时评估一次 `expand`。

## `approve`

**必经**（简单档可由 taskrail 做轻量：只核判据可检查）。结构门 + 评审门 + 冻结。进入本阶段后 **先读** [references/approve.md](approve.md)。没有可批准的方案就打断。Web UI 结构门另核 Active Instance freeze / digest（simple 无 freeze 须已确认 adopt-only 降级）。用户说「按推荐冻结并交接」时，本轮 `approve` 完立刻 `handoff`。处在 goal 里时不逐条问用户，按「Goal 里的确认」走 taskrail 确认协议 审阅；审阅收敛则同样本轮 `approve` 完立刻 `handoff`。

同一任务可多次 `approve`：新决定追加编号写入「已做决定」，被取代的旧决策标注「被 D-n 取代」。父任务的 `approve` 仅限范围、非目标与拆分原则，具体方案属各子任务。

兼容：点名 `decide` / `plan-review` 时改走本阶段（处在 goal 里时不逐条问用户）。

## `save`

保存任务最新进展到任务文档。

1. 必须已绑定。读现有 `TASK.md`，合并本轮进展，不抹掉仍有效的旧内容。
2. 更新 `updated`、目标/非目标、现状、进展、决策、交接、未决、下一步。有设计结论则链到 `design/`。
3. 同步更新 `INDEX.md` 中该任务的标题、日期、一句话目标；不要把进展日志抄进索引。
4. 不要贴聊天记录。无新进展则说明无需写入。
5. 报告改了哪些文件。

## `handoff`

把探索任务交给 taskflow（`{task-name}-driver`），任务转入 `handed-off`；**不归档、不搬目录、不清绑定**。成功后调用方（taskrail）置 `phase: propose`（本命令不把 `handoff` 写入 `phase`）。进入本阶段后 **先读** [references/handoff.md](handoff.md)。交接门禁含：命中交付类别门包时，契约文件指针与证据计划已就绪且契约本体已在交付仓；Web UI 另须三条 digest 进 driver（细则见阶段详情）。交接目标按绑定自动推断，无需用户逐项指定：

- 绑定子任务 → 交接该子任务，建 `{sub}-driver`。
- 绑定父任务 → 父是纯伞不可交接，自动批量交接所有「已 `approve`（或兼容 `decide`）未交接」的子任务，无需逐项确认；就绪为零则打断并报告各子任务所缺条件；未批准的子任务跳过且不阻塞其余。批量中任一失败即停，已交接的不回滚。
- 父任务无子任务 → 提示 `expand`/`split` 拆分或 `new` 另建，**不建 `{parent}-driver`**。

**`handed-off` 状态**：任务留在 `tasks/ongoing/`，INDEX 的 Ongoing 表保留该行（一句话以 `→ {task-name}-driver` 结尾）；可 `resume` 查看方案/决策/交接记录，进度只认 taskflow checkbox，任务文档不再勾交付进度；再次 `handoff` 只报告 driver 路径。方案修订默认直接改 driver 的 `proposal.md`；改动大或要推翻决策时，点名 `reopen` 撤回交接（`status` 回 `ongoing`）后重新 `approve` → `handoff`。

## `archive`

对确认关闭的探索任务归档，整树搬到 `tasks/archive/{yyyy-mm-dd}/{task-name}`。要交付请用 `handoff`。经 taskrail、方案已冻结且含实施动作、尚未 `handed-off` 时改走 handoff。进入前 **先读** [references/archive-reopen.md](archive-reopen.md)：不覆盖、不搬未确认的、先列未结项。

## `reopen`

把已归档任务搬回 `ongoing/`，或撤回 `handed-off`（目录不动）。进入前 **先读** [references/archive-reopen.md](archive-reopen.md)；须用户「确认 reopen」，目标已存在则停止，driver 不删。

---

## `expand` / `split`

从当前绑定的探索任务拆出子任务，承接一个可独立推进的方向。`split` 是 `expand` 的别名。子任务是完整探索任务，只是目录嵌套、`TASK.md` 带 `parent:`。闸口「expand 创建」走 taskrail 确认协议。

触发强化：`design` 发现 ≥2 独立方向，或 `approve` 驳回「范围过大」时，**必须评估一次**（提示并等人/goal 确认），不静默跳过。

1. 必须已绑定，绑定任务即父任务。绑定任务本身是子任务（`TASK.md` 已有 `parent:`）则停止：子任务只一层，提示改用 `approve` / `handoff` 收敛。
2. 缺 `{sub}` 名就由方向推断；连一句话方向都没有才停下，说明需要它；`explore` / `chat` 中发现可拆方向时只提示一次，不自动创建。
3. `{sub}` 用 kebab-case，且 **全局唯一**：扫 `ongoing/` 全树（含各父目录的子目录）无同名，冲突则换名。
4. 创建 `ongoing/{parent}/{sub}/TASK.md`（用模板）：填 `parent: {parent}`，继承父完成判据中可拆部分并写子判据，目标节写该方向的子目标，现状节链接父 `TASK.md` 相关段落。
5. 父 `TASK.md` 的 **子任务** 小节登记一行（无该小节则新建）：`{sub}`、一句话方向、状态、创建日期。
6. `INDEX.md` Ongoing 表追加一行：任务列 `{parent}/{sub}`，路径列 `ongoing/{parent}/{sub}/`。
7. 绑定切换到子任务，报告路径，并说明下一步默认进 `explore`。父任务随时可 `resume` 回来。父任务 `status` 恒 `ongoing`、自身无独立进度；`handoff` 永不针对父（对父点名 `handoff` = 自动批量交接就绪子任务），父也永不建自己的 driver。子任务均 `handed-off` 或 `archived` 后，父才可 `archive`。
