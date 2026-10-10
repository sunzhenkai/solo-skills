# human 闸口模板钉走查 + 审阅标题对齐

- target: skills/task-confirm
- mode: update
- patch: 20261010-223500-walkcheck-template-closeout
- risk: low
- status: proposed

## Intent

收口异源评审缺口：human 强制走查已有散文规则，但输出模板无固定「走查：」行，执行时结论易被吃掉；审阅节标题仍只写 approve，与 wizard 定稿点名派审不一致；审阅表仍写「方案/步骤」未与流程总览用语对齐。

本 patch：闸口输出模板加走查行；审阅标题覆盖 wizard 定稿；审阅表改为「方案/流程总览闸口」；契约测试钉住模板字面量。

## Conflict check

none —— 承接已 apply 的 20261010-215414 / 221500 / 222000 规则，只补执行面与可观测契约，不改机制。

## Rationale

异源评审（Request changes）要求：走查结论进闸口模板、explore/template/handoff 与 contract 贯通；本 patch 按最小收口清单落地，可经契约测试钉住。

## Files

- `skills/task-confirm/SKILL.md` — 模板走查行、审阅标题与表用语
- `skills/task-confirm/tests/test_task_confirm_contract.py` — 断言模板与标题

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 -m pytest skills/task-confirm/tests -q`
