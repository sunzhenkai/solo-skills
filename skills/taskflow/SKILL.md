---
id: taskflow
name: taskflow
description: "代码执行与隔离：在 workspace 为每个修改仓准备 git worktree，按 taskrail 路由选择 direct 或 OpenSpec；支持多仓、滚动切片、提交与验证。taskrail execute 委派、用户点名 taskflow / taskflow-new / 某个 driver，或需要隔离代码修改时使用。"
---

# taskflow

面向用户默认简体中文；端到端路由、resume、/goal 走 taskrail。用户表达按 [user-report.md](../taskrail/references/user-report.md)。

## 两个执行适配器，一套隔离协议

- `direct`：按 TASK / PLAN 的当前 checkbox 实施，不建 driver。
- `openspec`：建 `{task}-driver` 与子 changes，实施进度只看 change checkbox。
- 两者都在 `<workspace>/worktrees/<task-id>/<repo-id>/` 改代码、测试、提交；workspace 统一持 `tasks/` 和 `openspec/`。

执行前必读 [references/worktree.md](references/worktree.md)，并对每个必须修改的仓库运行：

```bash
python3 <taskflow>/scripts/prepare_worktree.py <workspace> <task-id> <repo-id> <source-repo> --json
```

exit 非 0 时不写代码；脏 worktree、身份或分支冲突保留现场并说明。基线可用 `--base` 显式指定，不自动 fetch、stash、reset、切源仓分支或清理用户改动。把返回的 repo / worktree / branch / base 写进 TASK 涉及仓库表。

## direct

1. 确认 criterion、PLAN 当前步骤和 worktree；`execution=direct`，不需要 handoff / approve / driver。
2. 读 [references/execution-discipline.md](references/execution-discipline.md)，在当前 worktree 实施一个连贯增量并跑 focused tests。
3. 只更新 PLAN 实施 checkbox 与证据，提交由编排者做；提交后重新路由，不直接标 done。

## OpenSpec

创建 driver 前按 taskrail handoff 写载荷，并在 workspace 跑 OpenSpec 入口门：

```bash
python3 <taskflow>/scripts/check_handoff.py <workspace> <task-path>
```

用户原话明确要求绕过 taskrail 时，才可在 TASK 写 `gate_bypass: "<日期> user-confirmed: <原话>"`；不手写省略验收的自由提示词，未核对项仍须记录。门通过后 `taskflow-new`：

1. 在 workspace 执行 `openspec new change {task}-driver --goal "<目标 + criterion + 方案 / 批准指针>"`。
2. `.openspec.yaml` 补 `skip_specs: true`，按 [references/driver-template.md](references/driver-template.md) 写 proposal 的 Driver 协议；tasks.md 留给 propose。
3. stock `openspec-*` 始终在 workspace 运行并显式给 change name；实现者 cwd 是对应 worktree。缺 skill / CLI 时说明安装，不发明等价命令。

## 经 taskrail 委托时

同名 change 选继续，不问；approve 放行即授权其范围内的 propose 与 apply，stock 的普通停顿由编排者按 [confirm-protocol.md](../taskrail/references/confirm-protocol.md) 停点表处理。单项做不了时该项保持未勾并继续其他就绪项；子 changes 全勾、验证和评审校核过后才 `openspec archive {task}-<slice> --yes`，不能用 `--yes` 掩盖未勾项。driver 归档后回 taskrail verify / close，不直接 done。

## 滚动与并行

OpenSpec 切片按依赖滚动展开，每片提交一次，片间检查点只说决定并继续，只增删改未勾项；新交付边界回 taskrail decompose。direct 也可按 PLAN 增量滚动，不因此自动创建 driver。

默认串行；同任务同仓写操作串行，不同子任务或不同仓库才可并行，细则 [references/multi-worker.md](references/multi-worker.md)。worker 只收本人范围、criterion、契约、worktree 绝对路径和证据要求，返回摘要与路径，不回灌完整日志。

完成验收与知识收口统一走 taskrail [done.md](../taskrail/references/done.md) / close，不在 taskflow 自行判 done。经验记录和进化只按 [self-evolution.md](references/self-evolution.md) 在运行闭环外执行。
