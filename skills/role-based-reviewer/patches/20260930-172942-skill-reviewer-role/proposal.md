# diag 角色更正为 skill（Agent Skill 诊断）角色

- target: skills/role-based-reviewer
- mode: update
- patch: 20260930-172942-skill-reviewer-role
- risk: medium
- status: proposed

## Intent

更正 20260930-172217-diag-role 的理解偏差：用户要的是「诊断 Agent Skill 本身」的评审角色，不是故障排障角色。本 patch 移除 diag（诊断/排障），新增 skill（Skill 诊断）：审查对象是 Agent Skill 的 `SKILL.md` / `references/` / `tests/`——description 触发面（过宽误触/过窄漏触/缺「何时不用」）、指令可检查性、术语与协议一致性、references 按需加载与文件预算、正文承诺与契约测试断言的对应、职责越界、公开仓纪律、自进化纪律。

非目标：不改三道门禁、不改既有 9 个角色职责、不改默认角色（仍 engineer）；历史 patch 目录 20260930-172217-diag-role 保留不改。

## Conflict check

- 与 engineer 的边界：SKILL.md/references 的触发、协议与契约质量 → skill；`scripts/` 代码缺陷 → engineer（redirect 已写）。
- 与 qa 的边界：正文承诺与 tests/ 断言的对应缺口 → skill；通用可测性与回归策略 → qa。
- 与 product 的边界：skill 该不该存在/合并拆分 → product；已存在 skill 的质量诊断 → skill。
- 与门 2 不冲突：skill 不在默认角色内，推断信号要求问题主体就是 Agent Skill 质量。
- 与 skill-creator / skill-upgrader / skill-evolver 不冲突：本角色只诊断与提建议（只读），改 skill 仍走这三个执行类 skill（下游建议）。

## Rationale

本仓是 Agent Skills 集合，「审查一个 skill 写得对不对」是高频诉求且技能组合独立（触发面样例、契约测试对应、预加载预算），与既有角色无重叠；仓内已有 skill-creator / skill-upgrader / skill-evolver 作为天然下游。

## Files

- `SKILL.md`：description、输入合法值、推断信号三处 diag → skill
- `references/role-vocabulary.md`：角色矩阵 diag 行 → skill 行
- `references/roles/diag.md`：删除；`references/roles/skill.md`：新增（优先锚点 / 诊断方法 / 8 条带命中判据清单 / 不算问题 / 下游建议 / redirect）
- `references/constraints.md`：命令边界表 diag 列 → skill 列（运行态=否）；redirect 表两行替换为 skill ↔ engineer、skill ↔ qa
- `references/brief-protocol.md`：角色枚举 diag → skill；运行态字段还原（skill 不需运行态）
- `references/preload-protocol.md`：运行态启用角色还原
- `tests/test_role_based_reviewer_contract.py`：枚举与 THICKENED_FULL 中 diag → skill（第三批加厚）

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`python3 -m pytest skills/role-based-reviewer/tests -q` 全绿；全仓 `python3 -m pytest skills -q`
- 公开性：无个人/凭据/内部 URL；下游 skill 名均为公开仓内既有 skill
