# human 意图与实施方案确认、非停点进度复述

- target: skills/taskrail
- mode: update
- patch: 20261027-172511-human-intent-plan-confirmation
- risk: high
- status: proposed

## Intent

让 human 任务在意图形成或变更后、首次 execute 前及实施方案实质变更后分别等待用户明确确认。goal 不增加人工停点。所有未命中停点的环节切换用简短复述同步已完成事项、当前判断和下一动作，不提问、不等待，也不把复述记为确认。

保留动态路由、现有 approve 的高风险职责、taskflow 执行适配器及危险动作门禁。不新增 reference、TASK 字段或依赖。

## Conflict check

实施方案确认属于现有 plan 完成门，不扩大 approve，因此不冲突于 taskflow 的 direct 不需要 approve。确认只影响 reference 的放行，不为 human 增加每个 reference 的固定停顿。子任务继承已确认意图与范围内 approve，但首次 execute 前仍确认自己的当前 PLAN，避免未展开方案被父任务空批。

## Rationale

当前 human 可按需跳过意图确认，PLAN 也没有独立的用户确认完成门，导致清晰但未经用户确认的目标和方案可一路实施。新规则把人工确认与自动进度复述分开，既保留普通可逆事项的自动推进，也让用户能分别纠正目标和实施方案。确认记录落在 PLAN，可在 resume 时核对并在实质变更后失效。

## Files

- skills/taskrail/references/intent.md：human 新意图与变更必须确认，resume 规则同步。
- skills/taskrail/references/plan.md：首次 execute 前和方案实质变更后的确认门与失效规则。
- skills/taskrail/references/confirm-protocol.md：两类确认、子任务边界和非停点复述。
- skills/taskrail/references/user-report.md：确认与普通决定、进度复述的表达边界。
- skills/taskrail/references/templates.md：PLAN 实施确认记录。
- skills/taskrail/references/router.md：execute 前检查 PLAN 完成门。
- skills/taskrail/references/contract.md：确认属于现有 reference 完成门，不新增固定阶段。
- skills/taskrail/evals/cases.yaml：human、goal、方案失效、子任务与非停点复述案例。
- skills/taskrail/tests/test_intent_contract.py：意图确认守卫。
- skills/taskrail/tests/test_confirm_contract.py：PLAN 确认门与记录守卫。
- skills/taskrail/tests/test_user_report_contract.py：非停点复述守卫。
- skills/taskrail/tests/test_decompose_contract.py：子任务确认边界守卫。

## Validation

- 生成候选副本的机械 unified diff，不直接编辑生产稿。
- 应用前运行 `git apply --check --recount`，检查隐私、路径与改动范围。
- high 风险：展示摘要和 diff，获得用户明确确认后再应用。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m pytest skills/taskrail/tests skills/taskflow/tests -q`。
- 运行 `python3 -m pytest skills tests -q`、`make check-names`、`make check-style`。
- 核对最终 diff 与本 patch 一致；不自动 sync、commit 或 push。
