# 选人：角色、数据位置与路由

## 角色：点了名就用默认 Endpoint

调用方点名了 Role、又没写 Endpoint 时，先解析这个 Role 的默认 Endpoint。`verdict: use` 走上面的快速路径，`verdict: ask` 停下来问。调用方没点名 Role 时，跳过本节，按下一节自行选人。

约定名字是 developer、planner、reviewer、code-reviewer、designer，一句话语义见 [references/roles.md](./references/roles.md)。调用方可以点自己加的名字。不从任务正文推断该用哪个 Role。本 skill 引用的仓级文档（CONTEXT.md、docs/adr/）只在源仓存在，安装副本不随分发。

```bash
python3 <skill-dir>/scripts/resolve_role.py <role-id>
```

exit 1 是 `verdict: ask`，要问人，不是脚本故障。exit 2 才是对照表或参数坏了，先停下说明，不要当成 ask。

- `verdict: use`：这个 Endpoint 就是使用者已经指定的唯一 Endpoint，走快速路径。解析时已经确认画像在、且最近一条探测状态可用，不要再因「画像不可用就回到完整路由」去枚举候选。`decision.md` 的指定来源写这个 Role，「为什么选它」写成「使用者把这个 Role 的默认 Endpoint 设成了它」。
- `verdict: ask`：问这次用哪个 Endpoint，同一句里问要不要记成这个 Role 的默认。回答里的 Endpoint 用于这次，并走快速路径。回答明确同意记成默认时才 `--write`。只给出 Endpoint、沉默、追问或换话题，对照表保持原样，委派照样继续。
- 调用方同时写了 Role 和 Endpoint：用写明的 Endpoint，不跑上面的脚本。

模型不在对照表里。调用方没给 model 就省略，用该 Endpoint 自己的默认。

```bash
python3 <skill-dir>/scripts/resolve_role.py --write <role-id> <host>/<kind>
```

`--write` 只在明确同意之后执行，并且只接受名册里已有的 Endpoint。这次 Endpoint 来自 Role、委派发出后受派方没起来：问这次换谁，同一句问要不要改默认，不回到完整路由另选。

## 数据在哪

本仓库只有机制，一条真实记录都没有：名册、案例、路由规则、运行痕迹一律不进本仓库。数据位置由 `~/.config/agent-roster/config.yaml` 的 `data_root` 指出（缺省时先问使用者，不要猜）。

| 内容 | 位置 | 谁写 |
| --- | --- | --- |
| Roster（Endpoint 画像） | `<data_root>/agents/<host>/<kind>.md` | 客观段由 Probe 回填，Disposition 由人或 agent 维护 |
| Routing Rule | `<data_root>/agents/routing.md` | Orchestrator 提案、使用者确认后写入，初始为空 |
| Role 默认 Endpoint | `<data_root>/agents/roles.yaml` | 使用者明确同意后由 Orchestrator 写入 |
| Trace（案例） | `<data_root>/agents/traces/<YYYYMMDD>-<slug>.md` | Orchestrator，仅在有教训时 |
| Run（运行痕迹） | `~/.cache/agent-roster/runs/<run-id>/` | 委派时自动落盘，可随时删 |
| Handoff（交接物） | 调用方在发起委派时指定的项目内路径 | 见「回收」 |
| Pattern（通用规律） | 本仓库 `experience/patterns/`，**不随安装分发** | 只在源仓库维护 |
| Example（优秀案例） | 本仓库 `examples/`，随安装分发 | 只在源仓库维护，没有真实案例就保持为空 |

运行位置只有 `SKILL.md`、`references/`、`scripts/`、`examples/` 的字节副本，写进去的东西会在下次同步时消失；`experience/`、`evals/`、`patches/` 连复制都不会发生。所以一条规律要真正生效，必须固化进本文件正文或 `routing.md`——`patterns/` 只是素材，`evals/` 只在源仓库改正文时用来验收。

格式见 [references/endpoint-schema.md](./references/endpoint-schema.md) 与 [references/trace-format.md](./references/trace-format.md)。

references 按当前步骤按需加载，不要预先全读：委派前读 `delegation-contract.md`，写/改画像时读 `endpoint-schema.md`，写 Trace 时读 `trace-format.md`，解析 Role 时读 `roles.md`。

## 路由：选谁

只有需要自行选人时才执行以下完整路由。点了 Role 时不是自行选人：`verdict: use` 走快速路径，`verdict: ask` 停下来问这次用谁。

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
