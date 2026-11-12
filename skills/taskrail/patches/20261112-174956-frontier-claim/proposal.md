# Frontier 与原子认领

- target: skills/taskrail
- mode: update
- patch: 20261112-174956-frontier-claim
- risk: medium
- status: proposed

## Intent

为多 worker 子任务增加可恢复的 frontier 与认领状态。decompose 仍按 ROADMAP 依赖激活 pending 子任务；主会话在调用 taskflow 派发前，通过 task_state.py 原子 claim 一个 active 且未认领的子任务。release 用于回收或确认 worker 停止后的 stale claim 清理。

不修改 taskflow，不解析 ROADMAP，不增加自动过期，不改变同任务同仓写串行、worktree 隔离或 worker 上下文边界。

## Conflict check

现有 pending → active 依赖推进保持不变。claimed_by / claimed_at 只新增到子任务 TASK，旧任务缺字段视为未认领。主会话统一写编排状态，worker 不直接认领或修改父 TASK。脚本继续使用 Python 3 标准库和现有 workspace state_lock。

## Rationale

现有规则要求每个 worker 只领一个单位，但缺少跨会话持久认领。锁内检查并写入可避免两个编排者同时派发同一子任务；显式 release 比按时间自动过期更保守，可用并发集成测试验证。

## Files

- skills/taskrail/SKILL.md：增加 frontier 与主会话认领不变量。
- skills/taskrail/references/contract.md：定义字段、frontier、认领与恢复语义。
- skills/taskrail/references/templates.md：补子任务认领字段说明。
- skills/taskrail/references/decompose.md：激活后、派发前 claim。
- skills/taskrail/references/ledger.md：resume 跳过已认领项及 stale claim 处理。
- skills/taskrail/scripts/task_state.py：新增 claim / release、字段渲染和 reconcile 输出。
- skills/taskrail/tests/test_task_state.py：覆盖状态校验、幂等、释放、旧任务和并发竞争。
- skills/taskrail/tests/test_decompose_contract.py：守卫派发前原子认领。
- skills/taskrail/evals/cases.yaml：增加两个编排者竞争同一子任务的案例。

## Validation

- 候选目录运行完整 python3 -m pytest skills/taskrail/tests -q。
- git apply --check --recount 与 git diff --check -- skills/taskrail。
- 应用后运行 python3 -m pytest skills/taskrail/tests -q 和 python3 -m pytest skills -q。
- 运行 make check-names 与 make check-style。
- 端到端核对两个进程同时 claim 只有一个成功，release 后另一个 owner 可认领，reconcile 不自动清理。
