---
name: agent-roster
description: 维护跨机器的 agent 端点名册（谁在哪台机器上、擅长什么），并据此把一件事委派给合适的 agent 执行、回收产出、留下可复用案例。用于需要让另一个 agent 定计划、做评审或实施，也用于登记、探测、查询可用 agent；不实现被委派 agent 自身的能力，也不把名册与案例写进本仓库。
---

# Agent Roster

让一个 agent 有依据地决定「这件事交给谁做」，然后真的派出去、取回产出、留下证据。

## 数据在哪

本仓库只有机制，一条真实记录都没有。数据位置由 `~/.config/agent-roster/config.yaml` 的 `data_root` 指出（缺省时先问使用者，不要猜）。

| 内容 | 位置 | 谁写 |
| --- | --- | --- |
| Roster（Endpoint 画像） | `<data_root>/agents/<host>/<kind>.md` | 客观段由 Probe 回填，Disposition 由人或 agent 维护 |
| Routing Rule | `<data_root>/agents/routing.md` | 只由 `$skill-upgrader` 从案例固化，初始为空 |
| Trace（案例） | `<data_root>/agents/traces/<YYYYMMDD>-<slug>.md` | Orchestrator，仅在有教训时 |
| Run（运行痕迹） | `~/.cache/agent-roster/runs/<run-id>/` | 委派时自动落盘，可随时删 |
| Handoff（交接物） | 调用方在发起委派时指定的项目内路径 | 见「回收」 |
| Pattern（通用规律） | 本仓库 `experience/patterns/` | 只能在源仓库改，运行时只读 |

格式见 [references/endpoint-schema.md](./references/endpoint-schema.md) 与 [references/trace-format.md](./references/trace-format.md)。

## 路由：选谁

1. 读 `routing.md`。为空就跳过，不要因为它空着而编规则。
2. 读候选 Endpoint 的画像。只读与当前任务相关的，不要把整个名册载入。
3. 检索相关 Trace（按 Agent Kind 与任务关键词），重点看失败与返工的那些。
4. **在执行之前**把「选了谁、当时有哪些候选、为什么选它」写进 `~/.cache/agent-roster/runs/<run-id>/decision.md`。事后补写的理由没有价值，它会让后续学习学到编造的故事。
5. 证据不足或没有合适候选时，直接问使用者，不要凭 Agent Kind 的名气猜。

## 委派：怎么派

委派通过一层适配契约发出，本 skill 不绑定具体执行器：

**输入** — Endpoint、prompt、工作目录、权限档位、期望交接物路径、超时上限
**输出** — 状态（completed / failed / timeout）、结果摘要、交接物路径、Run 目录

默认实现是 `acpx`，命令形态与降级方式见 [references/delegation-contract.md](./references/delegation-contract.md)。换掉执行器不应改动本文件。

权限只有两档，按委派性质定，不要逐次商量：

- **只读**（默认）：定计划、评审、调研、排查。受派 Endpoint 不许改工作目录里的任何文件。
- **可写**：仅实施类委派。发起前必须确认工作目录处于干净状态，否则先停下来问。

只读委派下受派方无法写文件，所以它的产出由 Orchestrator 从结果文本落盘到指定的 Handoff 路径——这条约束顺带保证了「定计划」这类委派永远不会偷偷动到代码。

## 回收：产出与交接

- Run 痕迹留在 `~/.cache/`，**不进任何 git 仓库**。它量大、含完整对话，且极易混入敏感内容。
- Handoff 落在项目里调用方指定的路径。它是真正的工作成果，应该被看见、被评审、被提交。
- 每次委派都必须显式说明期望产出什么。说不清要什么产出的委派，说明任务本身还没想清楚。
- 串接多次委派时，下一棒读的是上一棒的 Handoff 文件，不是把上一棒的完整输出塞进 prompt。

## 留痕：什么时候写 Trace

只在以下情形写，例行成功不写——否则有用的教训会被「派给 X，成功」淹没：

- 委派失败、超时，或结果需要返工
- 使用者纠正了选人决定
- 结果明显超出预期
- 用了新的委派方式或新的 Endpoint

字段见 [references/trace-format.md](./references/trace-format.md)。其中「为什么选它」是唯一能在将来固化成 Routing Rule 的东西，必须从 `decision.md` 原样搬过来，不要重写。

## 名册维护

```bash
python3 <skill-dir>/scripts/probe_endpoints.py            # L1：装没装、什么版本
python3 <skill-dir>/scripts/probe_endpoints.py --level 2  # L2：ACP 适配器能不能握手
python3 <skill-dir>/scripts/probe_endpoints.py --render   # 输出可粘贴的 Markdown 状态块
```

探测分三层，失败时要能区分三种完全不同的处置：

1. **L1 存在性** — CLI 在不在 PATH、什么版本。零成本，随时可跑。
2. **L2 握手** — 起 ACP 适配器走完 `initialize` 就断开。零 token，能确认适配器真的拉得起来。
3. **L3 冒烟** — 真发一句 prompt，确认登录态、额度与模型可用。花钱花时间，手动触发，脚本不做。

探测器只回填 Endpoint 文件里的客观状态段（保留最近 1–2 条），**绝不触碰 Disposition**。这条分工照搬既有设备台账的做法：机器写机器知道的，人写人知道的。

第一版只探测本机。远端 Host 的 Endpoint 可以手工登记，但跨机执行不在范围内。

## 不变量

- 名册、案例、路由规则、运行痕迹一律不进本仓库。
- 选择理由先写后执行，顺序不可颠倒。
- `routing.md` 不许凭想象写满，规则只能从累积案例中固化；否则它就退化成硬编码分支。
- 本仓库的目录在运行时只读。安装是字节复制，写进去的东西会在下次同步时消失。
- 名册里没有的 Endpoint 就是不存在，不要因为某个 CLI 出名就假设它可用。

## 相关

- `$skill-upgrader`：把攒够证据的规律固化进 `routing.md` 或本文件，走 `patches/` 审计。
- 术语见仓库根 [CONTEXT.md](../../CONTEXT.md)，关键决策见 [docs/adr/](../../docs/adr/)。
