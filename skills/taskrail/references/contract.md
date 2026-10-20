# taskrail 契约（阶段 / 载荷 / 目录 / 术语）

task 系列的**唯一真源**：`taskrail` / `task-explore` / `taskflow` / `task-intent` 与本文有出入时以本文为准；各 skill 只写执行细则。停点见 [confirm-protocol.md](confirm-protocol.md)，对用户说话见 [user-report.md](user-report.md)。

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

- 拿不准往 `skip` 靠并说一句理由。
- `skip` 不建 driver、不走 OpenSpec、不建 worktree：在主工作树直接改，改动留给用户提交；验证命令与结果写入 `TASK.md`「验证」节，过 [done.md](done.md) 即 `done`。
- 实现中发现超出局部（跨模块、要拆切片）→ 升 `full`，补 explore / approve / handoff。已在主工作树改过的文件列进「已做决定」；建 worktree 时基线用 `HEAD`，用 `git diff HEAD -- <这些文件> | git -C worktrees/{slug} apply` 带过去，之后只在 worktree 里改。
- 旧任务里的 `simple` 按 `skip` 读，`medium` / `complex` 按 `full` 读；下次写 `TASK.md` 时改成新值。
- UI 强度跟「是否观感交付」走，不跟档位（[ui-delivery.md](ui-delivery.md)）。
- `grill` 是 explore 的子步骤（委托 `grilling`，自问自答），不占 phase。大范围拆分见 [large-scope.md](../../task-explore/references/large-scope.md)，默认单任务。

## approve 出口与交接（本节是唯一出处）

1. approve 冻结且尚未 `handed-off` 时，唯一下一步是 `handoff`（步骤见 task-explore [handoff.md](../../task-explore/references/handoff.md)）。方案含实施动作却未交接时不归档；用户明确说放弃 / 不实施，才走探索侧 archive。
2. 查证项与外部依赖写进「带进实现的未决」，照常交接。
3. 交接只带指针与判据：`criterion` 原文、方案与 `approve/APPROVED.md` 路径。
4. `taskflow/scripts/check_handoff.py <root> <slug>` exit 0 是唯一机械门；不过就回 handoff 补齐。
5. 同一方案的多条实施线建成 `{slug}-driver` 的子 change。
6. `criterion` 只按下节「意图变更」改；方案落盘不是完成。

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
- `tasks/` 与 OpenSpec change 目录留在主工作树（planning root）；full 档代码改在修改仓的 `worktrees/{slug}`（taskflow Driver 协议）。
- 运行产物（证据）落仓外，`TASK.md` 只存指针（`evidence_root`）；单任务产物只写当前任务目录。

## TASK.md 元信息

写在 `TASK.md` 开头的 `---` frontmatter（`check_handoff.py` 按它解析），字段只取下列：

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
# 按需，只在对应动作发生时写：
handed-off: YYYY-MM-DD
archived: YYYY-MM-DD
reopened: YYYY-MM-DD
gate_bypass: "<YYYY-MM-DD> user-confirmed: <用户原话>"
```

- `phase` 只取上列枚举，命令名（`resume` / `handoff` 等）留在对话里。
- 进度：approve 前认 `phase` + 阶段产物；propose 之后只认 OpenSpec checkbox。`handed-off` 不等于 `done`。
- **一本账**：`TASK.md` 是唯一任务账；所有决定只追加到「已做决定」表（决定 / 理由 / 可逆 / 来源阶段）。
- `status` 随 `phase` 走：wizard–approve（及 skip 的 apply）为 `ongoing`；handoff 后 `handed-off`；完成清单过为 `done`；归档 `archived`；`blocked` 停在原 phase。

## 阶段载荷

缺则停在上一 phase，补齐再进：

| 进入 | 必须已有 |
|------|----------|
| explore / design | `wizard/intent.md`（`confirmed` 或 `assumed`）+ `criterion` + `wizard/plan.md`（目标 / 判据 / 步骤 / 不做） |
| approve | design 产出路径 + `criterion` + 「不做」 |
| propose | `approve/APPROVED.md` + `status: handed-off` + `driver` + `check_handoff.py` exit 0 |
| apply | full：driver `tasks.md` 已由 propose 产出；skip：wizard 已定稿 |
| archive（探索侧） | 用户确认关闭 |

## 执行座位

高噪声 legwork（摸底、调研、起草、实现、评审、复跑）宜交 worker（宿主 subagent；点名 Endpoint 走 `agent-roster`）；没有就主会话按同一落点自做。闸口与对用户的话留在主会话。worker 详情落盘，只回结论 / 路径 / 未决。`phase` / `status` / `driver` 只由编排者写。多 worker 并行见 [multi-worker.md](../../taskflow/references/multi-worker.md)。

## 对用户说话

规则与前后对比只在 [user-report.md](user-report.md)。

## 术语

| 术语 | 含义 |
|------|------|
| 完成判据（`criterion`） | 一条可检查的话，判断任务是否做完；原文逐字传递 |
| 交付标准 | 判据之外、本任务应有的可检查交付面要求；没有写「无」 |
| 档位（`tier`） | `skip` / `full`，wizard 判定，下游沿用 |
| 交接（handoff） | approve 之后转给 taskflow 的动作：`status:=handed-off`，`phase:=propose`，写 `driver` |
| 交接载荷 | `TASK.md`「## 交接」节：判据、交付类别、适用门包、指针；`check_handoff.py` 只认它 |
| driver | OpenSpec change `{slug}-driver`，只编排子 change `{slug}-<slice>` |
| 真阻塞 / 卡住 | 必须停下等用户的情况，清单只在 [user-report.md](user-report.md) 第 5 节 |
| 严重级 | P0 = Blocker、P1 = Major，挡路；P2 / Minor 不挡路 |
| 台账（ledger） | `tasks/` 下单任务 `TASK.md` + 派生 `INDEX.md` |
| grill | explore 阶段的自问自答拷问，只追细节、不重问意图 |
