# Proposal：goal 模式下的执行器定位（第三批·task-delivery 侧）

## 背景

goal 模式下本 skill 与 task-goal 都声称掌握同一个 task 的完成：本 skill 的 Stage 1–12 跑完整闭环并以 Stage 12「完成报告」收尾，task-goal 自带四状态与完成门。谁写真源没有条款，谁写 `已完成` 也没规定。

## 决定

- 定位：goal 模式下本 skill 是**执行器**，不是完成门。
- 新增「goal 模式的归属」节，写清五件事：task-goal 持四状态 / state-file / 退出点与授权 / 完成门；本 skill 持 Stage 1–12；每轮收口回报（带 `goal-event:` 戳优先，无戳按 task-goal 的事件推断顺序）；**本 skill 不写 `已完成`**；停机口径来自 task-goal，本 skill 的 Stop conditions 只列执行器特有项。
- Stage 12「完成报告」改名「收口报告」，并注明它是交给 task-goal 判完成门的输入。
- 回归门与观感类第 2 条的「完成门 / 完成报告」措辞同步改名。
- 新增 state-file 生产者责任：建任务时把 `goal-state-file:`（默认 `<evidence_root>/goal-state.yaml`）交给 task-goal。
- 观感类中途真人门标注「也是复杂档 B 类降级的唯一集中追认点」——防后续去重时误删（删了复杂档永远无法标完成）。

## 理由

- 本 skill 的自我定位原文是「薄编排层」，但它同时被当完成门用，与其定位矛盾。改为执行器后，角色边界与 task-goal 的声明互为对偶。
- 「不写 `已完成`」是 owner 条款的核心：单一终态写入方，避免两套主循环各标各的。

## 验证

- 全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**。
- `grep -n "已完成" skills/task-delivery/SKILL.md`：只应出现在「不写 `已完成`」的否定句里。

## 明确不改

Stage 1–12 的流程内容、Stop conditions 的执行器特有项、增量验证协议、benchmark 隔离、异源门。
