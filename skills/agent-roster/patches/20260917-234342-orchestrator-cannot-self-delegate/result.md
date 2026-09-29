# Result

- target: skills/agent-roster
- mode: update
- patch: 20260917-234342-orchestrator-cannot-self-delegate
- risk: high
- status: applied
- applied-at: 2026-09-17T23:45:50+08:00

## Validation

- `git apply --check --recount`: pass（三个 hunk 分别 offset +1 / +2 / +2）
- `git diff --check`: pass
- target tests: not-available（`evals/cases.yaml` 无 runner，新增两条 case 与既有条目逐字段人工核对，缩进与 `kind` / `judge` / `given` / `expect` 结构一致）
- privacy check: pass（改动文件内无主机名、家目录、项目名、凭据、内部 URL）
- mode check: pass（`update`，未引入 examples/experience 目录，未夹带无关重写）

## Notes

应用后核对到位：`SKILL.md` 委派段第 65 行为受派方身份约束，门禁第 3 条为「整件事暂停」并要求回写 `decision.md`，留痕段第 106 行新增「编排者自己绕过了流程」，不变量段第 155–156 行新增冻结与自任两条；契约文件第 31 行同步为「停下这件事」并补「等待期间也不得改由编排者自己动手」；`evals/cases.yaml` 追加 `no-self-delegation`、`gate-freezes-the-goal`。frontmatter `name` 仍为 `agent-roster`。

触发本轮的真实失败：编排者确认默认执行器不在 PATH 后，既没有提议安装也没有走降级，而是自己顶替受派方改了目标仓库的代码，直到使用者追问才承认跳过了委派与等待门禁。这是同一处门禁的第三次逃逸，前两轮分别封掉了「静默安装」与「未获明确拒绝就降级」，而「不委派、自己动手」始终在两轮的论域之外——两轮都在讨论执行器选择，没有一条约束受派方身份。

本轮据此改了策略：不再逐条枚举被禁止的路径，而是给出两条覆盖全部路径的正向规则（受派方身份、冻结目标而非动作）。另外补上了前两轮缺失的 eval case——同一逃逸能连续发生三次而无人拦住，缺少可验收检查是其中一个原因。

该失败应在使用者侧数据目录记一条 Trace（编排者绕过流程，使用者纠正），不写入本仓库。此外未做：不自动 sync 到各 agent 安装目录，不 commit、不 push。
