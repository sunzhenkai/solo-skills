# task-explore：各命令门禁与步骤

由 [../SKILL.md](../SKILL.md)「命令」表引用；进入某命令时只读该命令小节与其 phase 详情。

## `new`

立项。细则见 [references/cmd-new.md](cmd-new.md)。

1. 若没有 `tasks/`：**询问是否在当前位置创建 `tasks/`**。未确认则停止。
2. 推断 `{task-name}`；冲突则 resume 或换名。创建 `TASK.md`（模板）与 INDEX 行；绑定任务。
3. 输入含现成方案时登记进「方案」小节，不丢上游产物；无完成判据不编造。
4. 报告路径，询问下一步：`explore`（默认建议）还是 `chat`。不要自动开始 grill。

## `explore`

不断探索预期目标，委托 `grilling`。进入本命令后 **先读** [references/phase-explore.md](phase-explore.md)，再开始提问。未读完不要 grill。禁止调用 `grill-with-docs` / `domain-modeling`。

- **仅 grill**（simple / medium，经 taskrail）：只做 grilling 澄清，不强制写 glossary/ADR 全套。
- **完整 explore**（complex）：按 phase-explore 全文（含外部参照、术语/ADR 落盘）。

## `chat`（默认）

对任务问答。细则见 [references/cmd-chat.md](cmd-chat.md)。

- 只读本仓代码与任务里已有笔记，不做外部参照；不要开始实现。
- 不要把 `chat` 默认为 `explore`（不自动 grill）或 `design`（不写方案稿）。
- 路径已清、要交付 → `approve` 然后 `handoff`。有进展则提示是否更新任务文档。

## `resume`

恢复进行中的探索任务。细则见 [references/cmd-resume.md](cmd-resume.md)。

- **任务文档只读**；发现 INDEX 漂移时允许重建 `INDEX.md`（INDEX 漂移可重建），不要改 `TASK.md` / `glossary.md` / `design/`。
- 未指定名字：用 INDEX 列出请用户选。已归档不要自动恢复，走 `reopen`。
- 短摘要：**目标 / 当前 phase / 进展 / 未决 / 建议下一步**，然后等用户。

## `design`

方案写入 `{taskRoot}/design/`，不写 `docs/design/`。**方案不明朗时主动打断，提示缺口。** 进入本阶段后 **先读** [references/phase-design.md](phase-design.md)；落盘时再读 [references/design-template.md](design-template.md)。写对比表之前按阶段详情做一次外部参照。复杂档在此产出质量画像草稿（字段见 taskrail 确认协议）。命中交付类别门包时，本阶段另落 `design/contract.md`（契约文件指针与证据计划；判定与门包内容见 taskrail 确认协议 门包表）。Web UI：medium/complex 无 frozen Active Instance 则停下移交 `ui-template-design`；`design/contract.md` 须含根路径与三条 digest。方案成形后走 `approve`。发现 ≥2 独立方向时评估一次 `expand`。

## `approve`

**必经**（简单档可由 taskrail 做轻量：只核判据可检查）。结构门 + 评审门 + 冻结。进入本阶段后 **先读** [references/phase-approve.md](phase-approve.md)。没有可批准的方案就打断。Web UI 结构门另核 Active Instance freeze / digest（simple 无 freeze 须已确认 adopt-only 降级）。用户说「按推荐冻结并交接」时，本轮 `approve` 完立刻 `handoff`。处在 goal 里时不逐条问用户，按「Goal 里的确认」走 taskrail 确认协议 审阅；审阅收敛则同样本轮 `approve` 完立刻 `handoff`。

同一任务可多次 `approve`：新决策追加编号写入决策节，被取代的旧决策标注「被 D-n 取代」。父任务的 `approve` 仅限范围、非目标与拆分原则，具体方案属各子任务。

兼容：点名 `decide` / `plan-review` 时改走本阶段（处在 goal 里时不逐条问用户）。

## `save`

保存任务最新进展。细则见 [references/cmd-save.md](cmd-save.md)。

1. 必须已绑定。合并本轮进展，不抹掉仍有效的旧内容。
2. 更新 `updated` 与相关章节；同步 INDEX（不要把进展日志抄进索引）。
3. 不要贴聊天记录。无新进展则说明无需写入。

## `handoff`

把探索任务交给 taskflow（`{task-name}-driver`），任务转入 `handed-off`；**不归档、不搬目录、不清绑定**。成功后调用方（taskrail）置 `phase: propose`（本命令不把 `handoff` 写入 `phase`）。进入本阶段后 **先读** [references/phase-handoff.md](phase-handoff.md)。交接门禁含：命中交付类别门包时，契约文件指针与证据计划已就绪且契约本体已在交付仓；Web UI 另须三条 digest 进 driver（细则见阶段详情）。交接目标按绑定自动推断，无需用户逐项指定：

- 绑定子任务 → 交接该子任务，建 `{sub}-driver`。
- 绑定父任务 → 父是纯伞不可交接，自动批量交接所有「已 `approve`（或兼容 `decide`）未交接」的子任务，无需逐项确认；就绪为零则打断并报告各子任务所缺条件；未批准的子任务跳过且不阻塞其余。批量中任一失败即停，已交接的不回滚。
- 父任务无子任务 → 提示 `expand`/`split` 拆分或 `new` 另建，**不建 `{parent}-driver`**。

**`handed-off` 状态**：任务留在 `tasks/ongoing/`，INDEX 的 Ongoing 表保留该行（一句话以 `→ {task-name}-driver` 结尾）；可 `resume` 查看方案/决策/交接记录，进度只认 taskflow checkbox，任务文档不再勾交付进度；再次 `handoff` 只报告 driver 路径。方案修订默认直接改 driver 的 `proposal.md`；改动大或要推翻决策时，点名 `reopen` 撤回交接（`status` 回 `ongoing`）后重新 `approve` → `handoff`。

## `archive`

对确认关闭的探索任务归档（不交接而结束、或 `handed-off` 后确认无需回溯），整树搬到 `tasks/archive/{yyyy-mm-dd}/{task-name}`。要交付请用 `handoff`，不要用本阶段代替交接。经 taskrail、方案已冻结且方案含实施动作、尚未 `handed-off` 时，不进入本命令，改走 handoff。「方案已写完」「还有未决」不是关闭原因。进入本阶段后 **先读** [references/phase-archive.md](phase-archive.md)，未读完不得搬目录。

门禁按序执行、任一不过即停；步骤与细则在 reference，下列五条不可跳过：

- 必须已绑定或用户给出名字，且拿到用户「确认关闭」的明确答复；只给名字不算确认，未确认不搬。
- **目标已存在则停止并询问，禁止覆盖；此时不得改 `TASK.md`、不得移动目录、不得改 INDEX。**
- 存在子任务目录时：所有子任务 `status` 必须为 `handed-off` 或 `archived`，否则打断并列出未结子任务。父任务归档即整树关闭。
- 未决问题、曾 `handed-off` 的 driver 交付进度、指向旧路径的入链，三项必须清点并合并成一次确认后才搬。
- 必须在 `TASK.md` 留下本次结论与关闭原因，并写 `{taskRoot}/SUMMARY.md`（给人读的时间线总结）；曾 `handed-off` 的任务必须先按 `save` 落盘才搬。`archived` 日期在元信息、目录名、INDEX 三处一致。

不要把任务内容晋升到 `docs/design/` 或其它项目文档，除非用户另说。

## `reopen`

把已 `archive` 的探索任务搬回 `tasks/ongoing/{task-name}`；或对 `handed-off` 任务撤回交接（目录不动，只改状态）。进入本阶段后 **先读** [references/phase-reopen.md](phase-reopen.md)，未读完不得搬目录。

定位分支与步骤在 reference，下列四条门禁不可跳过：

- 必须拿到用户「确认 reopen」的明确答复；只给任务名不算确认。
- **目标已存在则停止并询问，禁止覆盖；此时不得改 `TASK.md`、不得移动目录、不得改 INDEX。**
- 状态以 `TASK.md` 的 `status` 为准，不按目录位置猜；已 `handed-off` / 已 `archived` 的子任务不自动复活，driver 一律不删。
- 撤回 `handed-off` 后，INDEX 行留在 Ongoing 但去掉 `→ {task-name}-driver` 尾注。

---

## `expand` / `split`

从当前绑定的探索任务拆出子任务，承接一个可独立推进的方向。`split` 是 `expand` 的别名。子任务是完整探索任务，只是目录嵌套、`TASK.md` 带 `parent:`。闸口「expand 创建」走 taskrail 确认协议。

触发强化：`design` 发现 ≥2 独立方向，或 `approve` 驳回「范围过大」时，**必须评估一次**（提示并等人/goal 确认），不静默跳过。

1. 必须已绑定，绑定任务即父任务。绑定任务本身是子任务（`TASK.md` 已有 `parent:`）则停止：子任务只一层，提示改用 `approve` / `handoff` 收敛。
2. 缺 `{sub}` 名或一句话方向则询问；`explore` / `chat` 中发现可拆方向时只提示一次，不自动创建。
3. `{sub}` 用 kebab-case，且 **全局唯一**：扫 `ongoing/` 全树（含各父目录的子目录）无同名，冲突则换名。
4. 创建 `ongoing/{parent}/{sub}/TASK.md`（用模板）：填 `parent: {parent}`，继承父完成判据中可拆部分并写子判据，目标节写该方向的子目标，现状节链接父 `TASK.md` 相关段落。
5. 父 `TASK.md` 的 **子任务** 小节登记一行（无该小节则新建）：`{sub}`、一句话方向、状态、创建日期。
6. `INDEX.md` Ongoing 表追加一行：任务列 `{parent}/{sub}`，路径列 `ongoing/{parent}/{sub}/`。
7. 绑定切换到子任务，报告路径，询问下一步（默认建议 `explore`）。父任务随时可 `resume` 回来。父任务 `status` 恒 `ongoing`、自身无独立进度；`handoff` 永不针对父（对父点名 `handoff` = 自动批量交接就绪子任务），父也永不建自己的 driver。子任务均 `handed-off` 或 `archived` 后，父才可 `archive`。
