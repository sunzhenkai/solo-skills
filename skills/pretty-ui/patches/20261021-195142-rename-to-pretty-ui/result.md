# Result

- target: skills/pretty-ui（原 skills/pretty-view-html）
- mode: update
- patch: 20261021-195142-rename-to-pretty-ui
- risk: medium
- status: applied
- applied-at: 2026-10-21T19:52:21+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills tests -q` → 389 passed, 3 skipped；`make check-style` → OK（0 条告警）；`make check-names` → OK
- privacy check: pass
- mode check: pass（只改名，行为不变）

## Notes

- `patches/` 历史随目录用 `mv` 迁到 `skills/pretty-ui/patches/`，未进 change.patch；历史记录里的旧名保持原样。
- 仓内生效文件里 `pretty-view-html` 只剩默认输出目录 `docs/pretty-view-html/`（按 proposal 留到正文重写那一轮处理）。
- 同轮配套：taskrail、taskflow 各一份改路径 patch（同一时间戳）；README skill 表改名（仓库级，不属于任何 skill）。
- 仓外待办：dotfiles 编目与锁文件仍写 `pretty-view-html`，按用户决定以后处理。
