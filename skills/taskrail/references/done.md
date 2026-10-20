# 完成清单（唯一真源）

把 `status` / `phase` 标 `done` 前逐条核对；任一条缺证据就不标。不靠记忆，不用「整体看没问题」代替。

1. **判据成立**：`criterion` 原文成立，有验证命令与结果。skip 档写在 `TASK.md`「验证」节；full 档写在 driver `proposal.md` 验证记录，且相关 checkbox 全勾。
2. **做完的样子**：对照 `wizard/intent.md`（若有），「做完的样子」逐条成立，「不做」没被越界。
3. **交付标准**：`wizard/plan.md` 列出的交付标准全过（写「无」则只看判据）。
4. **观感**：用户原话有观感目标时，下方「观感验收」已过。
5. **评审意见**：做过评审的，每条 Blocker / Major 都有处置——`fixed` 或 `accepted-recorded`（带理由）。
6. **没验证的不算过**：判据或交付标准里没验证到的项，写进「已做决定」说明少交付了什么、为什么；会缩小判据或交付面的，按真阻塞停下等用户（[user-report.md](user-report.md) 第 5 节）。

`handed-off`、propose 完、checkbox 全勾但判据不成立 → 不标 `done`。

## 观感验收

用户原话里有观感类目标（好看、设计感、体验）时加这一条验收，不看档位：

- **视觉方向**：动手前读 [../../pretty-view-html/references/frontend-design/REFERENCE.md](../../pretty-view-html/references/frontend-design/REFERENCE.md)，在 `wizard/plan.md`「质量属性」写下配色、字体、版式、一个特征元素，再列几件参照（作品或既有页面，写清取它哪一点）。
- **截图**：先备接近真实的演示数据（够多条、长短文本、多种状态），同一路由、同一视口截改前 / 改后两组，放进证据目录。
- **另一个模型审**：按 [confirm-protocol.md](confirm-protocol.md)「另一个模型审」派审，对照参照审截图（可用 `role-based-reviewer roles=design`）。
  - goal：不停下问人。还有观感 Blocker / Major 就按意见改、重截、再审，自己迭代到没有为止；每轮结论与截图路径记进验证记录。同一问题两轮没改好，按 [user-report.md](user-report.md) 第 5 节「卡住」停。
  - human：评审过了再把改前 / 改后截图给用户看，用户说可以才算完成；没回话不算。

## 可选附录（命中才读）

- Web UI 交付：[ui-delivery.md](ui-delivery.md)
- 用户点名质量画像 / 降级分级 / 验收打分，或 full 档交付面广：[quality-appendix.md](quality-appendix.md)
