# P3 瘦身：合并 5 个碎片 reference、按 SSOT 消除多点复读并解耦重复字面测试

- target: skills/taskrail
- mode: update
- patch: 20261127-005000-p3-slim-ssot-and-test-decouple
- risk: medium
- status: proposed

## Intent

按 `writing-for-agents` 信息层级与单一真源（SSOT）原则，为 `taskrail` 瘦身降噪、降低运行时上下文负担并解除脆弱的跨文件重复字面测试耦合：

1. **合并 5 个超薄碎片 reference（`references/` 从 26 减至 21 个）**：
   - `ledger-concurrency.md`（9 行）→ 并入 `ledger.md`「并发写入」；
   - `external-precedent.md`（8 行）→ 并入 `explore.md`「外部参照（按需）」；
   - `archive-reopen.md`（17 行）→ 并入 `close.md`「归档与重开」；
   - `design-detail.md`（28 行）→ 并入 `design.md`「方案细则（可选）」；
   - `ref-contract.md`（24 行，维护者规范、非运行时必读）→ 并入 `contract.md` 附录「Reference 统一契约」，并从 `SKILL.md` 运行时主循环中移除读取指针。
2. **消除多点复读（SSOT 收口）**：
   - 停点与重大方案人话对齐细则以 `confirm-protocol.md` 与 `approve.md` 为唯一真源，`SKILL.md`、`router.md`、`plan.md`、`design.md`、`decompose.md` 收敛为短指针与本环节特有动作；
   - 精简 `SKILL.md`、`intent.md`、`user-report.md`、`contract.md` 中重复展开的元规则表述，在保留全部有效规则与门禁的前提下显著压低冷启动加载体积。
3. **测试重心解耦**：
   - 将 `test_confirm_contract.py` 中要求同一长句在 5 个文件逐字复读的断言改为「测 SSOT 真源规则 + 其余文件指针存在」；
   - 更新 `test_taskrail_contract.py`、`test_explore_contract.py`、`test_flow_closure_contract.py`、`test_explore_behavior.py`、`test_design_and_handoff_gate.py`、`test_neighbor_skill_contract.py` 指向合并后的宿主文件并守卫已合并碎片不再回流。

非目标：不改变任何脚本行为、不削弱 P0–P2 任何门禁或工程纪律、不改动 `taskflow`、不改写历史 `patches/`。

## Conflict check

- 全仓 grep 确认无其他 skill 引用这 5 个文件（`wiki-data` 的 `archive-reopen.md` 为独立文件，互不影响），无需修改 `archive/README.md`。
- 仓级配套改动（非本 patch 范围）：同步 `AGENTS.md` 中对 `ref-contract.md` 的一处提及为 `contract.md` 附录。
- 保持 `SKILL.md <= 8192 B`、`confirm-protocol.md < 4000 B`、一层直链与正向表述约束。

## Rationale

`taskrail/references/` 此前多达 26 个文件，其中 5 个不足 30 行且运行时多与宿主文件成对出现；同一重大方案停点规则在 7 处文档反复复述并被测试逐文件锁死，既浪费上下文窗口又推高维护漂移风险。合并碎片并收口为 SSOT + 指针后，冷启动必读集显著变轻且规则单点可维护。

## Files

- `skills/taskrail/SKILL.md`：移除对 `ref-contract.md`/`archive-reopen.md`/`external-precedent.md` 的碎片链接并精简重复表述。
- `skills/taskrail/references/contract.md`：精简重复说明并收入「11. Reference 统一契约（维护规范，非运行时必读）」。
- `skills/taskrail/references/ledger.md`：合入「并发写入」节，重开指针指向 `close.md`。
- `skills/taskrail/references/explore.md`：合入「外部参照（按需）」节。
- `skills/taskrail/references/close.md`：合入「归档与重开」节。
- `skills/taskrail/references/design.md`：合入「方案细则（可选）」节并按 SSOT 收短第 6 步为指针。
- `skills/taskrail/references/router.md`、`plan.md`、`decompose.md`、`intent.md`、`user-report.md`：按 SSOT 精简跨文件复读，保留全部核心规则与指针。
- 删除已合并的 5 个碎片文件：`references/ledger-concurrency.md`、`references/external-precedent.md`、`references/archive-reopen.md`、`references/design-detail.md`、`references/ref-contract.md`。
- 更新 `skills/taskrail/tests/` 中 7 个契约测试文件以对接合并宿主并改为 SSOT + 指针断言。

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-005000-p3-slim-ssot-and-test-decouple/change.patch`
- `git diff --check -- skills/taskrail`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`、`skills/taskflow/tests` 与 `tests`
- `make check-names` 与 `make check-style`（0 报错 0 告警）
