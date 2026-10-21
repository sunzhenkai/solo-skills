# 跟随 pretty-view-html 改名为 pretty-ui

- target: skills/taskrail
- mode: update
- patch: 20261021-195142-pretty-ui-rename
- risk: low
- status: proposed

## Intent

`pretty-view-html` 同轮改名为 `pretty-ui`。把 `references/done.md`「观感验收」里的视觉方向链接，以及两个契约测试里锁定的路径字符串，改成新路径。

非目标：观感验收的内容和门槛不变。

## Conflict check

none

## Rationale

只改链接路径；改后链接目标存在，测试继续锁定该路径。

## Files

- `skills/taskrail/references/done.md`：视觉方向链接
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`、`tests/test_taskrail_contract.py`：路径断言

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 -m pytest skills/taskrail/tests -q`；链接目标文件存在
