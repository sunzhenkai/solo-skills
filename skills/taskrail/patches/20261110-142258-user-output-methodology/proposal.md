# 以用户认知与决策驱动 task 系列表达

- target: skills/taskrail
- mode: update
- patch: 20261110-142258-user-output-methodology
- risk: medium
- status: proposed

## Intent

将 taskrail / taskflow 的用户展示从固定话术和环节复述改为方法论：以理解、决策和行动需要确定内容，默认摘要并按需展开，只同步用户认知增量，详略与风险匹配。保留 human 确认停点、真阻塞、验证缺口和剩余风险披露；不改变路由、执行适配器或落盘产物结构。

## Conflict check

现有规则要求普通 reference 切换和片间检查点都复述，并为 resume / 完成通知提供固定模板，与本轮增量同步和渐进展开存在冲突，需同步调整。taskflow 已引用 user-report，无需增加第二套表达规则。

## Rationale

用信息价值和用户认知变化驱动展示，可比固定句式适应不同任务复杂度；契约测试锁定正向机制，行为 eval 检查精简后仍保留决策所需信息。

## Files

- skills/taskrail/references/user-report.md：统一表达方法论，移除固定话术和场景字段堆砌。
- skills/taskrail/references/confirm-protocol.md：非停点同步改由用户认知增量触发。
- skills/taskrail/references/contract.md：同步非停点汇报的总契约。
- skills/taskrail/references/intent.md：意图复述按理解与纠偏需要组织。
- skills/taskrail/references/plan.md：方案确认展示决策所需摘要。
- skills/taskrail/references/close.md：完成通知按交付与落地需要展开。
- skills/taskrail/tests/test_user_report_contract.py：守卫摘要、增量、风险和按需展开机制。
- skills/taskrail/tests/test_confirm_contract.py：守卫非停点同步的新触发条件。
- skills/taskrail/tests/test_flow_closure_contract.py：完成通知契约改锚定结果与落地信息。
- skills/taskrail/evals/cases.yaml：更新增量同步案例并补充渐进展开行为案例。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 taskrail 与 taskflow 契约测试、全仓测试、check-names、check-style 和 diff 检查。
- 检查 taskflow 与其他 references 的读者，确认无旧固定复述规则残留。
