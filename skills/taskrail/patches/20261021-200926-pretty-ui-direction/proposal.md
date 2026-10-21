# 观感验收的视觉方向改指 pretty-ui 的 direction.md

- target: skills/taskrail
- mode: update
- patch: 20261021-200926-pretty-ui-direction
- risk: low
- status: proposed

## Intent

pretty-ui 同轮重写（`skills/pretty-ui/patches/20261021-200926-fuse-oil-ui-refactoring-ui/`），删除了原样收录的 `references/frontend-design/REFERENCE.md`，视觉方向的方法改由 `references/direction.md` 承担。本 patch 只把 taskrail 指向旧文件的链接、契约测试断言和 eval 描述改到新文件，保持仓内链接有效。

非目标：观感验收各条的含义（方向卡栏目、截图与评审方式）留到下一轮单独 patch 调整。

## Conflict check

- `references/done.md`「观感验收」第一条的链接目标变化，文字不变。
- `tests/test_aesthetic_goal_contract.py` 的路径断言与方法名、`tests/test_taskrail_contract.py` 的路径断言随之更新。
- `evals/cases.yaml` 的 `aesthetic-goal-goal-mode` 只改括号里的读取对象。

## Rationale

链接改指后由契约测试锁定新路径；新文件存在由 pretty-ui 的契约测试保证。

## Files

- `skills/taskrail/references/done.md`
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`
- `skills/taskrail/tests/test_taskrail_contract.py`
- `skills/taskrail/evals/cases.yaml`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills/taskrail/tests -q`；全量 `python3 -m pytest skills tests -q`
