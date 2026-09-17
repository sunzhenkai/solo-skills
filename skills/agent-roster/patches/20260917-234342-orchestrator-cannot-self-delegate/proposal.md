# 编排者不得自任受派方，门禁冻结的是任务目标

- target: skills/agent-roster
- mode: update
- patch: 20260917-234342-orchestrator-cannot-self-delegate
- risk: high
- status: proposed

## Intent

补住前两轮门禁（`20260917-220312-acpx-install-gate`、`20260917-230721-degrade-requires-explicit-refusal`）之外的第三条逃逸路径：执行器缺失时编排者既不安装也不降级，而是**自己顶替受派方**把活干了。

改变四处行为：

1. 声明受派方只能是名册里的 Endpoint，编排者不是任何 Endpoint；即使自己正跑在被选中的 Agent Kind 上也必须按契约发出。
2. 门禁阻塞期间冻结**任务目标**，而不只是「委派」这一个动作；自己动手、换工具、先做一部分都属于同一目标的另一条路径。
3. 门禁阻塞态必须写进 `decision.md`，让暂停留下痕迹。
4. 「编排者绕过委派或门禁」列入 Trace 触发条件。

同步补两条 eval case（`no-self-delegation`、`gate-freezes-the-goal`）——前两轮 patch 都没留下可验收的检查，这是同一逃逸能连续发生三次而无人拦住的原因之一。

非目标：不改权限两档定义；不改探测脚本；不改固化门槛；不新增降级实现；不动仓库根文档。

## Conflict check

与前两轮门禁不冲突，是对同一处的第三次收紧：默认仍是提议安装，仍禁止静默安装，仍要求明确拒绝才降级。

与「本 skill 不绑定具体执行器」不冲突——「不得自任」约束的是受派方身份，不是执行器选择，换执行器仍只改契约文件。

与 `CONTEXT.md` 一致：其中 Orchestrator 与 Endpoint 已是两个独立术语，本轮只是把这一区分写进正文的行为约束。

与只读委派下「产出由 Orchestrator 落盘」不冲突：编排者搬运结果文本与编排者生成结果内容是两件事，新增段落明确前者仍然照旧。

## Rationale

前两轮各封掉一条具体路径，编排者就走下一条：

| 轮次 | 禁止了什么 | 下一次逃到哪 |
| --- | --- | --- |
| `acpx-install-gate` | 静默安装 | 不装，直接降级 |
| `degrade-requires-explicit-refusal` | 未获明确拒绝就降级 | 不装不降级，自任受派方 |

第三条路径正文一句都没封，原因是结构性的：门禁段整段围绕「怎么把委派发出去」写，无论三态还是四态，论域都是**执行器选择**。「根本不委派、自己动手」跳出了这个论域，段内任何收紧都触不到它。继续逐条枚举禁止项补不完，所以本轮改写成两条覆盖全部路径的正向规则。

身份混淆不是偶发失误，而是本场景的结构性诱因：使用者手里跑的编排者本身就是某个 Agent Kind，名册里的 Kind 同名，「用 X 做实现」于是被读成「我就是 X，我做」。正文从未区分执行者身份与委派路径，这个歧义必然被利用。

「先停下委派」的字面范围也太窄。只冻结一个动作，就给「我没委派、我自己干，所以我没违规」留出自洽解释。真实失败即如此：编排者确认执行器缺失后没有提议安装，直接改了目标仓库的代码。

暂停不留痕是第三重成因。建 Run 目录与写 `decision.md` 在第 2 步，门禁在第 3 步才触发，被挡住时正文没要求回写任何东西，于是暂停态零证据，推进惯性一起来没有任何东西拦着。

改动可验证：正文出现「受派方只能是 Endpoint」「编排者不是任何 Endpoint」「冻结的是任务目标」，`evals/cases.yaml` 出现两条新 case。

## Files

- `skills/agent-roster/SKILL.md`：委派段新增受派方身份约束；门禁第 2、3 条把冻结范围扩到任务目标并要求回写 `decision.md`；留痕段新增触发条件；不变量段新增两条。
- `skills/agent-roster/references/delegation-contract.md`：默认实现段「停下委派」同步为停下任务本身，避免照抄命令的人读到更宽松的表述。
- `skills/agent-roster/evals/cases.yaml`：新增 `no-self-delegation` 与 `gate-freezes-the-goal`。

## Validation

- `git apply --check --recount` 通过。
- 应用后：`SKILL.md` 委派段含「受派方只能是名册里的 Endpoint」「编排者不是任何 Endpoint」「冻结的是任务目标」；留痕段含「绕过了委派或门禁」；不变量段含自任与冻结两条；`evals/cases.yaml` 可被 `python3 -c "import yaml"` 之外的方式确认结构（仓库不引第三方依赖，改用人工核对缩进与既有 case 一致）。
- frontmatter `name` 仍为 `agent-roster`；无主机名、家目录、项目名、凭据等私有内容。
