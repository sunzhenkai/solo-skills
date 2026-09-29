# Eval: goal-stop-autocontinue-bridge

- candidate: evolutions/20260930-goal-stop-autocontinue-bridge/SKILL.md
- baseline: skills/task-goal/SKILL.md（源库 checkout，commit d0f7ece）
- date: 2026-09-30

## 回归

- 基线：`python3 -m pytest skills/task-goal skills/task-wizard -q` → **45 passed**
- 候选：同命令作用于隔离副本（/tmp 下的 skills 树，仅替换 SKILL.md 为候选稿）→ **45 passed**
- 结论：新段落未打断任何既有契约断言（frontmatter、解耦接口、P 级、评审者三选一、pending 确认门、退出点）。

## 模式

- 原失败路径：命中退出点 → goal 自动续跑 → 规则只允许重申 → 连续 4 轮空转。
- 按候选指令走同一路径：第 1–2 次续跑做只读环境查证与证据固化（有名分、有边界）；
  第 3 次续跑且仍无用户输入 → 标记 goal blocked + 交接摘要，循环终止。空转窗口从「无上限」变为「≤3 次」。
- 结论：该类失败可被新指令避免。

## 契约

- skill 自带 tests/（文本契约 pytest）。基线与候选同绿（见上），无分数编造。

## 副作用

- 触发范围：未改触发条件与门禁；未改「授权项是封闭集合」。
- 权限：只收紧不放宽——新段显式禁止停止期写交付代码、改判据/步骤/降级表、commit/push/部署；
  允许面仅限只读查证、外部原文取证、证据固化，并显式声明这些「不产生交付物、不属于『新增工作』」，
  消除与上一句「撞上退出点后不新增工作」的字面冲突（首轮候选未含此句，评估中发现后已补）。
- 残余风险（接受）：「证据固化」可被宽读为写文件；但证据文件非交付物，且 task-delivery 已有
  evidence_root 约定承接，不构成实现后门。
- 无密钥、内部 URL、项目代号进入正文。

## 结论

pass
