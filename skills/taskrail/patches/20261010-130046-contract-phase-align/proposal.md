# Proposal：对齐 phase 枚举与档位路径（Wave 0）

## Intent

按评审修复方案 D1–D3：消除 simple 交付分叉；`grill`/`handoff` 归为非 phase 动作；档位表与封闭 `phase` 枚举对齐。

## Mode

`update`（skill-upgrader）

## Risk

`medium`（改编排语义；用户已确认「按推荐做完」）

## 变更摘要

- `references/contract.md`：档位表改为 explore(仅 grill)/handoff→propose；simple 专条强制 taskflow；新增非 phase 动作表与 status×phase 合法组合
- `references/phase-wizard.md`：wizard 之后路径与契约对齐
- `SKILL.md`：主循环 explore/propose/完成门与依赖说明同步
- 契约测试与 eval case `simple-via-openspec`

## Validation

`python3 -m pytest skills/taskrail/tests -q`
