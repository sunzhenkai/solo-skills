# 结果

- status: applied
- `change.patch` 已包含生产文件、临时 git 仓集成测试与 evals；通过基线 `git apply --check` 和交付树反向应用检查。
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`：Ran 58 tests，OK。
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`：Ran 131 tests，OK（skipped=2）；跳过项为 taskrail 的可选真实浏览器测试。
- `git diff HEAD --check`：OK。
- `make check-style`：OK（0 条告警）；`make check-names`：OK。
- 两份 `evals/cases.yaml` 均解析通过；`prepare_worktree.py`、`check_handoff.py` 与 `task_state.py` 均通过 `py_compile`。
- 多仓 worktree 创建 / 恢复、身份冲突、脏树保留、无 remote 基线和 direct / OpenSpec handoff 边界均由临时仓库或契约测试覆盖；跨 Skill 本地引用检查通过。
- 根 `README.md`、`AGENTS.md` 与 `docs/task-flow/README.md` 作为仓级文档单独同步，不包含在本 Skill patch 中。
- 限制：未运行真实 OpenSpec CLI 端到端工作流；本次验证了 workspace / driver / handoff 适配契约，未宣称真实 CLI 已验收。
