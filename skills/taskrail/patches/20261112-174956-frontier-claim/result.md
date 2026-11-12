# Result

- target: skills/taskrail
- mode: update
- patch: 20261112-174956-frontier-claim
- risk: medium
- status: applied
- applied-at: 2026-11-12T17:49:56+08:00

## Validation

- `git apply --check --recount`: pass
- `git diff --check`: pass
- candidate tests: `python3 -m pytest skills/taskrail/tests -q` 152 passed, 2 skipped, 2 subtests passed
- target tests: `python3 -m pytest skills/taskrail/tests -q` 152 passed, 2 skipped, 2 subtests passed
- full tests: `python3 -m pytest skills -q` 573 passed, 3 skipped, 2 subtests passed
- style checks: `make check-names` 与 `make check-style` pass
- privacy check: pass
- mode check: pass

## Notes

claim / release 仅支持子任务；claim 要求 active，同一 owner 幂等，并发集成测试验证六个进程只有一个认领成功。release 校验 owner，force 用于人工确认后的 stale claim；reconcile 保留并报告认领。旧子任务缺少字段时可直接认领，根任务不写可选认领字段。

仅修改 taskrail；主会话在调用 taskflow 前认领，未修改 taskflow 或安装镜像。
