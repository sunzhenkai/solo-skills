---
id: 20261128-181200-mock-only-verification-and-contract-check
skill: anti-lazy
mode: update
status: proposed
risk: medium
source: user-feedback-retrospective
created_at: 2026-11-28T18:12:00+08:00
---

# Proposal: 强化 anti-lazy 的跨端契约核对与纯 mock 边界标注

## Trigger & Evidence
- 在前后端全栈排查与修复中，接口字段名、状态枚举、错误码或参数格式容易出现“前端单测 mock 了旧结构、后端单测 mock 了另一套结构，两边单测都绿但联调报错”的假完成。
- 仅靠局部 mock 或静态检查宣称完成时，必须显式标出验证边界与未跑真实链路的项。

## Target Files
- `skills/anti-lazy/SKILL.md`
- `skills/anti-lazy/tests/test_anti_lazy_contract.py`

## Planned Changes
1. 在 `skills/anti-lazy/SKILL.md` 第 2 节补充跨端/跨层契约核对要求：涉及 API、事件或配置结构改动时，核对生产方与消费方的真实类型/schema 与字段对齐，不凭单边 mock 推断契约一致。
2. 在 `skills/anti-lazy/SKILL.md` 第 4 节「替代验证 / 假验证」自检动作中补充：若测试仅依赖 mock 且未经过真实链路或端到端验证，须显式标注验证边界与未覆盖项，不得当作全量通过。
3. 在 `skills/anti-lazy/tests/test_anti_lazy_contract.py` 新增契约测试，锁定上述两项约束。

## Conflict Check
- 同步发起伴随 patch：`session-wrap`（`20261128-181200-enforce-push-gate-and-mock-boundary`）与 `taskflow`（`20261128-181200-worktree-node-deps-guidance`），三者修改各自独立目录，无文件冲突。

## Acceptance Criteria
- `python3 -m unittest discover -s skills/anti-lazy/tests` 通过。
- `make check-names && make check-style` 通过。
