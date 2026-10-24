# 动态路由

每次进入、继续、跳过或重入前读。状态枚举与父子任务规则见 [contract.md](contract.md)。

## 路由算法

1. 检查 criterion：为空或不可检查，回 [intent.md](intent.md)；代码任务没有当前最小计划，进 [plan.md](plan.md)。
2. 当前 reference 的输入与完成门仍成立才 continue；产物已满足且没有失效信号就 skip / exit。
3. 按下表选能解决当前最关键不确定性的一个 reference；一次只选一个。
4. 代码实施统一进 taskflow execute；实施后有证据才进 verify，最终 close。
5. 把 enter / skip / exit / reopen 与一句理由追加到 history.md；不维护第二份完成百分比。

## 信号与选择

| 当前事实 | 选择 | 可跳过的证据 |
|---|---|---|
| 改点、依赖、约束或影响面未知 | explore | 当前 commit 下已有相关入口与约束证据 |
| bug / 性能 / flaky 原因未证明 | diagnose | 原因已有一手证据，或只是明确文案 / 配置错误 |
| 多个方案带来实质外部取舍，约束冲突 | grill | 没有会改变方案的关键未知或取舍 |
| 公共 / 内部契约、数据、架构、迁移变化 | design | 完全沿用现有模式且无结构 / 契约变化 |
| 用户要求审批、难逆高风险、判据或重要外部行为改变 | approve | 普通可逆改动，或 goal 下无强制批准条件 |
| 多交付、多项目、需要增量反馈或一次难回归 | decompose | 一个连贯改动即可实施并验证 |
| 高风险、公共契约、复杂 diff、安全 / 性能敏感 | review | 小且可逆改动由 execute 做 diff 自检，可不派独立 reviewer |
| 全部实现产物就绪 | verify | 无；代码任务不得跳过验证 |
| 验证全过 | close | 无；done 与归档必须经过 close |

任务类型只是信号，不是固定路线：跨模块不必然 grill / OpenSpec；改动小但原因未知仍需 diagnose；大型机械改动可 decompose 而不 design。

## 执行中重新路由

- 找不到入口或事实冲突 → explore。
- 测试 / 修复失败且原因未知 → diagnose；原因明确 → execute。
- 新出现重要方案取舍 → grill；新发现契约 / 数据 / 迁移问题 → design，必要时 approve。
- 新出现独立交付或集成边界 → decompose；只追加未完成的 roadmap 项。
- reviewer Blocker / Major 指向实现 → execute；指向方案 → design / grill。
- 子任务完成 → 父任务选下一就绪项；全部完成 → 父任务 verify。
- criterion 改变 → intent；只使受影响产物失效。
- 工具 / 传输故障按退避重试，不伪装成代码根因；缺权限 / 凭据才 blocked，其他就绪项继续。

## 防振荡与上下文

同一 reference 在输入和证据没有变化时不得重跑完整动作；连续两次没有新证据就不能继续盲试，应换动作（explore ↔ diagnose、grill）或按真阻塞停。resume 先 reconcile，不机械沿用旧 current_ref。

每次只加载选中的 reference 及其必需产物。父任务只读 ROADMAP、共享契约和就绪子 TASK；不把兄弟子任务、历史和原始日志带入。
