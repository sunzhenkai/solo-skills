# Result：goal 模式下的执行器定位

已 `git apply`（与 task-goal / task-explore 的同 slug patch 同批）。

## 应用后的正文变化

| 位置 | 改动 |
|---|---|
| 开头定位 | 补「goal 模式下本 skill 是执行器：状态与完成门由 task-goal 持有」 |
| 主循环 2 | 「本循环其余阶段不变」→「本循环是执行器，不写 goal 状态」 |
| 新增节「goal 模式的归属」 | 五条：goal 持四状态/state-file/退出点与授权/完成门；本 skill 持 Stage 1–12；每轮收口回报；**本 skill 不写 `已完成`**；收口报告不是完成门；停机口径来自 task-goal |
| 主循环 12 | 「完成报告」→「收口报告」，注明是交给 task-goal 判完成门的输入 |
| 主循环 6 / 观感类 2 | 「主循环完成门」→「主循环的收口门」；「完成报告」→「收口报告」 |
| 观感类 3 | 中途真人门标注「也是复杂档 B 类降级的唯一集中追认点」 |

## 测试

全仓 `python3 -m pytest skills -q` → **424 passed, 1 skipped**。

交叉判读：`grep -n "已完成" skills/task-delivery/SKILL.md` 只剩两处，均为「不写 `已完成`」的否定句或状态枚举，符合预期。

## 遗留

- 无。

## 未验证 / 待观察

见 task-goal 侧 result.md（收口回报格式、来路分流的判据）。
