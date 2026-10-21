# Result

- target: skills/taskrail
- mode: update
- patch: 20261021-204720-decompose-rolling
- risk: high
- status: applied
- applied-at: 2026-10-21T20:50:00+08:00

## Validation

- `git apply --check --recount`: pass。应用前逐文件核对了基线，与生成 patch 时一致；应用后的结果与候选稿逐文件一致。
- `git diff --check`: pass
- target tests: 全量 `python3 -m pytest skills tests -q` 结果为 470 passed, 3 skipped。本 patch 新增 9 条（`test_decompose_contract.py`），taskflow 同 id patch 新增 5 条。
- `make check-style`: OK，0 条告警，含 SKILL.md 体量、description 长度、引用链一层三项检查。
- `make check-names`: OK
- 其他：全部 `evals/cases.yaml` 都能被 YAML 解析，id 不重复；CI 的 frontmatter 检查 18 个 skill 通过。
- privacy check: pass（示例只用「导出接口」「统一登录」这类通用说法）
- mode check: pass

## Notes

- 体量：SKILL.md 从 5858 B 增到 6115 B；description 227 字符。
- `references/explore-design.md` 改名为 `design.md`；`large-scope.md` 从 1095 B 增到 4472 B；contract.md 从 8119 B 增到 8908 B。
- evals 从 54 条增到 61 条。
- 只应用到工作树，没有暂存，也没有提交。
