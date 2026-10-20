# task 系列深度复审落地（task-explore）

- handoff 步骤顺序修正：原第 3 步先建 driver，而 taskflow 入口门要求 status=handed-off（第 4 步才写）→ 照字面会被打回 handoff 死循环。改为写交接节 → 改状态 → 跑 check_handoff → 建 driver → INDEX → propose；建不成时回滚状态。
- templates.md 的 TASK.md 元信息改成 `---` frontmatter（原 `- key:` 列表行 check_handoff 解析不到），补 evidence_root，confirm_mode 不再写死 human。
- approve：按「停点」表只走一次，放行后两种模式都同轮 handoff；连败两次按 user-report「卡住」停；已 handed-off 的改方案按契约「意图变更」第 4 条开修订子 change（原与契约两套做法）。
- description 去掉反向句，边界挪进正文。
- 新增行为测试 test_handoff_gate_before_driver。
