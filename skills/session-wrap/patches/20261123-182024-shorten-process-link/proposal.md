# 缩短过程复盘链接文字

- target: skills/session-wrap
- mode: update
- patch: 20261123-182024-shorten-process-link
- risk: low
- status: proposed

## Intent

缩短过程复盘链接的显示文字，保持目标路径与行为不变，使 SKILL.md 低于 8192 B 风格阈值。

## Conflict check

none

## Rationale

上一 patch 后文件为 8193 B，仅超阈值 1 B；链接显示文字无需重复目录名。

## Files

- skills/session-wrap/SKILL.md：缩短 process-review.md 链接文字。

## Validation

- 应用前运行 `git apply --check --recount`。
- 应用后运行 `git diff --check`、相关测试及 `make check-style`，确认体量低于 8192 B。
