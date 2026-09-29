# Decision — 20260929-review-integrity

decision: promote

原因：
- 使用者显式点名 skill-evolver 并要求晋升（2026-09-29），proposal 已逐条展示并获确认；
- evaluate 结论 pass（回归 5/5、模式四类失败均可被新指令避免、契约无冲突、副作用 fail-safe）；
- 候选与 proposal 一致，无夹带编辑：SKILL.md 三处（step 6 回归门、step 9 异源门、新增「观感类质量目标」节），loop-protocol.md Stage 7 一处（异源门 + 回归门 + 观感类目标）。
- 真实经验来源：2026-09 一次完整 UI 交付闭环的败局复盘（同源评审回声、主循环 Stage 7 零执行、真人在收口才首次看图），抽象后落盘，无项目名 / 机器路径 / 内部代号。

promote 范围：task-flow-skills/skills/delivery-loop/SKILL.md + references/loop-protocol.md。
注意：~/.agents/skills/ 运行镜像仍指向 dotfiles 旧副本（dotfiles 中本 skill 已迁出），
需从本仓库重新 sync；sync 与 commit 均未由本 skill 执行。
