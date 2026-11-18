# 收尾改为两轮：清单与带推荐的选项，确认后汇报结果与缺口

- target: skills/session-wrap
- mode: update
- patch: 20261118-170756-two-round-wrap
- risk: high
- status: proposed

## Intent

收尾从一次性报告改为两轮交互：

1. 第一轮列收尾清单，每个发现归入直接执行、需你选择或缺口。结论唯一的事项（含缺口记账）只列出、不提问；有两种以上合理做法的事项，或外部、不可逆的动作，每项一题，给 2–3 个选项，推荐项放首位并附理由。第一轮不下结论，也不单列验证流水。
2. 用户一次回答覆盖本轮清单，确认后按序执行；每题的选择只授权该项，外部动作各自成题并写明目标环境。没有需你选择的项时直接执行。
3. 第二轮输出结论、逐项收尾结果、缺口列表（事实、记在哪、建议处置）与恢复入口。

缺口落点按执行时的任务状态取：未收口写 `context/current.md`「未决问题」；已收口或已归档在 SUMMARY「剩余风险与后续项」追加一行；有 tracker 时写入作为需你选择的一题；都没有时只留在第二轮缺口列表。

非目标：取证范围、分支合入推荐、衍生问题分流、知识落点表与弯路复盘的触发和内容不变。

## Conflict check

- 与原 `plan-synthesis.md`「不写选项 A / B 式选择题」直接冲突，本次改写；原意（不把发现清单丢回用户）保留为反例。
- 原规则「不代写 `SUMMARY.md`」放宽为：已收口任务只允许在「剩余风险与后续项」追加一行；SUMMARY 的撰写仍归 taskrail `close`，与 `taskrail/references/done.md`「其余 `F-n` 已写入 SUMMARY 的剩余风险或后续项」一致。
- 逐项授权保持：push、合入共享分支、部署、删除、清理 worktree、跨机同步、写外部 tracker 仍各自需要用户点名，只是改成用一题承载。
- 其他 skill 未引用本 skill 的「收尾方案 / 额外缺口 / 需单独授权」术语，无跨 skill 悬空引用。仓库 README 的 skill 一行简介随本次同步（不在本 patch 内，属仓级文档）。

## Rationale

实际会话里，旧规则产出的收尾是：先报「可结束」，再单列已核对事实，把 worktree 删除、混合改动提交这类待定事项列成被动的「需单独授权」清单就结束；缺口标「未点名只记账」，但没有记账，也没有写落点（任务已归档，旧规则只定义了 `context/current.md` 一个落点）。用户的目标是收尾与记录缺口两件事，期望流程为：梳理收尾项 → 对拿不准的项给带推荐的选项 → 确认后执行 → 简述结果并重列缺口。改为两轮后，每个待定事项都有可点选的推荐，缺口在任何任务状态下都有落点。

## Files

- skills/session-wrap/SKILL.md：description 与引言改为两轮；第 7 步改为「列收尾清单」；重写「确认与授权」「输出」为两轮模板；删去与第 3 步、第 7 步重复的句子以留在 8KB 内。
- skills/session-wrap/references/plan-synthesis.md：重写为归属判据、提问规则、排序、缺口落点、确认语义、两轮输出与反例。
- skills/session-wrap/references/detour-review.md：两处「收尾方案 / 方案步骤」改为收尾清单的说法。
- skills/session-wrap/tests/test_session_wrap_contract.py：替换三档、单方案与旧输出段名的断言；新增两轮、带推荐的提问、按任务状态记账、反例守卫。
- skills/session-wrap/evals/cases.yaml：改写 9 条与新规则冲突或措辞过时的案例；新增已归档任务缺口落点、两轮汇报两条。

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/session-wrap/tests tests/test_evals_structure.py -q`
- 全量 `python3 -m pytest skills tests -q`；`make check-style`、`make check-names`、`git diff --check`
- 用一个真实收尾场景（已合并 worktree、混合多任务的未提交改动、已归档任务、两条缺口）按新规则手推两轮输出
