# 台账：workspace、绑定与恢复

写 TASK / INDEX 或绑定任务前读。目录与字段以 [contract.md](contract.md) 为准。

## workspace 解析

绑定由编排者自行判定，不拿记账问题问用户；按优先级选择，并一句话说出决定和理由：

1. 用户明确指定的 workspace 或当前会话已有绑定。
2. 从 cwd 向上找已有 `tasks/INDEX.md` 的 workspace。
3. 无上层 workspace 且位于独立 git 项目时，使用项目根。
4. 空目录首次使用时以 cwd 为 workspace。

确定后所有脚本显式传 workspace，不依赖隐式 cwd。workspace 持 `tasks/`、按需的 `openspec/` 和 `worktrees/`；项目 checkout 可在其内外。

## 绑定与新建

- 先读 INDEX；缺失或漂移时运行 `task_state.py rebuild-index <workspace>`。
- 同一件事恢复，无关事项新建；用户只说“继续”时恢复最近更新任务，拆过的任务按 ROADMAP 取下一就绪项。
- task id 用唯一 kebab-case；历史同名或 branch 冲突时加短后缀，不覆盖、不复用不明身份。
- 新建使用 `task_state.py init`；子任务只能由 [decompose.md](decompose.md) 用 `--parent` 创建。
- 是否把 tasks 纳入 git 由项目决定，不改 .gitignore。

## 原子更新与索引

TASK 更新、done 门和 INDEX 重建统一用 `scripts/task_state.py`。INDEX 是派生物，不手改状态；多会话写同一 workspace 时使用脚本锁，不靠“先读后写”碰运气。冷历史追加到 history，决定写 decisions，避免 TASK 无界增长。

## resume / explain

1. 跑 `task_state.py reconcile <workspace> <task-path> [--repair] [--json]`。
2. 核对 workspace、TASK、ROADMAP / 子任务、worktree / driver 身份；冲突时停止代码写入，不 reset 或覆盖。
3. 只读热状态与当前 reference 所需产物；旧 `phase/tier/status` 按现有产物兼容理解，不映射回固定双流程。
4. `done` 缺 SUMMARY 或子任务未完成时，repair 回 active / close；子任务全 done 的父任务转 verify。
5. explain 只读报告当前动作与理由、跳过 / 重入、子任务状态、worktree / driver 和下一动作。

归档任务先报告路径；用户明确 reopen 才按 archive-reopen 搬回。
