---
id: task-confirm
name: task-confirm
description: "确认与审阅协议：human 模式列选项（含推荐）等人确认；goal 模式推荐默认→派审→收敛即放行。不编排档位、不执行步骤。在消息含 /goal、被 taskrail/task-explore 以 goal 模式委派、或任一确认闸口需要本协议时使用。只要步骤级方案给人看用 taskrail wizard；不要用本 skill 代替编排。"
---

# task-confirm：确认与审阅

写给处在确认闸口的执行者。本协议**只**回答「是否放行 / 如何改后放行」；阶段推进与完成门归 `taskrail`。

契约闸口表见 [../taskrail/references/contract.md](../taskrail/references/contract.md)。质量画像字段见 [references/quality-profile.md](references/quality-profile.md)。

## 触发（「在 goal 里」的单一真源）

任一命中则 `confirm_mode` 按 goal 处理；否则 human：

- 消息看得到 `/goal`，或上游显式 `confirm:goal` / `goal:`。
- 当前有进行中的 goal 且本条挂了本 skill。
- 被上游（taskrail / task-explore）以 goal 模式委派。

其他 skill 判断是否处在 goal 里时按本节，不另写一份。

## 模式

| 模式 | 行为 |
|------|------|
| human | 闸口列选项（含推荐），等人确认或改值后放行 |
| goal | 写推荐默认 → 派审 → 完成程度为高且无未消 P0/P1 即收敛放行，同轮继续；不列选项 |

永不因审阅收敛自动放行：**线上动作、泄密、未点名的危险操作、A 类 `pending` 降级**。

## human 闸口呈现（强制）

每个未决口子必须含：**问题**、**推荐**、**一句话理由**；可选备选。**禁止**只列问题、不写推荐。

收口句默认：「按推荐继续 / 改第 N 条」。用户回「按推荐」即按表内推荐放行。

human 强制走查（wizard 定稿 / approve）：无论是否另派审，呈现闸口前自走三连并在呈现中附一行结论——①判据可检查；②流程总览（或推荐方案步骤）从现状走得到判据；③交付标准无漏、无越界。任一项不过：先修方案再走闸口，不把走查失败包装成待确认项。

human 点名派审：用户点名评审（名册 / subagent / 同事已评）时，按下方「审阅」节执行，含 P 级判定与收敛规则；human 闸口表的「推荐整体」即审阅的推荐默认。

输出模板（半屏内）：

```markdown
## 闸口：<名>
推荐整体：<一句话放行路径>
走查：<通过|失败|不适用> — <一句>（wizard 定稿 / approve 必填；其它闸口写「不适用」）

| # | 口子 | 推荐 | 理由 |
|---|------|------|------|
| 1 | … | 是/否/具体值 | … |

回复「按推荐」即放行；改哪条说编号即可。
```

## 闸口输入

调用方须给出：闸口名、推荐默认（**human 与 goal 均必填**）、审阅边界材料（完成判据、「不做的事」、wizard 定稿与 approve 时的流程总览；approve/复杂档另附质量画像与显式降级原文）。缺材料（含缺推荐默认）则停，退出点「理解不够」。

## 审阅（goal；human 在 wizard 定稿 / approve 点名派审时也可复用）

派审前贴上完成判据、「不做的事」，复杂档再贴质量画像与显式降级原文，并写明审与不审。返回完成程度（高/中/低）与范围内意见（P0/P1/P2）。有 P0 或 P1 时完成程度取中或低。

| 环节 | 审 | 不审 |
|------|----|------|
| 方案/流程总览闸口 | 判据可检查；流程总览（或推荐方案步骤）能否走到判据；交付标准是否漏或越界；阻塞/退出是否改道 | 架构、接口、schema、代码骨架；判据与「不做的事」没有的新行为 |
| approve | 同上 + 设计依据是否齐；冻结范围是否清楚 | 详细设计正文代写 |
| 执行中新决策点 | 该岔路及未验证步骤 | 已验证步骤；详细设计 |

**P0**：判据不可检查，或走不到判据，或漏会改道的阻塞/退出；复杂档画像缺必要字段也算。  
**P1**：验证对不住判据，或漏应有交付标准。  
**P2**：不改道的写法问题；写入坑，不参与完成程度。

完成程度写入：

- 有 P0/P1：取中或低（审阅者定高→写中；否则从其值）。
- 无 P0/P1：写高；审阅者定级不参与。

评审者三选一（选中即唯一）：

| 方式 | 何时 |
|------|------|
| role-based-reviewer | 复杂档 approve / 点名角色审 |
| agent-roster | 点名名册或 Endpoint |
| subagent | 默认回退；起不来换模型最多两次 |

只看完成程度是否为高判定通过。只有程度无意见也无诚实结论：再派一次；第二次仍无 →「审阅没有结论」。

**核对**（有 P0/P1 时）：写入判据或步骤后逐条标已消失/仍在/新增。全部消失且无新增 → 收敛。同一条连续两轮仍在，或单轮新增条数 ≥ 上轮已消失数 →「审阅不通过」。approve 闸口内只派一次审阅循环，禁止嵌套再开 approve。

## 退出点

命中则停，向调用方返回标签与所需授权；不标任务完成。

- **理解不够**：写不出可检查判据，或缺推荐默认，或步骤靠会改方案的猜测。
- **审阅不通过** / **审阅派不出** / **审阅没有结论** / **评审者未定**。
- **降级未确认**：A 类仍 `pending`——仅用户点名接受该项、或明确说按降级表全部确认可放行；审阅收敛与单独的「继续」都不算确认。B 类可经审阅记 `provisional`，到用户在场点追认。
- **阻塞解不开**。
- **未点名的危险操作** / **线上动作** / **泄密**。
- **同一验证连败两次**：同一假设下连续失败两次；换假设须写判伪差异；累计假设达 3 仍失败则停。

## 授权

授权只用于退出点已经点名的动作。单独「继续」在因退出点而停时不算授权。意图命中可复述生效（不可逆与线上仍须逐字点名）。

同闸口连败 2 次：返回调用方升级 human 或标 `blocked`。

## 不做

- 不产步骤级方案、不定档位、不改 `TASK.md.phase`。
- 不执行 OpenSpec、不写业务代码。
- 不维护完整四状态网格；任务进度真相在 `TASK.md` / checkbox（见 taskrail 契约）。

## 相关资产

- 质量画像：[references/quality-profile.md](references/quality-profile.md)
- 挂起五元组：[references/suspension.md](references/suspension.md)
- **legacy（勿作进度真源）**：[references/legacy/state-machine.md](references/legacy/state-machine.md)、[references/legacy/state-file.md](references/legacy/state-file.md)、`scripts/goal_transition.py`——仅旧 goal 计数器可选；**新编排进度真相是 `TASK.md.phase` / OpenSpec checkbox**，不得以状态机网格替代 taskrail 阶段推进。

---

## Self-evolution

本 Skill 从真实执行中积累经验，并按 Eval 验证改进。目录（均相对本 Skill 根目录）：

```text
skills/task-confirm/
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
