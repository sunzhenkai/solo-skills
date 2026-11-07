# Result

- target: skills/wiki-data
- mode: update
- patch: 20261107-001422-confidence-freshness-reuse
- risk: medium
- status: applied
- applied-at: 2026-11-07T08:10:43+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/wiki-data/tests -q` — 31 passed
- full tests: `python3 -m pytest skills -q` — 530 passed, 3 skipped
- repository checks: `make check-names` / `make check-style` — pass，0 条风格告警
- end-to-end: 临时 wiki 写入 source、validated / draft / deprecated experience、已更正 concept，运行 `lint_wiki.py --write-index` 与 JSON 检查 — 0 error，2 个 `review_overdue` 均准确报告；置信度、状态、核实与复审日期进入索引，历史页面保留
- applied diff: `git apply --check --recount --reverse` — pass
- privacy check: pass
- mode check: pass

## Notes

采用页面默认 `confidence` 与主张级例外，分离证据强度、经验状态与复审时效；高置信度及 validated 经验有确定性元数据门禁。查询增加相似任务执行前预检，输出保留出处、置信度、核实日期、适用边界和时效缺口。旧业务页缺 `confidence` 时会报 `missing_frontmatter`，需按真实证据补标，不会自动编造等级。
