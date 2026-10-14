---
name: agent-roster
description: 维护跨机器的 agent 端点名册（谁在哪台机器上、擅长什么），并据此把一件事委派给合适的 agent 执行、回收产出、留下可复用案例。用于需要让另一个 agent 定计划、做评审或实施，也用于登记、探测、查询可用 agent；不实现被委派 agent 自身的能力。
---

# Agent Roster

## 一次委派的完整顺序

```text
- [ ] 1 路由：读 routing.md → 读相关 Endpoint 画像 → 检索相关 Trace
- [ ] 2 建 Run 目录，写 decision.md（必须早于第 3 步）
- [ ] 3 委派：检查执行器在不在 → 按契约发出，权限按委派性质定
- [ ] 4 回收：Handoff 落到项目里，Run 痕迹留在缓存
- [ ] 5 留痕：只在有教训时写 Trace
- [ ] 6 固化：刚写过 Trace 才做这一步，够门槛就停下来提案
```

第 2 步与第 6 步的位置是本 skill 的不变量，不可重排。

## 快速路径

使用者明确指定唯一 Endpoint 且任务线性时，只读 `routing.md`、该 Endpoint 画像和相关 Trace，不枚举其他候选；画像缺失或不可用时回到完整路由。`decision.md` 可压缩为指定来源、可用性证据、权限、Handoff，但「为什么选它」仍须可复用；acpx、权限、回收与留痕门禁不变。

## 数据在哪

本仓库只有机制，一条真实记录都没有：名册、案例、路由规则、运行痕迹一律不进本仓库。数据位置由 `~/.config/agent-roster/config.yaml` 的 `data_root` 指出（缺省时先问使用者，不要猜）。

| 内容 | 位置 | 谁写 |
| --- | --- | --- |
| Roster（Endpoint 画像） | `<data_root>/agents/<host>/<kind>.md` | 客观段由 Probe 回填，Disposition 由人或 agent 维护 |
| Routing Rule | `<data_root>/agents/routing.md` | Orchestrator 提案、使用者确认后写入，初始为空 |
| Trace（案例） | `<data_root>/agents/traces/<YYYYMMDD>-<slug>.md` | Orchestrator，仅在有教训时 |
| Run（运行痕迹） | `~/.cache/agent-roster/runs/<run-id>/` | 委派时自动落盘，可随时删 |
| Handoff（交接物） | 调用方在发起委派时指定的项目内路径 | 见「回收」 |
| Pattern（通用规律） | 本仓库 `experience/patterns/`，**不随安装分发** | 只在源仓库维护 |
| Example（优秀案例） | 本仓库 `examples/`，随安装分发 | 只在源仓库维护，没有真实案例就保持为空 |

运行位置只有 `SKILL.md`、`references/`、`scripts/`、`examples/` 的字节副本，写进去的东西会在下次同步时消失；`experience/`、`evals/`、`patches/` 连复制都不会发生。所以一条规律要真正生效，必须固化进本文件正文或 `routing.md`——`patterns/` 只是素材，`evals/` 只在源仓库改正文时用来验收。

格式见 [references/endpoint-schema.md](./references/endpoint-schema.md) 与 [references/trace-format.md](./references/trace-format.md)。

references 按当前步骤按需加载，不要预先全读：委派前读 `delegation-contract.md`，写/改画像时读 `endpoint-schema.md`，写 Trace 时读 `trace-format.md`。

## 路由：选谁

只有需要自行选人时才执行以下完整路由。

1. 读 `routing.md`。为空就跳过——规则只能从累积案例中固化，凭想象写满会让它退化成硬编码分支。
2. 读候选 Endpoint 的画像，只读与当前任务相关的那几个。
3. 检索相关 Trace（按 Agent Kind 与任务关键词），重点看失败与返工的那些。
4. **在执行之前**先建 Run 目录，`<run-id>` 取 `<YYYYMMDD-HHMMSS>-<slug>`，`<slug>` 用几个词概括任务：

   ```bash
   run_id="$(date +%Y%m%d-%H%M%S)-<slug>"
   mkdir -p ~/.cache/agent-roster/runs/"$run_id"
   ```

   再把决策写进该目录下的 `decision.md`，四件事缺一不可：**候选有谁**、**选了谁**、**为什么选它**、**依据是什么**（读过哪些画像与哪几条 Trace）。「为什么选它」将来要原样搬进 Trace 再固化成规则，所以要写成脱离本次任务也成立的一句话——「它在长上下文重构上翻车少」可以固化，「这次是重构」不行。事后补写的理由会让后续学习学到编造的故事，等于没写。
5. 证据不足或没有合适候选时直接问使用者。名册里没有的 Endpoint 就是不存在，不要因为某个 CLI 出名就假设它可用。

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
- **可写**：仅实施类委派。发起前必须确认工作目录处于干净状态，否则先停下来问。

只读委派下受派方无法写文件，所以它的产出由 Orchestrator 从结果文本落盘到指定的 Handoff 路径——这条约束顺带保证了「定计划」这类委派永远不会偷偷动到代码。

## 回收：产出与交接

- Run 痕迹留在 `~/.cache/`，**不进任何 git 仓库**。它量大、含完整对话，且极易混入敏感内容。
- Handoff 落在项目里调用方指定的路径。它是真正的工作成果，应该被看见、被评审、被提交。
- 每次委派都必须显式说明期望产出什么。说不清要什么产出的委派，说明任务本身还没想清楚。
- 串接多次委派时，下一棒读的是上一棒的 Handoff 文件，不是把上一棒的完整输出塞进 prompt。

### 失败、超时与返工

`failed` 和 `timeout` 不是再跑一次就能消化的事。先分清是哪一类，再决定动作：

- **受派方没起来**（适配器报错、登录态失效、额度耗尽）→ 不要重试同一个 Endpoint。先跑 L1/L2 探测确认它是不是真的不可用，再回到路由换候选或问使用者。
- **起来了但没跑完**（timeout）→ 可以缩小范围重发一次，把已有的部分产出当输入。同一个 Endpoint 只重发一次，还不行就换人。
- **跑完了但产出不对** → 不要重发。先判断是 prompt 没说清还是人选错了：前者改 prompt 重来，后者回到路由重选，并在 `decision.md` 末尾追加一句改判说明——不要改写原来那段理由。

三类都要写 Trace，且要在 Trace 里写明是哪一类。「超时了」不是教训，「这个 Endpoint 在这类任务上会超时」才是。

## 留痕：什么时候写 Trace

只在以下情形写，例行成功不写——否则有用的教训会被「派给 X，成功」淹没：

- 委派失败、超时，或结果需要返工
- 使用者纠正了选人决定
- 编排者自己绕过了流程：自任受派方，或越过门禁的等待继续推进
- 结果明显超出预期
- 用了新的委派方式或新的 Endpoint

字段见 [references/trace-format.md](./references/trace-format.md)。其中「为什么选它」是唯一能在将来固化成 Routing Rule 的东西，必须从 `decision.md` 原样搬过来，不要重写。

## 固化：什么时候把案例变成规则

攒着不用的 Trace 只是历史。固化（Promotion）是唯一能让选人变准的动作，而它不会自动发生——必须有人在固定时刻检查。

**时机**：写完一条 Trace 之后立即检查，其他时候不查。尤其不要在路由途中插入这个判断，那时候使用者在等结果。

检查用 `scripts/promotion_check.py`（同一句「为什么选它」跨 Trace 精确计数，达门槛打印提案草稿）；脚本只负责把「没人去数」补上，提案与写入仍走下面的确认门禁。

**门槛**：同一个「为什么选它」的理由，在**不同任务**的 Trace 里复现两次以上。不是「同类任务攒够几条」——Trace 只在有教训时才写，按任务分类计数永远凑不齐。这个 2 和 `experience/patterns/` 的准入门槛是同一个数，不用记两套。

**动作**：攒够了就停下来向使用者提案，说清是哪几条 Trace、复现的是哪句理由、建议写成什么规则。使用者确认后按去向分两条路：

- 规则带 Host 名、只对当前使用者成立 → 直接写进 `routing.md`。
- 结论已脱敏、换台机器换个项目仍然成立 → 走 `$skill-upgrader` 的 `patches/` 审计，进本文件正文或 `patterns/`。

分野的理由见 [ADR 0003](../../docs/adr/0003-promotion-splits-by-destination.md)。攒够了却不提案，和凭空编规则一样有害：前者让系统永远停在现读现判，后者让它学到假的东西。

## 名册维护

```bash
python3 <skill-dir>/scripts/probe_endpoints.py            # L1：装没装、什么版本
python3 <skill-dir>/scripts/probe_endpoints.py --level 2  # L2：ACP 适配器能不能握手
python3 <skill-dir>/scripts/probe_endpoints.py --render   # 输出可粘贴的 Markdown 状态块
python3 <skill-dir>/scripts/probe_endpoints.py --write    # 直接回填画像「探测状态」段（L3 记录永不被挤掉）
```

探测分三层，失败时要能区分三种完全不同的处置：

1. **L1 存在性** — CLI 在不在 PATH、什么版本。零成本，随时可跑。
2. **L2 握手** — 起 ACP 适配器走完 `initialize` 就断开。零 token，能确认适配器真的拉得起来。
3. **L3 冒烟** — 真发一句 prompt，确认登录态、额度与模型可用。花钱花时间，手动触发，脚本不做。

探测只回填 Endpoint 文件的客观状态段，**Disposition 归人维护**，格式见 [references/endpoint-schema.md](./references/endpoint-schema.md)。

第一版只探测本机。远端 Host 的 Endpoint 可以手工登记，但跨机执行不在范围内。

## 不变量

正文里最容易被绕过的四条，执行途中逐条自查：

- 选择理由先写后执行，顺序不可颠倒。
- 受派方只能是名册里的 Endpoint，编排者不得自任——正跑在同名 Agent Kind 上也不例外。
- 未安装 `acpx` 时先停下并提议安装：未获确认不得安装，未获**明确拒绝**不得降级；阻塞期间冻结的是任务目标，不是某一个动作。
- 固化条件攒够时必须提案，不许继续沉默；提案与写入之间必须有使用者确认。

## 相关

- `$skill-upgrader`：把脱敏规律写进本文件或 `patterns/` 时的 `patches/` 审计入口。
- 术语见仓库根 [CONTEXT.md](../../CONTEXT.md)，关键决策见 [docs/adr/](../../docs/adr/)。
