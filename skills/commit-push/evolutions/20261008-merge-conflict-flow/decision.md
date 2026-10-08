# Decision

`promote`

## Reason

- 用户确认 Evolution Proposal 与候选 diff。
- 候选评估为 `pass`：生产基线 19 项契约测试通过，候选 27 项通过；合成 merge 冲突、脚本帮助、摘要模式、冲突裁剪与 `--full` 均已验证。
- 变更与 Proposal 一致，未改变既有安全协议与推送确认门。

## Action

- 已用候选 `SKILL.md`、`scripts/commit_push_context.sh`、`tests/test_commit_push_contract.py` 覆盖源码目录 `skills/commit-push/`。
- 未执行 git commit，也未同步安装镜像。
