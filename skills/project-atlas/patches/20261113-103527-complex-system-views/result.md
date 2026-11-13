# Result

- target: skills/project-atlas
- mode: update
- patch: 20261113-103527-complex-system-views
- risk: medium
- status: applied
- applied-at: 2026-11-13T11:20:31+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/project-atlas/tests -q`，17 passed
- repository checks: `make check-names`、`make check-style` 通过；`python3 -m pytest skills -q`，529 passed, 3 skipped, 2 subtests passed
- privacy check: pass，示例为虚构通用系统，无真实公司、项目、主机或凭据
- mode check: pass，仅更新现有多视角组织、CLI、测试、evals 与示例

## Notes

新增 `flows/`、`architecture/`、`data/`、`cross-cutting/` 页面支持；保留既有领域三层、Archify 与自愈契约。示例包含建议目录、L0 总览和广告请求主链路内容。
