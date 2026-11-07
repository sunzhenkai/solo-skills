# 收敛 human 确认边界并堵住绕过入口

- target: skills/taskrail
- mode: update
- patch: 20261107-001842-human-confirmation-boundaries
- risk: high
- status: proposed

## Intent

新根任务先进入 intent，不再从 plan 起步；以 context/current 的意图确认状态区分“criterion 已填写”和“意图已确认”。human 下，已确认的意图、实施方案、交付边界或风险任一变化都重新确认；独立交付拆分、接受未修复的 Blocker / Major、验证不足或缩小交付必须有明确放行。内部切片、普通可逆取舍和 checkbox 进度保持不停。goal 的确认方式与真阻塞规则不变。

非目标：不修改 taskflow，不改变执行适配器，不新增固定线性阶段，不同步安装副本。

## Conflict check

现有 confirm-protocol 已声明意图与实施确认，但 init 和 router 允许 criterion 非空的新任务绕过 intent；decompose 的自动建子任务需调整为 ROADMAP 确认后自动执行；verify / done 的 accepted-recorded 需排除执行者自行接受风险。契约保留动态 references，不增加固定阶段。

## Rationale

以四个已确认边界统一停点可覆盖新增仓库、依赖、契约变化、交付拆分和剩余风险，同时避免每个 reference 都停。脚本初始化、路由文本、模板和契约测试共同约束同一行为，可用状态测试与文本契约验证。

## Files

- skills/taskrail/scripts/task_state.py：根任务从 intake 开始并初始化意图确认状态。
- skills/taskrail/references/confirm-protocol.md：统一四类边界及新增停点。
- skills/taskrail/references/router.md：按意图确认状态路由，而非只看 criterion。
- skills/taskrail/references/intent.md：记录 pending / confirmed / not-required 并在放行后更新。
- skills/taskrail/references/plan.md：明确执行中需要重新确认的触发器。
- skills/taskrail/references/grill.md：用户价值取向的取舍进入确认停点。
- skills/taskrail/references/decompose.md：独立交付结构先确认，内部切片不停。
- skills/taskrail/references/verify.md：风险接受与验证降级的放行规则。
- skills/taskrail/references/done.md：完成清单同步风险接受与验证降级规则。
- skills/taskrail/references/contract.md：热状态包含意图确认状态，新任务入口为 intake。
- skills/taskrail/references/templates.md：TASK 与 context 模板同步。
- skills/taskrail/tests/test_task_state.py：验证 human / goal / 子任务初始状态。
- skills/taskrail/tests/test_confirm_contract.py：守卫总规则与新增停点。
- skills/taskrail/tests/test_intent_contract.py：守卫确认状态路由。
- skills/taskrail/tests/test_explore_contract.py：更新模板入口断言。
- skills/taskrail/tests/test_decompose_contract.py：守卫确认后自动创建子任务。
- skills/taskrail/evals/cases.yaml：增加入口绕过、独立交付和风险接受案例。

## Validation

- 生成机械 unified diff，运行 `git apply --check --recount`。
- 高风险门禁：展示风险与 diff，获得用户明确确认后应用。
- 应用后运行 `git diff --check -- skills/taskrail`。
- 运行 `python3 -m pytest skills/taskrail/tests -q`。
- 运行 `python3 -m pytest skills -q`、`make check-names`、`make check-style`。
- 检查实际 diff 只含本提案声明的 taskrail 生产文件，不含安装镜像或历史 patch。
