# approve：自查 → 闸口 → 冻结

未绑定先按 [ledger.md](ledger.md)「绑定」绑定。不写实现代码，不建 OpenSpec change。

## 1. 自查

缺任一项就停，回 `design`：

- 目标一句话说得清，`criterion` 可检查；「不做」清楚。
- 有推荐方案（通常来自 `design/`；skip 档不走本阶段）。
- 设计步骤与 `wizard/plan.md` 步骤对得上，偏离处在「已做决定」里有记录。
- 拆了的：路线图满足 [large-scope.md](large-scope.md)「路线图」三条要求，有代码依赖的两项都是切片。
- 没有会缩小判据或交付面、却还没经用户同意的降级（那是改判据，属真阻塞）。

## 2. 闸口

按 [confirm-protocol.md](confirm-protocol.md)「停点」表的 approve 行只走一次：human 把推荐写成决定呈现，用户说「继续」即放行；goal 派另一个模型审，收敛即放行。用户点名名册评审时按 `$agent-roster` 只读委派，意见落 `approve/review-<yyyy-mm-dd>.md`。

子任务的方案在父任务路线图那一行的范围和子判据之内时，闸口不停：按推荐写成决定，`APPROVED.md` 注明「在父任务路线图范围内」，同轮冻结并 handoff。超出范围或要改子判据，才按 approve 行停。

## 3. 冻结

- `TASK.md`「已做决定」追加：采纳方案 + 主因、取舍、回退；带进实现的未决单列。
- 写 `approve/APPROVED.md`：一句话结论、方案路径（可附 git 短 hash）、评审意见路径、未决、下一步只写 handoff。
- 同步 INDEX 行（如「已批：…」）。
- 出口按 [契约「approve 出口与交接」](contract.md)：下一步只有 handoff。闸口放行后本轮冻结完立刻 handoff，两种模式相同。

## 重复 approve 与驳回

- 新决定以新编号追加，被取代的标「被 D-n 取代」。已 `handed-off` 的按 [契约「意图变更」](contract.md)第 4 条开修订子 change。
- 自查或闸口不过：`phase` 回 `design`（或 `wizard`）；同一闸口连败两次，按 [user-report.md](user-report.md) 第 5 节「卡住」停。
