# 结果

- status: applied
- `python3 scripts/e2e_cross_repo.py --mode all`：direct 11 步 PASS（0.9s）、openspec 14 步 PASS（22.6s，openspec CLI 1.14.1），报告含逐步骤明细。
- 根 `python3 -m unittest discover -s tests -p 'test_*.py'`：Ran 13 tests，OK（含 direct / openspec 两个活体 E2E，缺依赖自动 skip）。
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`：Ran 131 tests，OK（skipped=2，playwright 可选）。
- `python3 -m unittest discover -s skills/taskflow/tests -p 'test_*.py'`：Ran 58 tests，OK。
- `make check-names`、`make check-style`、`git diff HEAD --check`：全部通过。
- 脚本开发中修复并回归的问题：run_json 缺 cwd、unittest 结果在 stderr 导致证据为空、sub_change 漏写夹具代码、macOS /var vs /private/var 路径比较、复跑测试的计时行弄脏 worktree（改为复跑不写证据）。
- 限制：openspec 模式依赖 CLI 行为（按 1.14.1 验证）；活体测试在无 git / 无 openspec 的环境自动跳过。
