# 点名 Role 时使用它的默认 Endpoint

- target: skills/agent-roster
- mode: update
- patch: 20260925-023824-role-default-endpoint
- risk: high
- status: proposed

## Intent

调用方点名 Role、又没写 Endpoint 时，用 `<data_root>/agents/roles.yaml` 里该 Role 的默认 Endpoint，当作已经指定的唯一 Endpoint，走快速路径。没有能用的默认（没配、不在名册、最近一条探测状态含 ❌ 或 ⚠）就问这次用谁，不改走 routing.md 或 Trace。同一句问要不要记成默认；只有明确同意才 `--write`。没点名 Role 时，选人方式不变。不从任务正文推断 Role。模型不进对照表。

## Conflict check

快速路径原来说「画像缺失或不可用时回到完整路由」。Role 解析为 `use` 时，可用性已经在 `resolve_role.py` 里判过，再回到完整路由会把使用者点名的默认盖掉，所以这条退路对 Role 来源关掉。失败分类里「受派方没起来就回到路由」同样会盖掉 Role，改为问这次换谁。

与 ADR 0002 的关系：五个约定名字是词汇，调用方不点名就不归类，不给 Endpoint 打分。`no-scoring` 的「不把任务切成固定枚举」仍然成立。没点 Role 时 `empty-routing-rules` 的自行选人不变。

## Rationale

这是 ADR 0004 的机制：默认 Endpoint 和当场点名 Endpoint 同一级，临时回答不写进对照表。解析与写入做成脚本，退出码和 `verdict` 可单独验收，不靠编排者记规则。

## Files

- `skills/agent-roster/SKILL.md`：选人顺序、角色一节、数据表、失败时的 Role 例外、第五条不变量。
- `skills/agent-roster/references/roles.md`：对照表格式与 `use` / `ask` 判定。
- `skills/agent-roster/scripts/resolve_role.py`：解析与 `--write`。
- `skills/agent-roster/evals/cases.yaml`：增加 `role-names-default-endpoint`。

## Validation

- `git apply --check --recount` 通过。
- `git apply --recount` 后 `git diff --check` 通过。
- `python3 skills/agent-roster/scripts/resolve_role.py --self-check` 通过。
- frontmatter `name` 仍为 `agent-roster`。
- 无主机名、真实 Endpoint、凭据或内部 URL。
