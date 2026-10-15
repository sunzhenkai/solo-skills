---
id: agent-roster
name: agent-roster
description: 维护跨机器的 agent 端点名册（谁在哪台机器上、擅长什么），并据此把一件事委派给合适的 agent 执行、回收产出、留下可复用案例。用于需要让另一个 agent 定计划、做评审或实施，也用于登记、探测、查询可用 agent；调用方点名 Role 且未写 Endpoint 时，用该 Role 的默认 Endpoint。也承接原 agent-roster-flow：按 Stage 编排跨 agent 任务（理解、定方案、方案评审、实现、可选代码评审、收尾），用于多 agent 工作流、跨 agent 分步选人、每步选 Endpoint 和模型时走 flow 模式。普通单次修复不要加载 flow。不实现被委派 agent 自身的能力。
---

# Agent Roster

## flow 模式（原 agent-roster-flow）

使用者要按 Stage 串起多 agent 工作流（每段确认 Endpoint + Model 或 human，执行才委派）时，读 [references/flow.md](references/flow.md)；否则不加载。

## 一次委派的完整顺序

```text
- [ ] 1 选人：没点 Role 时读 routing.md → 读相关 Endpoint 画像 → 检索相关 Trace。点了 Role 且没写 Endpoint 时跑 resolve_role.py：use 走快速路径，ask 停下来问这次用谁
- [ ] 2 建 Run 目录，写 decision.md（必须早于第 3 步）
- [ ] 3 委派：检查执行器在不在 → 按契约发出，权限按委派性质定
- [ ] 4 回收：Handoff 落到项目里，Run 痕迹留在缓存
- [ ] 5 留痕：只在有教训时写 Trace
- [ ] 6 固化：刚写过 Trace 才做这一步，够门槛就停下来提案
```

第 2 步与第 6 步的位置是本 skill 的不变量，不可重排。

## 快速路径

使用者明确指定唯一 Endpoint 且任务线性时，只读 `routing.md`、该 Endpoint 画像和相关 Trace，不枚举其他候选；画像缺失或不可用时回到完整路由。`decision.md` 可压缩为指定来源、可用性证据、权限、Handoff，但「为什么选它」仍须可复用；acpx、权限、回收与留痕门禁不变。

## 角色：点了名就用默认 Endpoint

点了 Role 且未写 Endpoint、或要按数据选人时，先读 [references/selection.md](references/selection.md)（角色默认 Endpoint、数据位置、路由规则）。

## 数据在哪

名册、画像、Trace、Run 目录的位置见 [references/selection.md](references/selection.md)。

## 路由：选谁

完整路由（读 routing.md、画像、Trace，选谁与为什么）见 [references/selection.md](references/selection.md)。

## 委派：怎么派

委派通过一层适配契约发出，本 skill 不绑定具体执行器。契约字段、命令形态、受限清单与降级步骤见 [references/delegation-contract.md](./references/delegation-contract.md)；受控执行有入口脚本 `scripts/delegate.py`（run 目录 + decision.md + timeout 兜底一条命令），状态判定用 `scripts/run_status.py`。

受派方只能是名册里的 Endpoint。Orchestrator 不是其中任何一个——即使自己正跑在被选中的那个 Agent Kind 上，也必须按契约把任务发出去，不能由自己顶上。「交给 codex 做实施」说的是委派路径，不是执行者身份；把两者混为一谈，这次委派就等于没有发生，既没有 Run 痕迹，也没有可复现的选人依据。

正式委派必须**受控执行**：Endpoint+模型组合无 L3 成功记录时先冒烟；`timeout` 必填；启动时写 `run-dir/status.json` 并记录 PID，状态判定用 `scripts/run_status.py <run-id>`，不用 `pgrep` 或肉眼读事件流（细节见 [references/delegation-contract.md](./references/delegation-contract.md)「受控执行」）。

默认执行器是 `acpx`。**每次**委派前都检查它是否在 PATH——上一次委派怎么走不构成本次的依据：

1. 已安装：按契约发出。
2. 未安装：**先停下这件事**，向使用者提议安装（方式以 https://acpx.sh 为准），然后等回答。不要静默安装。
3. 使用者还没回答：**整件事暂停**，把「卡住了、在等什么」写进 `decision.md`。冻结的是任务目标本身，不是「委派」这一个动作——自己动手做、换个工具做、先做掉一小部分，都是通往同一目标的另一条路径，一样不许走。沉默、追问、话题转移都不是拒绝，此时不得改走降级。
4. 使用者明确拒绝：先把受限清单说清，再走降级，并把这次拒绝记进 `decision.md`——它只对本次委派有效。不要把降级说成与默认执行器对等。

权限只有两档，按委派性质定，不要逐次商量：

- **只读**（默认）：定计划、评审、调研、排查。受派 Endpoint 不许改工作目录里的任何文件。
- **可写**：仅实施类委派。发起前必须确认工作目录处于干净状态，否则停下，说明哪些文件有未提交改动（受派方会改到用户的改动，属真阻塞）。

只读委派下受派方无法写文件，所以它的产出由 Orchestrator 从结果文本落盘到指定的 Handoff 路径——这条约束顺带保证了「定计划」这类委派永远不会偷偷动到代码。

## 回收：产出与交接

- Run 痕迹留在 `~/.cache/`，**不进任何 git 仓库**。它量大、含完整对话，且极易混入敏感内容。
- Handoff 落在项目里调用方指定的路径。它是真正的工作成果，应该被看见、被评审、被提交。
- 每次委派都必须显式说明期望产出什么。说不清要什么产出的委派，说明任务本身还没想清楚。
- 串接多次委派时，下一棒读的是上一棒的 Handoff 文件，不是把上一棒的完整输出塞进 prompt。

### 失败、超时与返工

`failed` 和 `timeout` 不是再跑一次就能消化的事。先分清是哪一类，再决定动作：

- **受派方没起来**（适配器报错、登录态失效、额度耗尽）→ 不要重试同一个 Endpoint。先跑 L1/L2 探测确认它是不是真的不可用。这次 Endpoint 来自 Role 时，按「角色」一节问这次换谁；否则回到路由换候选或问使用者。
- **起来了但没跑完**（timeout）→ 可以缩小范围重发一次，把已有的部分产出当输入。同一个 Endpoint 只重发一次，还不行就换人。
- **跑完了但产出不对** → 不要重发。先判断是 prompt 没说清还是人选错了：前者改 prompt 重来，后者回到路由重选，并在 `decision.md` 末尾追加一句改判说明——不要改写原来那段理由。

三类都要写 Trace，且要在 Trace 里写明是哪一类。「超时了」不是教训，「这个 Endpoint 在这类任务上会超时」才是。

## 留痕：什么时候写 Trace

第 5 步写 Trace 的条件与格式见 [references/maintenance.md](references/maintenance.md)。

## 固化：什么时候把案例变成规则

第 6 步固化门槛与提案流程见 [references/maintenance.md](references/maintenance.md)。

## 名册维护

登记、探测、更新名册时读 [references/maintenance.md](references/maintenance.md)。

## 不变量

正文里最容易被绕过的五条，执行途中逐条自查：

- 选择理由先写后执行，顺序不可颠倒。
- 受派方只能是名册里的 Endpoint，编排者不得自任——正跑在同名 Agent Kind 上也不例外。
- 未安装 `acpx` 时先停下并提议安装：未获确认不得安装，未获**明确拒绝**不得降级；阻塞期间冻结的是任务目标，不是某一个动作。
- 固化条件攒够时必须提案，不许继续沉默；提案与写入之间必须有使用者确认。
- 点了 Role 就用它的默认 Endpoint；没有能用的默认就问这次用谁，不改走路由；没得到明确同意不改对照表。

## 相关

- `$skill-upgrader`：把脱敏规律写进本文件或 `patterns/` 时的 `patches/` 审计入口。
- 术语与关键决策的原文（CONTEXT.md、docs/adr/）在源仓 `docs/agent-roster/`，安装副本不随分发。
