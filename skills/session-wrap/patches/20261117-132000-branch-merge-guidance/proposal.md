# 补充分支合入主推荐

- target: skills/session-wrap
- mode: update
- patch: 20261117-132000-branch-merge-guidance
- risk: medium
- status: proposed

## Intent

收尾发现未合并分支时，根据仓库硬规则、已有 MR/PR、用户本次选择与长期习惯、CI/评审要求和提交结构，给出一个明确的合入主推荐。覆盖 MR/PR、squash、merge commit、rebase 与直接合入，保持执行前逐项授权；不改变 session-wrap 的只读定位。

## Conflict check

none。实际 MR/PR 操作仍由 repo-manager 等既有机制承担，session-wrap 只负责证据核对、推荐和路由。

## Rationale

原有内容只提示未合并分支和合并授权，无法帮助用户选择合入方式。新增决策顺序与输出字段可通过文本契约和行为案例验证。

## Files

- skills/session-wrap/SKILL.md：增加分支合入路由和主推荐输出。
- skills/session-wrap/tests/test_session_wrap_contract.py：锁定推荐依据、方式选择与授权边界。
- skills/session-wrap/evals/cases.yaml：增加 squash、merge commit、已有 MR 和用户习惯场景。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行目标测试、evals 结构检查、`git diff --check`、名称与风格检查及全部 skill 测试。
