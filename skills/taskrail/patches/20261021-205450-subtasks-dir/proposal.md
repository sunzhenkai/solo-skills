# 子任务放到父任务的 subtasks/ 下

- target: skills/taskrail
- mode: update
- patch: 20261021-205450-subtasks-dir
- risk: low
- status: proposed

## Intent

用户要求子任务放到独立目录，不和父任务的 design 等阶段产物放在一起。目录从 `ongoing/{parent}/{sub}/` 改为 `ongoing/{parent}/subtasks/{sub}/`：`subtasks/` 与父任务的 `wizard/`、`design/`、`approve/` 并列，每个子任务一个目录，里面的布局与父任务相同。

改动只换路径：

- 契约目录树与术语、large-scope 的建法与收尾落点、handoff 传给入口门的 slug、归档时的停留位置。
- `{sub}` 仍全仓唯一，driver 名仍是 `{sub}-driver`。

非目标：拆分规则、继承、停点都不变。

## Conflict check

- 入口门按 slug 拼 `tasks/ongoing/<slug>/TASK.md`，slug 里带 `subtasks` 这一层就能定位，脚本逻辑不用改。taskflow 同 id patch 只改脚本说明和用例里的路径。
- 已有任务如果按旧路径建过子任务，按旧路径继续；新规则只对之后拆出的子任务生效。

## Rationale

父任务目录里阶段产物和子任务混在一层，resume 和归档时不容易分清哪些是本任务的方案、哪些是另一个任务。单独一层 `subtasks/` 之后，父任务的 wizard、design、approve 仍然只属于父任务。

## Files

- `skills/taskrail/references/{contract,large-scope,handoff,archive-reopen}.md`
- `skills/taskrail/tests/test_decompose_contract.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills/taskrail/tests skills/taskflow/tests -q`
