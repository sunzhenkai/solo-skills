# description 去掉实现细节

- target: skills/service-manager
- mode: update
- patch: 20261118-014614-description-trim
- risk: high
- status: proposed

## Intent

description 保留探索来源、六个 phase 与访问方式，去掉「按项目隔离缓存与日志；安全停止（进程组优先）；缺 name 默认询问；完成后给出改动范围、影响面」等正文细节；触发句补全「重启」「状态与日志」。非目标：正文与 references 不变（上述细节已在 SKILL.md「项目根」「完成后总结」与 `references/commands.md` 中）。

## Conflict check

none。

## Rationale

description 常驻上下文，按 AGENTS.md 只写 WHAT + WHEN；触发句与 phase 一一对应。

## Files

- skills/service-manager/SKILL.md：description。

## Validation

- `python3 -m pytest skills/service-manager/tests -q`（gate lock）
