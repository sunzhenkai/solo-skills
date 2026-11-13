# Result

- target: skills/wiki-data
- mode: update
- patch: 20261113-190313-wiki-atlas-boundary
- risk: medium
- status: failed
- applied-at: 2026-11-13T19:05:35+0800

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- target tests: `python3 -m pytest skills/wiki-data/tests -q`：1 failed, 41 passed；新增 Atlas 链接测试未重建索引，触发既有 `index_stale`
- privacy check: pass
- mode check: pass

## Notes

补丁已应用，链接解析未报错；测试缺少 `--write-index` / `--check-index` 步骤。按协议保留失败记录，后续修正使用新 patch。
