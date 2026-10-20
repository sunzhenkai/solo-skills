# task 系列深度复审落地（role-based-reviewer）

- 删 `intent` 角色（roles/intent.md 及 SKILL / protocol 引用）：goal 意图代审已由 taskrail confirm-protocol 派异源模型按 task-intent 清单做，全仓无调用方，且它用 Blocker/Major 而清单用 P0/P1。
- 门 2 写明核心角色可按强信号推断、可选角色只在点名或调用方传入时启用（原与 protocol 冲突）。
- 「不落盘」补一句：调用方需要评审文件时由调用方按骨架落盘（对齐 ui-delivery 的评审文件要求）。
- protocol.md 13145 → 6137 B：约束去掉与三道门重复的部分；RoleBrief 改一行说明；聚合骨架去字段级小标题；角色矩阵只留「我管」列，redirect 表去掉冗余列；删死指令「表内加粗角色是风险 owner」与已删除概念「未覆盖即降级 / A/B 定级」。
- 契约测试同步（test_no_intent_role）。
