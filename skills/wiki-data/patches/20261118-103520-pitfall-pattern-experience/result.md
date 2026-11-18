# Result

- target: skills/wiki-data
- mode: update
- patch: 20261118-103520-pitfall-pattern-experience
- risk: medium
- status: applied
- applied-at: 2026-11-18T10:37:00+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/wiki-data/tests -q`，45 passed
- full tests: `python3 -m pytest skills tests -q`，589 passed、3 skipped、2 subtests passed
- repository checks: `make check-style` 0 条告警；`make check-names` 无命中
- CLI 样例：虚构 wiki（2 个 pitfall + 1 个 pattern）`--check-index` 0 error / 0 warning，索引摘要带 `[pitfall]` / `[pattern]` 与现象词；去掉一页 `symptoms` 后报 `symptoms_missing`
- size: `SKILL.md` 8091 字节，低于 8KB 告警线
- privacy check: pass（示例均为虚构通用场景）
- mode check: pass

## Notes

- 既有「用户明确要求归档 `trouble-grill` 记录时」原句保留，弯路复盘的坑候选另起一句接入同一节。
- 未设 `kind` 的页面与索引输出不变，既有工作区升级后无需重建索引。
