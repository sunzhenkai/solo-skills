# Result：Web UI 检查按档调度（taskrail 侧）

改动已落工作树。

## 测试

- `python3 -m pytest skills tests -q` → 494 passed, 3 skipped（HEAD 为 493 passed, 3 skipped；+1 为新增 design 角色速度小节断言）。
- `make check-names` → OK。
