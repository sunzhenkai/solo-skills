# taskrail 契约（workspace / 状态 / references / 父子任务）

task 系列唯一真源。其他细则与本文冲突时以本文为准；用户表达见 [user-report.md](user-report.md)，停点见 [confirm-protocol.md](confirm-protocol.md)。

## 1. 三个根与三个正交维度

```text
<workspace>/
├── tasks/                  # 规划根：任务、父子任务、证据指针
├── openspec/               # 按需：所有 driver / changes
└── worktrees/<task-id>/<repo-id>/ # 代码根：各修改仓的 git worktree
```

- workspace 可以包含多个项目，也可以本身就是项目仓库；不要求 workspace 是 git 仓。
- 项目 checkout 可在 workspace 内外。每个任务在 TASK「涉及仓库」登记 repo_id、source_repo、worktree、branch、base。
- OpenSpec 命令 cwd 是 workspace；读改代码、测试、提交 cwd 是对应 worktree。项目自己的 `openspec/` 不自动写。
- 理解与设计（explore / diagnose / grill / design / approve）、交付结构（不拆 / 切片 / 子任务）、执行方式（direct / OpenSpec）分别判断。worktree、confirm_mode、worker 数量也不绑定这些选择。

## 2. 最小主干与动态循环

固定不变的是：目标与 criterion → 当前最小计划 → 动态 references → verify → close。中间不设固定顺序和 skip/full 档位。

意图与 PLAN 的确认属于对应 reference 的完成门，不新增固定阶段；未命中停点的进度复述不改变路由，也不要求用户回复。

每轮按 [router.md](router.md) 重新判断 enter / continue / skip / reopen。reference 依赖产物和证据，不依赖“上一阶段”；统一结构见 [ref-contract.md](ref-contract.md)。相同输入下不得无理由重复进入同一环节；没有新证据时必须改变动作或报告真阻塞。

## 3. TASK.md 状态

```yaml
slug: <kebab-case>
parent: null | <parent-task-id>
status: pending | active | blocked | done | archived
current_ref: intake | plan | explore | diagnose | grill | design | approve | decompose | execute | review | verify | close | null
confirm_mode: human | goal
execution: direct | openspec | null
criterion: "<一条可检查的话>"
driver: null | "<task-id>-driver"
created: YYYY-MM-DD
updated: YYYY-MM-DD
# 旧字段与 gate_bypass 等按需兼容保留；archived / reopened 在动作发生时写
```

- `pending`：子任务已规划但未就绪；`active`：可推进；`blocked`：只表示需要外部输入或环境解锁。
- `current_ref` 只是当前动作，不是完成百分比。direct 任务的实施进度看 PLAN checkbox；OpenSpec 任务看 change checkbox；父子结构看 ROADMAP 与子 TASK。
- `execution` 和 `driver` 不决定任务生命周期。driver 归档后若未验收，`current_ref: close` 或 `verify`，绝不能直接推导 done。
- `status: done` 必须同时满足：[done.md](done.md) 全过、SUMMARY.md 存在、所有直接子任务 done。`task_state.py update --status done` 机械检查这些条件。
- 状态写入与 INDEX 重建使用 `scripts/task_state.py`；INDEX 是派生物，不是第二状态源。

## 4. 任务目录

```text
tasks/
├── INDEX.md
├── ongoing/<parent>/
│   ├── TASK.md               # 热状态：目标、判据、当前/下一动作、repo 与产物指针
│   ├── PLAN.md               # 当前计划；容器型父任务只写协调与集成
│   ├── ROADMAP.md            # 仅拆分：切片 / 子任务 / 集成项与依赖
│   ├── context/current.md    # 当前有效事实与假设
│   ├── context/sources.md    # 证据索引
│   ├── design/               # 按需：grill、design、契约、ADR
│   ├── reviews/              # 按需：approve / review
│   ├── evidence/             # 按需：复现、测试、集成、性能证据或指针
│   ├── decisions.md          # 决定与 superseded 关系
│   ├── history.md            # 冷历史：路由、更正、状态迁移
│   ├── SUMMARY.md            # close 产出
│   └── subtasks/<child>/     # 结构同父任务；只拆一层
└── archive/<yyyy-mm-dd>/<parent>/
```

子任务内部再拆只能是切片。父任务若有子任务则不直接写业务代码、不持实施 driver，只维护共享契约、依赖和集成验收；每个子任务独立选择 direct 或 OpenSpec。

## 5. decompose 与交付原子性

[decompose.md](decompose.md) 在多个交付边界、多项目、增量反馈或单次难以回归时自动进入，可在 explore / design / execute 后重入。

- **切片**：必须同一交付一起落地，共享任务分支，后片依赖前片未发布代码；一个任务 driver 下的子 changes。
- **子任务**：可独立实施和验证，通过明确契约集成，可有独立分支与交付节奏；位于父任务 `subtasks/`。
- 是否有“代码依赖”不是唯一判据；必须原子落地的是切片，能按契约独立交付的可作有依赖子任务。
- decompose 一次创建所有子任务的轻量 pending TASK，细节按就绪顺序展开。一个子任务 blocked 只停其依赖链。
- 全部子任务 done 后父任务进入 verify，执行集成项和总判据；不能按子任务数量直接 done。

## 6. 执行与 handoff

所有 git 代码任务默认调用 `<taskflow>/scripts/prepare_worktree.py`，direct 与 OpenSpec 共用 [../taskflow/references/worktree.md](../../taskflow/references/worktree.md)。

OpenSpec 只在用户要求、长期 spec、多会话 / 多 worker 编排或正式 change 产物有需要时使用。只有 OpenSpec 路径走 [handoff.md](handoff.md) 与 `check_handoff.py`；approve 可按 router 跳过，此时交接节记录 `批准：not-required: <理由>`。direct 路径不建 driver、不跑 handoff 门。

## 7. 意图与认知变更

用户改目标 / criterion，或新事实推翻输入时：

1. 回 [intent.md](intent.md) 纠偏；criterion 变化按确认协议放行。
2. 在 `context/current.md` 把旧认知标为 `refuted` / `superseded`，写当前结论和证据。
3. `history.md` 追加更正原因，`decisions.md` 用 superseded 关联旧决定。
4. 只使受影响的 plan / design / checkbox 失效并重入对应 reference；已完成且不受影响的历史不改写。
5. 已执行的 OpenSpec 任务只增删改未勾项，必要时建修订子 change；已归档历史不改。

## 8. 上下文与并发

默认只读 TASK、当前计划或 ROADMAP 就绪行、context/current、当前 reference 及其所需产物。history、全部子任务设计、全部 changes 和原始日志不默认加载。

TASK 约 6 KB、context/current 约 8 KB 是压缩软预算；超出时把冷历史与原文下沉，保留判据和证据指针。父会话不加载所有子任务上下文，worker 只收本人范围、判据、契约、worktree 和证据要求。

只读 explore / review、不同子任务或不同仓库可并行；同任务同仓写操作串行。worker 不直接改父 TASK；父编排者统一更新协调状态。详见 [../taskflow/references/multi-worker.md](../../taskflow/references/multi-worker.md)。

## 9. 术语

| 术语 | 含义 |
|---|---|
| reference | 有进入 / 跳过 / 输入 / 产出 / 完成门 / 重入规则的可组合环节 |
| workspace | 任务与 OpenSpec 的统一规划根 |
| worktree | 某修改仓属于某任务的 git worktree，不是普通目录副本 |
| criterion | 判断任务是否完成的一条可检查原文 |
| ROADMAP | 父子结构、依赖、涉及仓库和集成项唯一真源 |
| 切片 | 同一任务、同一交付分支内按依赖滚动的 change |
| 子任务 | 父任务下可独立实施验证、按契约集成的任务 |
| handoff | direct/OpenSpec 选择后，仅 OpenSpec 进入 driver 前的载荷核对动作 |
| 热状态 | resume 默认读取的最小 TASK / 当前事实 / 当前计划 |
