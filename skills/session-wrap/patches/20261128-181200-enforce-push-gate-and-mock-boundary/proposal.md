---
id: 20261128-181200-enforce-push-gate-and-mock-boundary
skill: session-wrap
mode: update
status: proposed
risk: medium
source: user-feedback-retrospective
created_at: 2026-11-28T18:12:00+08:00
---

# Proposal: 强化 session-wrap 的 push 门禁与发布前验证边界说明

## Trigger & Evidence
- 最近一次全栈排查与收尾中，推送前需严格遵守 `commit-push` 的密钥扫描与前置检查，不应仅作口头路由。
- 在发布/部署只读核对环节，若测试仅靠 mock 通过、缺少真实环境或端到端验证，未标明验证边界容易误判已可放手。

## Target Files
- `skills/session-wrap/SKILL.md`
- `skills/session-wrap/references/release-deploy.md`
- `skills/session-wrap/tests/test_session_wrap_contract.py`

## Planned Changes
1. 在 `skills/session-wrap/SKILL.md` 第 3 节「路由执行」中明确：提交/推送**必须先读取并遵守 `commit-push`**，跑完其前置检查与密钥扫描门禁后再执行，不跳过或简化。
2. 在 `skills/session-wrap/references/release-deploy.md` 第 2 节「只读核对」中补充验证边界要求：若仅在 mock/单测环境下通过而缺真实联调或端到端验证，须显式标注验证边界与未覆盖风险。
3. 在 `skills/session-wrap/tests/test_session_wrap_contract.py` 新增契约测试，锁定上述两项约束。

## Conflict Check
- 同步发起伴随 patch：`anti-lazy`（`20261128-181200-mock-only-verification-and-contract-check`）与 `taskflow`（`20261128-181200-worktree-node-deps-guidance`），三者修改各自独立目录，无文件冲突。
- 保留 `SKILL.md` 中既有 `commit-push` 引用及非直接执行门禁约束，不触发 `test_no_action_without_confirmation` 负向断言。

## Acceptance Criteria
- `python3 -m unittest discover -s skills/session-wrap/tests` 通过。
- `make check-names && make check-style` 通过。
