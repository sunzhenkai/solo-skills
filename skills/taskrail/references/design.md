# design：先 grill，再写方案

未绑定任务先按 [ledger.md](ledger.md)「绑定」绑定。design 不停人，两步做完就进 approve；旧任务的 `phase: explore` 从第一步接着做。

## 第一步：grill 自问自答

1. 读 `TASK.md`、`wizard/intent.md`（子任务读父任务的，加路线图里自己那一行）、`wizard/plan.md`、已有 `design/`。意图里已确认的目标 / 做完的样子 / 不做不重问，只追细节、边界、约束、未知。
2. **自问自答，按设计树分轮**：把待定的点排成树（一个决定下面挂着依赖它的决定），每轮只处理前置都已定的那一层。每题由自己回答：先查一手资料，查得到的写成事实；查不到的取舍按推荐定下，带一句理由；再进下一层。纪要落 `design/grill.md`（旧任务的 `explore/` 照读），决定追加到 `TASK.md`「已做决定」；给用户只报结论（说决定见 [user-report.md](user-report.md)）。
3. 与确认版意图冲突：停下按 [intent.md](intent.md) 重新纠偏，按契约「意图变更」处理。
4. 术语结晶写 `{taskRoot}/glossary.md`；独立难逆的决定写 `{taskRoot}/design/adr-<slug>.md`。产物只写任务目录。
5. 树上没有未定的点就结束：列出已定结论和仍开放的问题，写回 `TASK.md`。

## 第二步：写方案

写入 `{taskRoot}/design/`（`README.md` 索引 + `<topic>.md` 主设计，按需 `adr-<slug>.md`）。

**动笔前要有**：目标一句话说得清；判据可检查；约束已知或已标明未知。缺了就说缺什么，回第一步补，不写空心方案。

**写法**：

- 按 `wizard/plan.md` 的步骤展开（有路线图就逐项展开）；新增 / 删改 / 改序写进「已做决定」。
- 路线图长时写到能批的程度：整体方案、各项边界与接口写全；依赖还没满足的项写一段话即可，细节等轮到它时按当时的代码补。
- 推荐方案 + 被放弃的方案各一两句与取舍；有可逆性差别就写回退。
- 影响架构、接口、技术栈的选择写一句依据和它换来的可检后果（少了哪处耦合 / 重复 / 回归面）。细则与对比表格式见 [design-detail.md](design-detail.md)（可选）。
- 推荐依赖未决项时把未决单列，不写成已定。
- Web UI 交付：读 [ui-delivery.md](ui-delivery.md)，需要时落 `design/contract.md` 放指针与 digest。

成形后走 `approve`。写方案时发现要拆、或要改拆法：按 [large-scope.md](large-scope.md) 改 plan 的路线图并记进「已做决定」；动到判据或范围的走契约「意图变更」。
