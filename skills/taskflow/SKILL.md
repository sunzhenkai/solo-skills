---
id: taskflow
name: taskflow
description: "交接后的执行：check_handoff 入口门通过后用 `taskflow-new` 建 `{task}-driver`，拆成多个 OpenSpec change，委托 stock `openspec-*` propose/apply/archive，进度只认 checkbox。仅在用户点名 taskflow / taskflow-new / 某个 `{task}-driver`、或被 taskrail 委派时使用；泛指的推进、resume、/goal 一律走 taskrail。"
---

# taskflow

面向用户默认使用简体中文；命令、路径、代码、状态值与既成术语保持原文。

一个任务 = 一个 driver change `{task}-driver`。实现拆成若干子 change `{task}-<slice>`，与 driver 同一 planning root；跨 root 时在 driver 涉及面表里显式记录 root 或 store id。共享 `{task}` 前缀让 `openspec list` 直接看出归属，不需要额外元数据。

**进度只有 checkbox 一种真相。** 不建 `tasks/` 台账、不写索引文件、不引入编号体系；唯一脚本是只读入口门 `scripts/check_handoff.py`。术语见 [../taskrail/references/glossary.md](../taskrail/references/glossary.md)。

## 阶段路由

| 阶段 | 入口 | 参数 |
|------|------|------|
| 立项 | 本文件「脚手架」小节（command `taskflow-new`） | 任务描述 |
| 澄清 | stock skill `openspec-explore` | `{task}-driver` |
| 提案 | stock skill `openspec-propose` | `{task}-driver` |
| 实施 | stock skill `openspec-apply-change` | `{task}-driver` |
| 归档 | stock skill `openspec-archive-change` | `{task}-driver`（只归档 driver 自身） |

taskflow 只提供 `taskflow-new` 一个 command，四个阶段一律复用 stock skill，不另造等价命令。

## 委托契约

`openspec-*` skill 默认由 `dotf agents -c` 装到全局 `~/.agents/skills`（`openspec init --tools agents`），**不是每个仓都自带**。委托前确认当前 agent 环境能读到它们；不可用就在同一条回复里给全可选项与推荐项——跑 `dotf agents -c` / `openspec init --tools agents` 装到全局，或改用 openspec CLI 直调——用户选完即继续，不反复停，**不要自行发明等价命令**。

可用时，委托必须同时具备两项绑定：**在 driver 的 planning root 下执行**，并**显式给出 change name `{task}-driver`**。缺任一项不得委托——openspec CLI 只认 cwd 最近的 `openspec/`，无绑定会写错位置或反问用户选 change。无法确定时停下报告。

## 入口门（强制）

`taskflow-new`、以及任何创建 `{task}-driver` 或子 change 的动作，**第一步**必须在工作区根跑：

```bash
python3 <taskflow>/scripts/check_handoff.py <workspace-root> <slug>
```

它核对 `tasks/ongoing/<slug>/TASK.md`：`status: handed-off`、`phase` ∈ propose / apply / archive / done，且「## 交接」节带「交付类别」「适用门包」（Web UI 另带 Active Instance 根路径与三条 digest）。exit 非 0 → **拒绝建 driver**，回复用户改走 `taskrail`（approve → handoff），不自行补写 TASK.md 绕过。

- **逃生口**：仅当用户明确说「不走 taskrail 直接建 driver」时，把 `gate_bypass: "<YYYY-MM-DD> user-confirmed: <理由>"` 写入该任务 TASK.md 元信息再跑（脚本以 BYPASS 放行并警告）；无 TASK.md 时先建最小 TASK.md 承载这一行。agent 不得自写或推断该确认；BYPASS 下门包视为未覆盖，按 taskrail 确认协议「未覆盖即降级」登记。
- **派给编码 agent 的提示词**：必须由交接载荷生成——判据原文、交付类别、适用门包条目、证据要求、契约指针（Web UI 含三条 digest 与 `ui_evidence_check` manifest / report 要求）逐项带上；禁止手写省略 UI / 验收的自由提示词。缺载荷 = 入口门不过。

## 脚手架

`taskflow-new {任务描述}` 在入口门通过后固定三步，不多做：

1. 由任务描述归纳 kebab-case 的 `{task}`（Agent 自己归纳，不追问用户；描述确实为空时才问「要做什么？」）。
2. `openspec new change {task}-driver --goal "<任务描述原文>"`。
3. 在该 change 的 `.openspec.yaml` 补 `skip_specs: true`，再按下方模板写 `proposal.md`。

`skip_specs` 的原因、**不要写 `tasks.md`**（留给 propose）、driver `proposal.md` 逐字模板（含固定的 **Driver 协议** 块）、脚手架输出、propose 阶段 `tasks.md` 骨架与 simple 单切片：动手前**先读** [references/driver-template.md](references/driver-template.md)。Driver 协议块逐字写入，不改写、不精简。

## 纪律

propose / apply / 收尾前**先读** [references/execution-discipline.md](references/execution-discipline.md)。要点（细则与例外只在该文件）：

- 进度只认 checkbox：子 change 记实现、driver 记编排；driver 实施项只在子 change 全勾且 `openspec validate --strict` 通过后勾。不另建账本。
- 一轮结束只有三种情况（以 Driver 协议块为准）；「需要用户决策」按 [../taskrail/references/suspension.md](../taskrail/references/suspension.md) 挂起五元组呈现，不依赖的条目继续。
- 新发现的降级按 [../taskrail/references/quality-profile.md](../taskrail/references/quality-profile.md) 定级：A 类 `pending` 停等用户；B 类 `provisional` 到用户在场点追认。
- 归档前逐条跑「收尾机械校核」；禁止 `--yes` 掩盖未勾。最终验收按 [references/acceptance-rubric.md](references/acceptance-rubric.md)，回归按 [references/delivery-quality-loop.md](references/delivery-quality-loop.md)。
- 并行：旗舰先行、同类失败升级、改共享面必广播。
- 实现者输入：按 [references/implementer-isolation.md](references/implementer-isolation.md)；命中 [../taskrail/references/gate-packs.md](../taskrail/references/gate-packs.md) 时必带契约文件 / 门包 / 证据要求。
- Web UI 切片委托 `ui-template-apply`；完成 = `ui_evidence_check.py` report exit 0 + design 评审 `--validate-review` exit 0。

---

## Self-evolution

本 Skill 从真实执行中积累经验，并按 Eval 验证改进。目录（均相对本 Skill 根目录）：

```text
skills/taskflow/
├── SKILL.md
├── examples/      # 经过验证的优秀执行案例
├── evals/         # 可验证成功标准（cases.yaml）
└── experience/    # 真实失败 / 成功 / 规律
```

自进化不改变上文已规定的目标、流程、工具用法、输出与约束。

- 执行复杂任务前先查 `examples/`，有相关成功案例就复用；没有就按正文执行，不编造案例。
- 任务完成前对照 `evals/cases.yaml` 验证关键输出；Eval 失败先修输出，不带着失败交卷。
- 完成后遇失败、用户纠正、明显成功或新的有效方法才写入 `experience/`：单次失败进 `failures/`，重复规律进 `patterns/`（至少两次同类证据）。不记 trivial 信息，不伪造条目，不写密钥 / 内部 URL / 凭据。
- 改生产正文：先出提案并经用户确认，再走 `skill-evolver`（`evolutions/`）或 `skill-upgrader` 的 `update` 模式（`patches/`）；禁止由单次失败直接改 `SKILL.md`。
