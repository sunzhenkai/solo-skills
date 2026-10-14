# Proposal：simple 档直接实现 + 验证；删 task-explore 逐字锁

- target: taskrail 等（见 change.patch）
- mode: update
- patch: 20261015-slim-1-simple-direct
- risk: medium
- status: applied

## Intent

强模型下 simple 局部小改不需要 driver / OpenSpec。simple：wizard 定稿后直接实现，验证写 TASK.md「验证」节，过完成门即 done；超出局部即升档 medium。完成门第 3 条按档；taskflow 删「simple 单切片」节；示例改 medium。删除 task-explore tests/gate_lines.txt（117 句）与 test_task_explore_gate_lock.py，改为 6 条关键行为检查（不覆盖、建 tasks/ 先确认、archive/reopen 明确确认、phase 枚举封闭、任务目录不调 grill-with-docs、approve 唯一出口 handoff）。根目录 AGENTS.md / README.md 同步一句（未计入本 change.patch）。
