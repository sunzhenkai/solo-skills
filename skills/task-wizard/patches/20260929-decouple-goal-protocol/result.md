# Result：task-wizard 收窄

已按 proposal 执行。SKILL.md 从 274 行减至 108 行；Goal 相关小节与术语全部移除；决策收敛节已加；references 迁移完成（external-precedent.md 保留并删 Goal 小节）。

测试：task-wizard 契约 16 条全过；全仓 `python3 -m pytest skills -q` → 282 passed, 1 skipped。

遗留：无。goal 侧语义见 task-goal 同 slug patch。
