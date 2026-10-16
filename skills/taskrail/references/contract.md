# taskrail 契约（阶段 / 载荷 / 闸口 / 目录 / 术语）

task 系列的**唯一真源**。`taskrail` / `task-explore` / `taskflow` / `task-intent` 与本文有出入时以本文为准；各 skill 只写执行细则，不另造阶段枚举或术语定义。

职责收敛：taskrail 管步骤与完成；task-intent 管意图；[user-report.md](user-report.md)（+ 薄确认 [confirm-protocol.md](confirm-protocol.md)）管对用户的输出与交互。Web UI、多 worker、大范围拆分、质量画像是可选包，命中才读。

## 流程

```text
confirm_mode: human | goal

wizard → explore(grill) → design → approve → [handoff] → propose → apply → archive
                                             ↑ handoff 是动作，不是 phase
```

| 档位 (`tier`) | 路径 | 何时 |
|---------------|------|------|
| `skip` | wizard → apply（直接实现 + 验证）→ done | 局部修改，一句话说得清改动 |
| `full` | wizard → explore(grill) → design → approve → handoff → propose → apply → archive | 其余：跨模块 / 仓库、要拆步骤、涉及面广 |

- 拿不准往 `skip` 靠并说一句理由；实现中发现超出局部（跨模块、要拆切片）→ 升 `full`，补 explore / approve / handoff。
- `skip` 不建 driver、不走 OpenSpec：验证命令与结果写入 `TASK.md`「验证」节，过 [done.md](done.md) 即 `done`。
- 旧任务目录里的 `simple` 按 `skip` 读，`medium` / `complex` 按 `full` 读；下次写 `TASK.md` 时顺手改成新值。
- UI 强度不跟档位走，跟「是否观感交付」走（见 [ui-delivery.md](ui-delivery.md)）。

## 非 phase 动作

| 动作 | 时机 | 影响 |
|------|------|------|
| `grill` | `explore` 的子步骤，委托 `grilling`，自问自答 | 不占 phase |
| `handoff` | approve 冻结后、propose 前；步骤见 task-explore [handoff.md](../../task-explore/references/handoff.md) | `status:=handed-off`，`phase:=propose`，写 `driver` |

大范围拆分（父伞 / 子任务）是可选附录：[large-scope.md](../../task-explore/references/large-scope.md)。默认单任务。

## approve 出口与交接（本节是唯一出处）

1. approve 冻结且尚未 `handed-off` 时，唯一下一步是 `handoff`；不列 archive、另起任务、继续探索。方案含实施动作却未交接时拒绝 archive。仅当用户明确说放弃 / 不实施，才走探索侧 archive。
2. 查证项与外部依赖写进「带进实现的未决」，不阻断交接。
3. 交接只带**指针与判据**：`criterion` 原文、方案与 `approve/APPROVED.md` 路径（可附 git 短 hash），不复制方案、画像或降级原文。
4. `taskflow/scripts/check_handoff.py <root> <slug>` exit 0 是**唯一机械门**；不过就回 handoff 补齐，不在别处复述它的核对项。
5. 同一方案的多条实施线建成 `{slug}-driver` 的子 change，不另起 driver。
6. 禁止用当轮叙事改写 `criterion`；方案落盘不是完成。

## 意图变更

wizard 之后用户改主意，或 grill / design / apply 发现与 `wizard/intent.md` 冲突：

1. 重跑 `task-intent`，改写 `wizard/intent.md` 并在纠偏记录追加一行。
2. 「做完的样子」变了 → 显式改 `criterion`（human 等用户说可以；goal 审阅收敛），记入「已做决定」。这是唯一合法改写。
3. 未 `handed-off`：只改细节留在当前 phase；改范围 / 判据回 `wizard` 或 `design`，已 approve 的重新 approve。
4. 已 `handed-off`：经 taskflow 开修订子 change，未勾 checkbox 按新判据重排。

## 目录

```text
tasks/
├── INDEX.md
├── ongoing/{slug}/
│   ├── TASK.md
│   ├── wizard/intent.md   # task-intent 确认版
│   ├── wizard/plan.md
│   ├── evidence/intent/   # 意图摸底详情
│   ├── explore/           # grill 纪要（可选）
│   ├── design/
│   └── approve/           # 评审意见 + APPROVED.md
└── archive/{yyyy-mm-dd}/{slug}/
```

- 经 `taskrail` 推进的任务一律建 `tasks/ongoing/{slug}/`；无 `tasks/` 在仓库根直接建，一句话说明。
- 运行产物（证据）落仓外，`TASK.md` 只存指针（`evidence_root`）。
- 单任务产物只写当前任务目录（不写仓库根 `CONTEXT.md`、`docs/adr/`、`docs/design/`）。

## TASK.md 元信息（封闭字段）

```yaml
slug: <kebab-case>
parent: <父 slug；仅子任务>
status: ongoing | handed-off | blocked | done | archived
phase: wizard | explore | design | approve | propose | apply | archive | done
confirm_mode: human | goal
tier: skip | full
criterion: "<完成判据原文一条>"
driver: null | "{slug}-driver"
evidence_root: <仓外路径或 null>
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

- `phase` 只取上列枚举；命令名（`new` / `save` / `resume` / `handoff` 等）不得写入。
- approve 前进度认 `phase` + 阶段产物；propose 之后只认 OpenSpec checkbox。
- **一本账**：`TASK.md` 是唯一任务账；所有决定只追加到「已做决定」表（决定 / 理由 / 可逆 / 来源阶段）。driver 只是 OpenSpec 执行记录。`handed-off` 不等于 `done`。
- `status` 随 `phase` 走：wizard–approve（及 skip 的 apply）为 `ongoing`；handoff 后 `handed-off`；完成清单过为 `done`；归档 `archived`；`blocked` 停在原 phase。

## 阶段载荷

缺则停在上一 phase，不让下游猜：

| 进入 | 必须已有 |
|------|----------|
| explore / design | `wizard/intent.md`（`confirmed` 或 `assumed`）+ `criterion` + `wizard/plan.md`（目标 / 判据 / 步骤 / 不做） |
| approve | design 产出路径 + `criterion` + 「不做」 |
| propose | `approve/APPROVED.md` + `status: handed-off` + `driver` + `check_handoff.py` exit 0 |
| apply | full：driver `tasks.md` 已由 propose 产出；skip：wizard 已定稿 |
| archive（探索侧） | 用户确认关闭 |

## 执行座位

高噪声 legwork（摸底、调研、起草、实现、评审、复跑）宜交 worker（宿主 subagent；点名 Endpoint 走 `agent-roster`）；没有就主会话按同一落点自做，不停下。闸口与对用户的话不外派。worker 详情落盘，只回结论 / 路径 / 未决。`phase` / `status` / `driver` 只由编排者写。多 worker 并行见 [multi-worker.md](../../taskflow/references/multi-worker.md)。

## 确认闸口

wizard 定稿、design 定稿、approve、危险操作前。一律按 [confirm-protocol.md](confirm-protocol.md)：说决定、真阻塞才停。

## Skill 归属

| Skill | 职责 |
|-------|------|
| `taskrail` | 唯一编排入口；绑定任务；推进阶段；[done.md](done.md) |
| `task-intent` | 意图：探索 → 复述 → 纠偏 |
| `task-explore` | explore / design / approve / handoff（台账细则） |
| `taskflow` | driver + propose / apply / archive；checkbox |

## 对用户说话

规则只在 [user-report.md](user-report.md)。前后对比：

- 闸口 —— 前：「gate=approve；tier=full；criterion 待确认；P1×1」；后：「方案定了，做完的标准是导出 5 秒内。大文件内存占用有点风险，我先加个上限再动手。接下来我就往下做。」
- 进度 —— 前：「driver checkbox 3/5，slice-2 apply done」；后：「五步里做完了三步，第二部分已经实现并通过测试。接下来做剩下两步。」
- 评审摘要 —— 前：「roles=engineer,qa；Blocker 0；Major 2」；后：「工程和测试两个角度看过了，没有必须马上修的问题；有两处该补：超时处理和一条回归测试，我这就补上。」

## 术语

| 术语 | 含义 |
|------|------|
| 完成判据（`criterion`） | 一条可检查的话，判断任务是否做完；原文逐字传递 |
| 交付标准 | 判据之外、本任务应有的可检查交付面要求；没有写「无」 |
| 档位（`tier`） | `skip` / `full`，wizard 判定，下游不重判 |
| `handed-off` | 已交接 taskflow，任务仍在 `ongoing/`，之后进度只认 checkbox |
| 交接载荷 | `TASK.md`「## 交接」节：判据、交付类别、适用门包、指针；`check_handoff.py` 只认它 |
| driver | OpenSpec change `{slug}-driver`，只编排子 change `{slug}-<slice>` |
| 真阻塞 | 必须停下等用户的情况，清单只在 [user-report.md](user-report.md) 第 5 节 |
| 授权 | 用户明确接受某个已点名的动作；单独「继续」不算对危险动作的授权 |
