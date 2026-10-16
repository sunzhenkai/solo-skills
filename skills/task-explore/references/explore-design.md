# explore 与 design

未绑定任务先回 taskrail 绑定。

## explore：grill 自问自答

1. 读 `TASK.md`、`wizard/intent.md`、`wizard/plan.md`、已有 `design/`。意图里已确认的目标 / 做完的样子 / 不做不重问，只追细节、边界、约束、未知。
2. 委托 `grilling`，按它的轮次格式，但**自问自答**：每题先自己查一手资料，再写推荐结论和一句理由。纪要落 `explore/`，决定追加到 `TASK.md`「已做决定」；给用户只报结论（说决定见 [user-report.md](../../taskrail/references/user-report.md)）。`grilling` 不可用时同样自问自答。
3. 与确认版意图冲突：停下回 `task-intent` 纠偏，按契约「意图变更」处理。
4. 术语结晶写 `{taskRoot}/glossary.md`；独立难逆的决定写 `{taskRoot}/design/adr-<slug>.md`。有 `tasks/` 时 grill 只用 `grilling`——`grill-with-docs` / `domain-modeling` 会写仓库根文档，与任务目录落点冲突。
5. 结束时列出已定结论和仍开放的问题，写回 `TASK.md`。

## design：写方案

写入 `{taskRoot}/design/`（`README.md` 索引 + `<topic>.md` 主设计，按需 `adr-<slug>.md`）。

**动笔前要有**：目标一句话说得清；判据可检查；约束已知或已标明未知。缺了就说缺什么，回 explore，不写空心方案。

**写法**：

- 按 `wizard/plan.md` 的步骤展开；新增 / 删改 / 改序写进「已做决定」。
- 推荐方案 + 被放弃的方案各一两句与取舍；有可逆性差别就写回退。
- 影响架构、接口、技术栈的选择写一句依据和它换来的可检后果（少了哪处耦合 / 重复 / 回归面）。细则与对比表格式见 [design-detail.md](design-detail.md)（可选）。
- 推荐依赖未决项时把未决单列，不写成已定。
- Web UI 交付：读 [ui-delivery.md](../../taskrail/references/ui-delivery.md)，需要时落 `design/contract.md` 放指针与 digest。

成形后走 `approve`。一个目标里出现 ≥2 个独立方向时读 [large-scope.md](large-scope.md)。
