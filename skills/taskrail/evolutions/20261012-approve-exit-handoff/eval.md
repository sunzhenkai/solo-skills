# Eval：approve-exit-handoff（20261012，taskrail）

## 回归

- 生产稿未改。`python3 -m pytest skills -q` → **495 passed, 2 skipped**。
- 新断言四句在生产稿中均为缺句（红）。
- 候选暂存到独立目录（不覆盖生产稿）后全仓 → **497 passed, 2 skipped**
  （495 + taskrail / task-explore 各 1 条新断言）。
- 档位表、phase 枚举、simple 必 handoff、带着未决关闭（「不要求清零」）仍在，既有断言不破。

## 模式

- approve 完成后唯一推荐是 handoff；此出口不列 archive、另起任务、继续探索。
- 查证与外部依赖进「可带进实现的未决」，未决不阻断交接、不另开任务。
- 同一已冻结方案的多条实施线建成该 driver 的 taskflow 子 change。
- 禁止用当轮叙事改写 criterion；方案落盘不是完成门。
- 方案含实施且尚未 handed-off 时拒绝进入 archive。用户明确放弃或不实施才可归档。
- 与 task-explore「不交接而结束」冲突时以 taskrail 本节为准。阶段细则同步见 task-explore 同 slug。

## 契约

- 第一级：候选暂存后 taskrail 新断言与既有契约测试通过。
- 第二级：宿主 `python3 -m pytest skills -q`。生产基线 495 passed；候选暂存 497 passed。

## 副作用

- 未改档位、phase 枚举、父任务纯伞、子任务只一层。
- 未删「带着未决关闭」；只在进入 archive 之前增加拒绝条件。
- 触发范围：approve 之后的推荐下一步变窄。放弃 / 不实施 / 确认关闭且不做实施仍可 archive。
- 过拟合：提案与正文无项目名、路径、密钥。

## 结论

pass
