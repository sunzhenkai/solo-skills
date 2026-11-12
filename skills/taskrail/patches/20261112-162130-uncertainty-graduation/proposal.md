# 未决问题与待明确区

- target: skills/taskrail
- mode: update
- patch: 20261112-162130-uncertainty-graduation
- risk: medium
- status: proposed

## Intent

在现有动态路由中区分可准确提问的未决问题（U-n）与尚不能准确提问的待明确区（F-n）。未决问题按现有 references 解决；新证据使待明确区可准确提问时毕业为未决问题。PLAN 和 ROADMAP 不提前展开模糊未知，任务完成只受会影响 criterion 的未决问题约束。

不引入 issue tracker、新 current_ref、一会话一票、强制 HITL 或自动 push。

## Conflict check

保留 taskrail 的端到端交付、goal 连续推进、grill 先查自答、direct / OpenSpec 执行和现有热状态预算。U-n / F-n 只存于 context/current.md，决定仍写 decisions.md，交付结构仍只写 ROADMAP.md，不形成第二状态源。

## Rationale

现有 PLAN 已要求不提前细化后续步骤，但缺少可恢复的分类与毕业契约。显式区分 U-n / F-n 可减少过早拆分，同时让跨会话恢复知道下一项关键未知及其证据落点。改动可用文本契约测试和声明式 eval 验证。

## Files

- skills/taskrail/SKILL.md：增加未决问题与待明确区的核心不变量。
- skills/taskrail/references/contract.md：定义术语、唯一落点和生命周期。
- skills/taskrail/references/templates.md：补 context/current.md 模板。
- skills/taskrail/references/grill.md：分类、解决、毕业与失效规则。
- skills/taskrail/references/router.md：未决项选择和待明确区最小探索。
- skills/taskrail/references/plan.md：模糊未知只写触发条件。
- skills/taskrail/references/design.md：未决节只引用 U-n / F-n。
- skills/taskrail/references/done.md：增加关键未决问题完成门。
- skills/taskrail/references/close.md：剩余待明确区写入剩余风险或后续项。
- skills/taskrail/tests/test_uncertainty_contract.py：新增文本契约测试。
- skills/taskrail/evals/cases.yaml：增加毕业与剩余雾区收口案例。

## Validation

- 应用前运行 git apply --check --recount。
- 应用后运行 git diff --check -- skills/taskrail。
- 运行 python3 -m pytest skills/taskrail/tests -q。
- 运行 python3 -m pytest skills -q。
- 运行 make check-names 与 make check-style。
- 用通用案例核对 U-n 解决、F-n 毕业、热状态无重复和无关 F-n 不阻塞 close。
