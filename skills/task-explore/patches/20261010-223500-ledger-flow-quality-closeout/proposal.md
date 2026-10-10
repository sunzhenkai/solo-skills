# 台账/handoff 贯通流程总览与质量属性

- target: skills/task-explore
- mode: update
- patch: 20261010-223500-ledger-flow-quality-closeout
- risk: low
- status: proposed

## Intent

收口异源评审缺口：contract 要求流程总览快照随 handoff 进 driver，phase-handoff 未写明写入 `proposal.md`；task-template / cmd-new 仍登记「步骤」；phase-explore 步骤 3 的 grill 未覆盖列表漏「质量目标」。

本 patch：handoff 明确流程总览进 driver `proposal.md`；template 与 cmd-new 改为质量属性 + 流程总览；explore 步骤 3 与步骤 5 对齐；契约测试钉住。

## Conflict check

none —— 承接已 apply 的 20261010-215414 / 221500 / 222000 规则，只补执行面与可观测契约，不改机制。

## Rationale

异源评审（Request changes）要求：走查结论进闸口模板、explore/template/handoff 与 contract 贯通；本 patch 按最小收口清单落地，可经契约测试钉住。

## Files

- `skills/task-explore/references/phase-explore.md` — 步骤 3 补质量目标
- `skills/task-explore/references/task-template.md` — 方案节字段对齐
- `skills/task-explore/references/cmd-new.md` — new 登记字段对齐
- `skills/task-explore/references/phase-handoff.md` — 流程总览进 proposal.md
- `skills/task-explore/tests/test_task_explore_contract.py` — 守卫断言

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 -m pytest skills/task-explore/tests -q`
