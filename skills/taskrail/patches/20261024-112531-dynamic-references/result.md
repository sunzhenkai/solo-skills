# 结果

- status: applied
- `change.patch` 已包含生产文件、测试、evals 与旧 `phase-wizard.md` / `large-scope.md` 删除项；通过基线 `git apply --check` 和交付树反向应用检查。
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`：Ran 131 tests，OK（skipped=2）。跳过项均为需要 playwright / axe 环境的可选真实浏览器测试。
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`：Ran 58 tests，OK；包含共享 handoff 与跨 Skill 契约回归。
- `git diff HEAD --check`：OK。
- `make check-style`：OK（0 条告警）；`make check-names`：OK。
- 两份 `evals/cases.yaml` 均解析通过；三个执行 / 状态脚本均通过 `py_compile`。
- taskrail 与 taskflow 的 SKILL / references 本地 Markdown 引用存在性已固化为契约测试；生产文档与根使用文档共 42 个文件的人工解析复核通过。
- 根 `README.md`、`AGENTS.md` 与 `docs/task-flow/README.md` 作为仓级文档单独同步，不包含在本 Skill patch 中。
- 限制：未运行真实 OpenSpec CLI 端到端工作流；本次验证了 OpenSpec 适配契约、handoff 新旧兼容和完成门，未宣称真实 CLI 已验收。
