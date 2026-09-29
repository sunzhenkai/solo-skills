# Decision — 20260930-heterogeneous-review

decision: promote

原因：
- 使用者确认 Proposal（2026-09-29「确认」），随后 skill 源迁移至 solo-skills，
  本轮以 solo-skills 为生产源重新校准后执行；
- evaluate 结论 pass（回归路径等价、三类失败模式均可避免、无权限放宽）；
- 候选与 proposal 一致，无夹带编辑：输入节 +2 参数、示例 +1 行、流程第 1/4 步、耗时优化节，
  共四处最小 patch；
- 证据抽象落盘（无项目名 / 机器路径 / 内部代号）。

promote 范围：solo-skills/skills/role-based-reviewer/SKILL.md。
注意：~/.agents/skills/ 运行镜像为旧目录副本（非软链），sync 与 commit 未由本 skill 执行。
