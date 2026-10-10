# approve 阶段（必经）

进入本阶段后执行。未绑定则先回到 `SKILL.md` 的绑定规则。

合并原 `plan-review` + `decide`：**结构门 → 评审门 → 冻结**。通过后写 `approve/APPROVED.md` 与 `TASK.md` 决策节，并将 `phase` 置为可 handoff/propose。不写实现代码，不创建 OpenSpec change。

## 门禁

缺任一项就停下，建议先 `explore` / `design`：

- `TASK.md` 目标能一句话说清；元信息含 `criterion`（或方案节完成判据）时可检验。
- 有可推荐方案（通常来自 `design/`；简单档可来自 `wizard/plan.md`；无稿则 human 须当面确认选项）。
- 「方案」里的质量画像与显式降级原文快照（上游复杂档传入时）属成功标准输入：冻结时连同原文一起写入，不得只留路径指针；缺失则先 `save` 补回；输入没有时不编造。
- 存在确认状态为 `pending` 的显式降级时**不得冻结**：停下，写成「降级未确认」并列出条目。只有用户点名接受该项、或明确说按降级表全部确认，才改为 `confirmed`；审阅收敛、单独的「继续」、执行者或评审者的判断都不算确认。
- 父任务只冻结范围、非目标与拆分原则；具体方案是各子任务的 `approve`。

## 1. 结构门

核对：判据可检查；非目标清晰；推荐方案的架构/接口/技术栈选择按 [phase-design.md](phase-design.md)「设计依据」写齐（不适用须声明）；上游有流程总览时，设计步骤与总览逐条对齐、偏离处带显式决策。写不出依据的选择列入未决，不算可批准。

## 2. 评审门

委托 `task-confirm`（闸口名 `approve`）。本闸口**只派一次**审阅循环，禁止嵌套再开 approve。

- **human**：可列选项；需要名册评审时按下方「名册评审」执行，或用户/同事已评审也算完成（结论写入 `approve/` 或 `design/review-*.md`）。
- **goal**：推荐默认 = design 里已写出的默认（含「冻结并允许 handoff」）；按 task-confirm 审阅；收敛即视为确认。无设计稿且无推荐方案时不编造，停下。

### 名册评审（可选增强；goal 默认走 task-confirm 派审，不强制名册）

用户点名要名册评审，或 human 选择名册时：

1. `{taskRoot}/design/`（或简单档 plan）已有可评方案；脏工作树先问用户。
2. 按 `$agent-roster`：先写 `decision.md` 再委派；`permission: read-only`；意见落 `{taskRoot}/approve/review-<yyyy-mm-dd>.md` 或 `design/review-<yyyy-mm-dd>.md`。
3. 评审要求须含**设计依据核对**：逐条按 phase-design「设计依据」核模式与变化点、可检后果、有无写不出依据却当成已设计的选择。
4. 接受的意见回 `design` 修正后再回本阶段结构门；不接受的当面说明。

## 3. 冻结写入

更新 `{taskRoot}/TASK.md` 的 **决策** 小节：

- 采纳：方案名 + 一句话主因
- 取舍：接受什么、放弃什么
- 可带进实现的未决：已逐条确认；未确认的不收录
- 回退：选错了怎么撤

写 `{taskRoot}/approve/APPROVED.md`（一句话结论、方案指针、评审意见路径、未决、下一步 handoff/propose）。`TASK.md` 元信息 `phase: approve` 完成后改为调用方约定的下一阶段（通常由 taskrail 写成 `propose`，或提示 `handoff`）。

同步 `INDEX.md` 对应行一句话（可改成「已批：…」）。有独立难逆权衡时另写 `{taskRoot}/design/adr-<slug>.md`。

## Goal 里

处在 goal 里时，不逐条问用户，也不列出「全部按默认冻结 / 先改某条 / 暂不冻结」。审阅收敛则写入决策与 APPROVED.md；调用方（taskrail）可在同轮 `handoff`。「降级未确认」不在此列。

不在 goal 里时：带默认值的未决须逐条请用户确认后才写入决策节。

## 重复 approve

新决策以新编号（D-n）追加；被取代的旧决策标注「被 D-n 取代」。`status: handed-off` 须先 `reopen` 才能重新 approve 后手 handoff；小改优先直接修订 driver `proposal.md`。

## 压缩路径

用户明确说「按 design 里的推荐冻结并交接」：视为已确认推荐默认（不含 pending 降级）；本轮完成本阶段后立刻 `handoff`。

## 驳回

评审不通过或结构门失败：`phase` 回 `design`（或 wizard），连败 +1；同闸口连败 2 次交 task-confirm / taskrail 升级 human 或 `blocked`。
