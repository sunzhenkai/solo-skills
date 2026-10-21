# taskrail 契约（阶段 / 载荷 / 目录 / 术语）

task 系列的**唯一真源**：taskrail 各阶段细则或 `taskflow` 与本文有出入时，以本文为准；它们只写执行细则。停点见 [confirm-protocol.md](confirm-protocol.md)，对用户说话见 [user-report.md](user-report.md)。

## 流程

```text
confirm_mode: human | goal

wizard → design(grill) → approve → [handoff] → propose → apply → archive → done
                            ↑ handoff 是动作，不是 phase
```

| 档位 (`tier`) | 路径 | 何时 |
|---------------|------|------|
| `skip` | wizard → apply（直接实现 + 验证）→ done | 局部修改，一句话说得清改动 |
| `full` | wizard → design(grill) → approve → handoff → propose → apply → archive → done | 其余：跨模块 / 仓库、要拆步骤、涉及面广 |

- 拿不准往 `skip` 靠并说一句理由。
- `skip` 不建 driver、不走 OpenSpec、不建 worktree：在主工作树直接改，改动留给用户提交；验证命令与结果写入 `TASK.md`「验证」节，过 [done.md](done.md) 即 `done`。
- 实现中发现超出局部（跨模块、要拆切片）→ 升 `full`，补 design / approve / handoff。已在主工作树改过的文件列进「已做决定」；建 worktree 时基线用 `HEAD`，用 `git diff HEAD -- <这些文件> | git -C worktrees/{slug} apply` 带过去，之后只在 worktree 里改。主工作树里那份改动保持原样，完成通知里写明它已带进任务分支。
- 旧任务里的 `simple` 按 `skip` 读，`medium` / `complex` 按 `full` 读，`phase: explore` 按 `design` 读；下次写 `TASK.md` 时改成新值。
- UI 强度跟「是否观感交付」走，不跟档位（[ui-delivery.md](ui-delivery.md)）。
- `grill` 是 design 的第一步（自问自答，方法见 [design.md](design.md)），不占 phase。
- 拆分在 wizard 定，默认不拆；拆了按 [large-scope.md](large-scope.md)：同一份交付分成一个 driver 下的切片，按依赖滚动展开；要分别交付的才拆子任务。拆成子任务的父任务走 wizard → apply（推进子任务）→ done，不 design、不建 driver。

## approve 出口与交接（本节是唯一出处）

1. approve 冻结且尚未 `handed-off` 时，唯一下一步是 `handoff`（步骤见 [handoff.md](handoff.md)）。方案含实施动作却未交接时不归档；用户明确说放弃 / 不实施，才走任务归档（未完成关闭）。
2. 查证项与外部依赖写进「带进实现的未决」，照常交接。
3. 交接只带指针与判据：`criterion` 原文、方案与 `approve/APPROVED.md` 路径。
4. `<taskflow>/scripts/check_handoff.py <root> <slug>` exit 0 是唯一机械门（核对已批准、判据非空、driver 名、交接载荷）；不过就回 handoff 补齐。
5. 同一方案的多条实施线是切片，建成 `{slug}-driver` 的子 change。
6. `criterion` 只按下节「意图变更」改；方案落盘不是完成。

## 意图变更

wizard 之后用户改主意，或 grill / design / apply 发现与 `wizard/intent.md` 冲突：

1. 重跑意图确认（[intent.md](intent.md)），改写 `wizard/intent.md` 并在纠偏记录追加一行。
2. 「做完的样子」变了 → 显式改 `criterion`（human 等用户说可以；goal 审阅收敛），记入「已做决定」。这是唯一合法改写。
3. 未 `handed-off`：只改细节留在当前 phase；改范围 / 判据回 `wizard` 或 `design`，已 approve 的重新 approve。
4. 已 `handed-off`：经 taskflow 开修订子 change，未勾 checkbox 按新判据重排。

## 交接后的位置

`handed-off` 之后，编排者每做完一步就回写 `phase`；resume 时，或 `phase` 与 driver 对不上时，以 driver 状态为准推导并回写：

| driver 状态 | `phase` |
|---|---|
| `tasks.md` 还没有 | `propose` |
| 有未勾项 | `apply` |
| 全勾、driver 未归档 | `archive` |
| driver 已归档 | `done` |

## 目录

```text
tasks/
├── INDEX.md
├── ongoing/{slug}/
│   ├── TASK.md
│   ├── wizard/intent.md   # 意图确认版
│   ├── wizard/plan.md     # 拆了的含「路线图」
│   ├── evidence/intent/   # 意图摸底详情
│   ├── design/            # 方案；grill 纪要 design/grill.md
│   ├── approve/           # 评审意见 + APPROVED.md
│   └── subtasks/{sub}/    # 子任务：一个子任务一个目录，结构同上（只拆一层；意图沿用父任务）
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
phase: wizard | design | approve | propose | apply | archive | done
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
- `status` 随 `phase` 走：wizard–approve（及 skip 与父任务的 apply）为 `ongoing`；handoff 后 `handed-off`；完成清单过为 `done`（做完归档后仍是 `done`）；未完成就关闭为 `archived`；`blocked` 停在原 phase。

## 阶段载荷

缺则停在上一 phase，补齐再进：

| 进入 | 必须已有 |
|------|----------|
| design | `wizard/intent.md`（`confirmed` 或 `assumed`；子任务用父任务的）+ `criterion` + `wizard/plan.md`（目标 / 判据 / 步骤 / 不做） |
| approve | design 产出路径 + `criterion` + 「不做」 |
| propose | `approve/APPROVED.md` + `status: handed-off` + `driver` + `check_handoff.py` exit 0 |
| apply | full：driver `tasks.md` 已由 propose 产出；skip：wizard 已定稿；父任务：路线图已定稿 |
| 任务归档 | 已 `done`（父任务要子任务全部 `done`）；未完成的要用户明确说关闭 |

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
| 归档 | `phase: archive` 只指归档 driver；任务归档指把任务目录搬进 `tasks/archive/`，`done` 后同轮做 |
| 交接载荷 | `TASK.md`「## 交接」节：判据、交付类别、适用门包、指针；`check_handoff.py` 只认它 |
| driver | OpenSpec change `{slug}-driver`，只编排子 change `{slug}-<slice>` |
| 路线图 | 拆分时写在 `wizard/plan.md` 的表：每项一句话目标、子判据、依赖 |
| 切片（slice） | driver 下的一个子 change，与其他切片同一条任务分支，可依赖前一片的代码 |
| 子任务 | `ongoing/{parent}/subtasks/{sub}/` 下要分别交付的任务，有自己的 driver 与分支，与兄弟子任务无代码依赖 |
| 真阻塞 / 卡住 | 必须停下等用户的情况，清单只在 [user-report.md](user-report.md) 第 5 节 |
| 严重级 | P0 = Blocker、P1 = Major，挡路；P2 / Minor 不挡路 |
| 台账（ledger） | `tasks/` 下单任务 `TASK.md` + 派生 `INDEX.md` |
| grill | design 第一步的自问自答拷问，只追细节、不重问意图 |
