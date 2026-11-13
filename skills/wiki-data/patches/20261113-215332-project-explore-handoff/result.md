# Result

- target: skills/wiki-data
- mode: update
- patch: 20261113-215332-project-explore-handoff
- risk: medium
- status: applied
- applied-at: 2026-11-13T21:53:32+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/wiki-data/tests -q` — 42 passed
- privacy check: pass
- mode check: pass

## Notes

源码探索入口已改为 project-explore。wiki-data 可接收 Brief 和 Atlas 回执为候选材料；Atlas 缺口或冲突需要代码取证时交给 project-explore，query 保持只读。wiki 布局与 lint 脚本未改。
