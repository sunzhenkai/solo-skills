# Result

- target: skills/code-explore → skills/project-explore
- mode: update
- patch: 20261113-214757-project-explore-integration
- risk: high
- status: applied
- applied-at: 2026-11-13T21:47:57+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/project-explore/tests -q` — 12 passed
- privacy check: pass
- mode check: pass

## Notes

目录、frontmatter 与 agent 配置已统一为 project-explore。ask/explore 保持只读；archive/ingest/project 改为持久化路由，不再直接写文档或创建独立 profile。历史 patches 内容未改。
