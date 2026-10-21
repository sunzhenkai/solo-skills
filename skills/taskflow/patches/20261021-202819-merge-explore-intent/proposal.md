# 台账模板与交接步骤改指 taskrail

- target: skills/taskflow
- mode: update
- patch: 20261021-202819-merge-explore-intent
- risk: low
- status: proposed

## Intent

task-explore 并入 taskrail（同 id 的 taskrail patch）。taskflow 里指向 task-explore 的四处改指 taskrail：跳过 taskrail 时建最小 `TASK.md` 用的模板、入口门拒绝时的提示语、入口门测试读取的 `handoff.md` 与 `templates.md`、对应 eval。行为不变。

## Conflict check

`check_handoff.py` 只改提示语字符串，核对逻辑不变。`evals/cases.yaml` 叠在另一会话已暂存的版本之上，只改一行。

## Rationale

旧目录删除后这些指针会失效；测试读取路径不改会直接报错。

## Files

- `skills/taskflow/SKILL.md`
- `skills/taskflow/scripts/check_handoff.py`
- `skills/taskflow/tests/test_check_handoff.py`
- `skills/taskflow/evals/cases.yaml`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/taskflow`；`python3 -m pytest skills/taskflow/tests -q`
