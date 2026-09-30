# Proposal：plan-review 在 goal 里默认跳过（task-explore 侧）

## 背景

`plan-review` 阶段要求「候选收成编号表（Endpoint / Model / 擅长方向 / 依据）供用户圈选」。处在 goal 里时，`SKILL.md`「Goal 里的确认」节已规定每一处要向用户确认、选择或询问的决定都改走 task-goal 的审阅——而审阅本身要派一个审阅者，于是形成嵌套派审。这是「审阅派不出」的一条结构性来源（推断，尚无运行证据）。

## 决定

`plan-review` 节加一段：处在 goal 里时本阶段默认跳过——方案已由 task-goal 审阅收敛，再派名册评审会把审阅套进审阅。用户点名要名册评审时才走。

## 理由

- 该阶段原文已标注「可选——用户不要求则跳过，直接 `decide`」，本改动与既有定位一致，只是把 goal 里的默认值写明确。
- 不删除该阶段（非 goal 场景仍可用），只改 goal 里的默认值。

## 验证

- `python3 -m pytest skills/task-explore -q` 全过。

## 明确不改

`plan-review` 的门禁、`$agent-roster` 委托契约、`phase-plan-review.md`、`design` / `decide` 流程。
