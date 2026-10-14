# Proposal：输出风格门禁 + task-explore / role-based-reviewer 瘦身到 ≤8K

- target: scripts/check_output_style.py、tests/test_output_style.py、Makefile、AGENTS.md、skills/task-explore、skills/role-based-reviewer
- mode: update
- patch: 20261015-output-style-slim
- risk: low
- status: applied

## Intent

简洁要求只散在文案里（「半屏内」「≤2 行」），没有任何执行手段；task-explore 9.5K、role-based-reviewer 10.4K 超出 8K 指导线。

- 新增 `scripts/check_output_style.py`（仅标准库）：task 族 + role-based-reviewer 的 SKILL.md ≤8192 B（其余 skill 仅告警）；意图复述模板 ≤8 行且无内部术语；「Digest（≤10 行）」模板 ≤10 行。`make check-style`；repo 级测试调用它，pytest 即覆盖。
- task-explore：只压缩表格对齐空格，内容不变（9499 → 7559 B；gate_lines 锁全过）。
- role-based-reviewer：「视角推断」全文、「耗时优化」全文、调用示例原句下沉到 `references/inference-and-speed.md`，正文留 3 行要点 + 指针；删一句与 description 重复的定位句；description 角色表补 `intent`（10425 → 8178 B）。
- AGENTS.md：体量从「不设测试」改为 task 族强制；命令表与提交前检查加 `make check-style`。

非目标：pretty-view-html / project-init / skills-store 仍超 8K，只告警不改。
