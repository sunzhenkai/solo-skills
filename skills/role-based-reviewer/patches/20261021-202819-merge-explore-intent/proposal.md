# 角色清单里的 task-explore 指针改为 taskrail

- target: skills/role-based-reviewer
- mode: update
- patch: 20261021-202819-merge-explore-intent
- risk: low
- status: proposed

## Intent

task-explore、task-intent 并入 taskrail（同 id 的 taskrail patch）。algo / data / engineer / product 四个角色的「相关 skill」行把 `task-explore` 换成 `taskrail`；测试里说明意图清单出处的注释改指 taskrail `intent.md`。评审规则不变。

## Conflict check

另一会话同时在改 `references/roles/design.md` 与本 skill 的测试（新增视觉规则号断言）；本 patch 只改测试里的一行注释，不碰 design.md。

## Rationale

旧 skill 名删除后指针失效。

## Files

- `skills/role-based-reviewer/references/roles/{algo,data,engineer,product}.md`
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check -- skills/role-based-reviewer`；`python3 -m pytest skills/role-based-reviewer/tests -q`
