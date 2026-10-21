# 入口门的子任务 slug 带上 subtasks 这一层

- target: skills/taskflow
- mode: update
- patch: 20261021-205450-subtasks-dir
- risk: low
- status: proposed

## Intent

taskrail 同 id patch 把子任务目录改成 `ongoing/{parent}/subtasks/{sub}/`。入口门本来就把 slug 当成 `tasks/ongoing/` 下的相对路径，所以脚本逻辑不变，只把说明和用例从 `<parent>/<sub>` 改成 `<parent>/subtasks/<sub>`。driver 名仍取 slug 末段，`demo/subtasks/api` 的 driver 是 `api-driver`。

非目标：核对项不变。

## Conflict check

- 与 taskrail 同 id patch 一起用；只改说明和测试，不改判定。

## Rationale

说明和用例还写着旧路径的话，交接时会把入口门指到父任务目录里面。

## Files

- `skills/taskflow/scripts/check_handoff.py`
- `skills/taskflow/tests/test_check_handoff.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 -m pytest skills/taskflow/tests/test_check_handoff.py -q`
