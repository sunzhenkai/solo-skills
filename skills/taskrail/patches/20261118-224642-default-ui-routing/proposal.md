# Proposal：Web UI 实现前经 ui-kit 分派

## Intent
taskrail 在 Web UI 实现前选择通用或模板主路线。通用路线继续使用 pretty-ui Active Instance 与 two-pass；模板路线使用 ui-template lock 和像素保真。两条路线都保留运行态证据和独立 design 评审门。

## Files
- `skills/taskrail/references/ui-delivery.md`
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`
- `README.md` 依赖组由 ui-kit patch 一并收录

## Tests
验证 ui-kit 链接可解析、非 React 与模板分派存在、模板交接值明确；既有 pretty-ui 方向、截图与批评契约不变。
