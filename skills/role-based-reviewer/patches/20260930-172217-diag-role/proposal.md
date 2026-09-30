# 新增 diag（诊断/排障）角色

- target: skills/role-based-reviewer
- mode: update
- patch: 20260930-172217-diag-role
- risk: medium
- status: proposed

## Intent

为 role-based-reviewer 新增第 10 个角色 `diag`（诊断/排障）：管「现象 → 根因」的假设-验证闭环、复现与取证（日志/监控/堆栈）、症状与根因区分、回归验证；不管已定根因的修复与实现质量（→ engineer）、部署/资源/集群侧根因的处置（→ sre）、离线口径与管道（→ data）。

非目标：不改三道门禁、不改既有 9 个角色职责、不改默认角色（仍 engineer）；diag 仅在显式 `roles=diag` 或「目标就是根因排查」的强信号下启用。

## Conflict check

- 与 engineer 的边界：engineer 审静态代码质量与缺陷；diag 管从现象到根因的定位过程与可诊断性。`diag ↔ engineer` redirect 明确「定位 → diag，已定根因的修复 → engineer」，避免双开。
- 与 sre 的边界：故障根因归属按侧分——应用内逻辑/数据 → diag，部署/资源/依赖/集群 → sre；与既有 `sre ↔ engineer`（重启/OOM/稳定性）判据一致。
- 与门 2 不冲突：diag 不在默认角色内，推断信号要求问题主体就是根因排查。
- 不引入自进化结构，非 self-upgrade。

## Rationale

排障是一类独立问题（假设-验证循环），与静态评审的技能组合不同；仓内已有 `diagnosing-bugs`（诊断循环）与 `trouble-grill`（根因拷问）作为天然下游，diag 角色把「按诊断视角看问题」接入角色化评审框架，复用门 2/门 3 与分级输出契约。

## Files

- `SKILL.md`：description、输入合法值、视角推断信号三处加 `diag`
- `references/role-vocabulary.md`：角色矩阵加 `diag` 行
- `references/roles/diag.md`：新增（优先锚点 / 诊断方法 / 6 条带命中判据清单 / 不算问题 / 下游建议 / redirect）
- `references/constraints.md`：命令边界表加 diag 列；redirect 表加 diag ↔ engineer、diag ↔ sre 两行
- `references/brief-protocol.md`：RoleBrief 角色枚举与运行态字段加 diag
- `references/preload-protocol.md`：运行态上下文启用角色加 diag
- `tests/test_role_based_reviewer_contract.py`：角色枚举与 THICKENED_FULL 加 diag（第三批加厚）

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills/role-based-reviewer/tests -q` 全绿
- 公开性：无个人/凭据/内部 URL；下游 skill 名均为公开仓内既有 skill
