# Proposal：engineer 角色新增「结构选择的依据」检查（role-based-reviewer 侧）

- target: skills/role-based-reviewer
- mode: update
- patch: 20261008-design-rationale-engineer
- risk: low
- status: applied

## Intent

`task-explore` 的 `design` 阶段本轮新增「设计依据」门禁与模板小节（见该 skill `patches/20261008-design-rationale/`），但评审侧没有承接点：design 稿里写了模式与可检后果，没有任何角色会去核它对不对。

本 skill 的 `engineer` 清单里，第 7 条「与现有约定一致」只管对齐现状，第 9 条「复杂度」只管过度工程，都没有「这个结构选择凭什么成立」的位置。方案评审（`task-explore` 的 `plan-review` 阶段）会因此漏掉一整类问题：模式名与变化点不匹配（贴名而无收益）。

要改变的行为：

1. `references/roles/engineer.md` 核心检查清单在 🟡 组内、第 7 条之后插入第 8 条 `🟡 [代码][方案] 结构选择的依据`，判据是「指出该选择对应的具体变化点或重复点；指不出则报，指出但模式与其不匹配（贴名而无收益）也报」，并标出方案评审按方案稿判定、纯 diff 只看已落地的结构。原 8 / 9 / 10 顺延为 9 / 10 / 11。
2. `## 不算问题` 追加一条反例「模式命名」：名字本身既不是问题也不是依据，按是否消掉具体变化点或重复点判断，无可检收益时并入复杂度条目，不为命名单独报。

非目标：不改三道门禁、`审阅边界输入`、`role-vocabulary.md` 的角色矩阵与共享对象归属；不改其余角色文件；不改 SKILL.md。

## Conflict check

- 门 3（默认只报 Blocker / Major）不动：新条定为 🟡 Major，落在默认上报区间，与既有 🟡 组同档。
- 与第 9 条「复杂度」（过度工程）方向相反、不重叠：那条防「说不出用处仍建抽象」，新条防「建了抽象但说不出对应的变化点」；两者判据不同（有无第二个使用者 vs 有无具体变化点或重复点）。
- 与第 7 条「与现有约定一致」不重叠：那条判「偏离先例」，新条判「依据能否成立」，仓库无先例时第 7 条不报而新条仍可报。
- 新增「不算问题」条目与新条互补：新条要求指出变化点，该反例挡住「只凭模式名报问题」的误报路径，与既有「推测性 future-proof」条同一纪律风格。
- 级别标记保持：新增条目用 🟡，文件仍同时含 🔴 与 🟡，`test_thickened_roles_keep_level_marks` 不受影响。
- 新条含 `[方案]` 标记，与既有 `[代码]` / `[运行态]` 标记形式一致；文件头对 `[运行态]` 的降级说明不动，新标记不触发降级规则。

## Rationale

上游设计侧新开门禁后，评审必须同批承接，否则「写了依据但没人核」，与 `20260930-173857-ceiling-refset-boundary` 里「定义了没人审」是同一失效模式（本轮方向相反：那轮是评审承接上游定义，本轮是评审承接上游门禁）。

判据落在「具体变化点或重复点」而不是「有没有写模式名」，因为后者是文字游戏、前者是可核事实：写得再漂亮，指不出变化点就是不成立；写得朴素但能对上变化点就成立。这同时避免了把评审推向「模式命名偏好」的误报区，故配套加「不算问题」反例。

改动局部、可逆、无脚本，风险低。

## Files

- `references/roles/engineer.md` — 检查清单插入第 8 条并顺延编号；`## 不算问题` 追加「模式命名」
- `tests/test_role_based_reviewer_contract.py` — `TestRoleFilesStructure` 新增 `test_engineer_checks_structure_rationale`

## 与上游的关系

上游 `task-explore` 侧改动（`phase-design.md` 门禁 + 「设计依据」小节 + `design-template.md` 字段 + `plan-review` 委派要求）见 `skills/task-explore/patches/20261008-design-rationale/`。两侧同批，本 patch 只做评审承接。

## Validation

- 应用前（仓库根）：`git apply --check --recount skills/role-based-reviewer/patches/20261008-design-rationale-engineer/change.patch`
- 应用后：`git diff --check`；`python3 -m pytest skills/role-based-reviewer -q`；`python3 -m pytest skills -q` → **430 passed, 1 skipped**
- 本 patch 不 sync、不 commit、不 push。
