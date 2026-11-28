# Result

- target: skills/project-design-patterns（原 skills/agent-api-ops 并入）
- mode: update
- patch: 20261123-142058-merge-agent-api-ops
- risk: medium
- status: applied
- applied-at: 2026-11-23T14:28:19+08:00

## Validation

- solo-skills 全量：`python3 -m pytest skills tests -q` → 658 passed, 3 skipped, 2 subtests passed（基线 659；减少的 1 项为旧技能独立 frontmatter/尺寸断言，已并入引用件契约）
- `make check-style` → OK（0 告警）
- `make check-names` → OK（10 个 denylist 词）
- 布局：把 `skills/project-design-patterns/` 复制到临时目录，`SKILL.md` 直链 `references/agent-api-ops.md`、`references/agent-api-access.md` 均可解析，无跨 skill 断链
- 旧独立安装命令 `-s agent-api-ops`：仅剩测试里的否定断言与 `change.patch` 历史内容；运行时文本已清零

## Consumer sync

- hela：`go test ./internal/handler/` → ok；`pnpm exec vitest run src/shared/apikeys.test.ts` → 4 passed。话术安装命令、`/skill.md` 版本声明（`skill: project-design-patterns@1.1.0`）、契约测试与 README 已同步。
- dotfiles：`agents/skills.yaml` 移除 `agent-api-ops`；`agents/skills.lock.yaml` 同步删除该条目（解析 70 条，`project-design-patterns` 在列）。`pytest tests/test_lock_update.py tests/test_agents_sync_references.py` → 26 passed；`make registry` → 校验通过。
- **待办**：solo-skills 提交推送后，dotfiles 需 `make skills-lock-update` 重锁——`project-design-patterns` 的 lock 仍指向既有 revision `69674d4`（合并前内容），重锁后更新 revision/content_hash 与审计 evidence。

## Notes

- `README.md`、`archive/README.md` 属仓库级清单，按 patch 协议未进入 `change.patch`，已在本轮直接更新：README 合并为一行；archive 旧名链 `app-api-ops → agent-api-ops` 改指 `→ project-design-patterns`，并新增 `agent-api-ops → project-design-patterns` 并入登记（`tests/test_cross_skill_refs.py` RegistryTest 依赖）。
- 不建 `archive/skills/agent-api-ops/` 副本：生产内容已并入引用件，沿用 `skill-evolver` 等「并入」先例，由 `archive/README.md` 概念表登记。
- 版本口径：操作规范版本随 `project-design-patterns` 的 `SKILL.md` frontmatter（本版 1.1.0）；应用声明最低期望版本，模式库后续扩展不会强制应用升级。
