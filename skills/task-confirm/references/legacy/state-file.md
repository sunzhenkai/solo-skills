# 状态文件：schema 与事件推断顺序

> **legacy（已迁入 references/legacy/）。** 非 taskrail 进度真源；仅旧 goal 计数器可选使用。迁移网格见 [state-machine.md](state-machine.md)。

goal 运行时的**计数器状态**落在一个 YAML 文件里，由 `scripts/goal_transition.py` 读写。本文件规定字段、落点、首轮模板，以及「没有生产者戳时怎么机械地推断事件」。

**红线**：本文件只存计数器（state / exit_point / autocontinue_count / last_input_event / blocked / handoff_summary），**不存迁移规则**——迁移规则唯一真源是 [state-machine.md](state-machine.md) 的网格。

## 落点

state 文件是**运行产物**，落在仓库之外。推荐沿用 taskrail 的 `evidence_root` 风格：

```text
<task 运行目录>/goal-state.yaml
```

路径由进入方指定，随 goal 生命周期存续，goal 标完成或 blocked 交接后可归档，不删：

- **被 taskrail 以 goal 模式推进**：建任务时写入 `goal-state-file:` / `evidence_root`（默认 `<evidence_root>/goal-state.yaml`）。本文件不替它决定落点。
- **独立 `/goal` 进入**：由执行者按上表落 `<task 运行目录>/goal-state.yaml`。
- 可在每轮 prompt 里盖 `goal-state-file: <path>` 戳覆盖上述默认。

新编排以 `TASK.md.phase` 为进度真相；本状态机为可选计数器资产。

## Schema（封闭字段集）

```yaml
# goal-state.yaml — 计数器与上轮输入，不存规则
state: 已停                    # 四状态之一；首轮由执行者按方案路由写入
exit_point: 降级未确认          # 命中退出点的标签；未命中为 null
autocontinue_count: 2          # 已停 × goal 自动续跑 已连续发生次数；其它事件清零
last_input_event: goal 自动续跑 # 上一轮的事件名（封闭枚举 11 种之一）
blocked: false                 # 是否已 blocked 交接
handoff_summary: null          # blocked 时的交接摘要占位（已完成/未完成/证据/下一步）
```

字段规则：

- 只列上表 6 个 key；新增 key 会被 `goal_transition.py` 静默忽略（防止漂移）。
- 值都是标量（字符串 / 整数 / 布尔 / null），不嵌套、不列表。
- `autocontinue_count` 只在「已停 × goal 自动续跑」时递增；其它事件触发时由脚本清零。
- `blocked: true` 后脚本不再主动改 `state`，等用户处置。

## 首轮模板

goal 启动（或方案路由确定状态）时，由执行者写入：

```yaml
state: 执行中                  # 或按路由写 已交接 / 已停
exit_point: null
autocontinue_count: 0
last_input_event: null
blocked: false
handoff_summary: null
```

state-file 不存在时，脚本按 `--state` 回退并在 `--write` 时创建。

## 事件推断顺序（无生产者戳时的降级路径）

goal 系统若没在每轮 prompt 开头盖 `goal-event: <tag>` 戳，执行者**按以下顺序逐条比对**，命中即停，不跳过、不合并：

1. 本轮 prompt 与上一轮**逐字相同** → `goal 自动续跑`
2. 消息点名或按意图命中退出点已列的授权项（含「仍按此方案执行」「接受降级」「按降级表全部确认」；意图命中须复述「理解为授权 X，若无纠正即生效」后生效，不可逆动作除外） → `用户授权`
3. 消息为「继续」「接着做」「go on」类短句、无其它语义 → `用户继续`
4. 消息含改向词（「改」「换成」「不要」「重新」「升档」「换个方案」「先别做」） → `用户改向`
5. 消息是对执行者提问的事实性答复、不含授权/改向 → `用户补充信息`
6. 以上都不命中 → 按 state-file 里 `last_input_event` 与当前环节推断：
   - 上次处于完善中（路由以「完善中」开头） → `审阅未收敛`
   - 上次处于写完之后且 checkbox 有推进 → `步骤推进`
   - 上次处于写完之后且判据成立 → `判据成立`
   - 其它情况 → 走「无进展轮」兜底

**判断细节**：

- 「逐字相同」去掉前后空白与时间戳类差异后比对；防止 goal 系统带轻微噪声。
- 改向词列表是封闭集合；新增词要改本表 + 测试。
- 推断顺序本身**只是分类辅助**，分类错了脚本会返回 `defined: false` 走无进展轮——最坏结局仍是 blocked 交接，不会越权。

## 生产者戳（优先路径）

goal 系统若能改，每轮 prompt 开头加一行：

```text
goal-event: auto-continue
goal-round: 3
goal-state-file: <path>
```

执行者看到戳就直接 `--event-tag auto-continue` 调脚本，跳过上面的推断顺序。tag → 事件名的映射表内置在 `scripts/goal_transition.py` 的 `EVENT_TAGS`，本文件不重复列。
