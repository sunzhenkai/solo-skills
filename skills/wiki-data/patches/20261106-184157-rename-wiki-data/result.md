# Result

- target: skills/llm-wiki → skills/wiki-data
- mode: update
- patch: 20261106-184157-rename-wiki-data
- risk: medium
- status: applied
- applied-at: 2026-11-06T18:47:28+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/wiki-data/tests skills/trouble-grill/tests skills/code-explore/tests -q` — 33 passed
- full tests: `python3 -m pytest skills -q` — 520 passed, 3 skipped
- repository checks: `make check-names` / `make check-style` — pass
- privacy check: pass
- mode check: pass

## Notes

目录、frontmatter、agent 配置、索引维护者与测试已统一为 `wiki-data`。既有工作区布局和 lint 接口未变；历史 patches 仅随目录迁移，内容未改。`README.md`、`.project-denylist` 与 `code-explore` 的有效引用已同步。
