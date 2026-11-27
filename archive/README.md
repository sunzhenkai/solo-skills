# archive

已从 `skills/` 下线、不再安装的 skill。生产内容与历史 `patches/` / `evolutions/` 原样保留在 `archive/skills/<id>/`，便于查阅与恢复。改名、合并与删除的概念也在本文件登记（见文末）。

这里不进 `npx skills` / `npx skills add` 的发现路径，也不跑测试与风格检查。

## 恢复

1. `git mv archive/skills/<id> skills/<id>`
2. 在根 `README.md` 的 skill 表补回该行
3. 从本文件条目表删掉该行
4. 跑 `python3 -m pytest skills/<id>/tests -q`、`make check-style`、`make check-names`

## 条目

| 名称 | 下线原因 |
|------|----------|
| `project-spec-mirror` | 按用户要求下线归档（2026-11-12）；spec 镜像场景暂由 `wiki-data` 与 OpenSpec 流程承接 |

## 改名、合并与删除的概念

skill 改名、并入其他 skill，或删除了会被其他 skill 引用的概念时，在下表登记一行。`tests/test_cross_skill_refs.py` 据此检查各 skill 的 `SKILL.md`、`references/`、`examples/`：旧名只能出现在「现在」列的 skill 里（作为旧触发词）；其他位置写成「原 `旧名`」。上表已下线的 skill 同样只能以「原 `名称`」出现。

| 旧名 | 现在 | 说明 |
|------|------|------|
| `agent-wizard` | `agent-docs-writer` | 改名 |
| `code-explore` | `project-explore` | 改名 |
| `llm-wiki` | `wiki-data` | 改名 |
| `skill-evolver` | `skill-upgrader` | 并入为 `evolve` 模式 |
| `agent-roster-flow` | `agent-roster` | 并入为 flow 模式 |
| `app-api-ops` | `project-design-patterns` | 改名 `agent-api-ops` 后并入其 `references/agent-api-ops.md` |
| `agent-api-ops` | `project-design-patterns` | 并入为 `references/agent-api-ops.md`，不再独立安装 |
| `wizard` | — | taskrail 改为动态路由，不再有 wizard 环节 |
| `solo-code-review` | `way-to-cr` | 改名并扩展为多引擎代码审查 |
