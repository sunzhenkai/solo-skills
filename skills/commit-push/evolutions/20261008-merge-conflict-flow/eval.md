# Evaluation

## 回归

- 生产契约测试（候选前）：`19 passed`。
- 候选契约测试（含新增冲突流程与脚本测试）：`27 passed`。
- 原有安全协议、规模分流、路径级暂存、非共享远程链式命令、共享远程推送确认门均保持通过。

## 模式

- 合成 merge 冲突场景：`commit_push_context.sh --conflicts` 能识别 `operation: merge`、输出 `file: <path>` 与 `conflicts: 1`，并按默认上限输出两侧摘要。
- `--help`、`--summary`、`--stat`、`--push` 均能在干净仓库中运行；`--summary` 输出固定为少量结构化行。
- `SKILL.md` 已包含“处理冲突”入口与追加型 / 语义型 / 危险型分流规则。
- 手动验证 `--max-lines 1` 只输出每侧 1 行并提示截断，`--full` 展开全部冲突行。

## 契约

- `scripts/commit_push_context.sh` 存在且可执行，`bash -n` 语法检查通过。
- 新增契约覆盖：冲突章节存在、三类冲突分流存在、冲突盘点脚本被引用、验证步骤存在、冲突处理不绕过推送确认门、脚本帮助与合成冲突输出。
- 候选目录结构：`proposal.yaml` / `SKILL.md` / `scripts/commit_push_context.sh` / `tests/test_commit_push_contract.py`。

## 副作用

- 脚本只读：仅使用 `git status`、`git diff`、`git log`、`git rev-parse`、`git ls-files` 等读取命令，不含 add/commit/push/reset/checkout。
- 推送门禁未放宽：共享远程与默认分支仍需单独确认。
- 未改变密钥、内部 URL、破坏性操作等安全约束。
- 默认冲突输出按每侧 40 行裁剪，仅在 `--full` 时展开，符合降低 token 消耗的目标。

## 结论

`pass`
