# Proposal：design 的架构 / 接口 / 技术栈选择须有设计依据（task-explore 侧）

- target: skills/task-explore
- mode: update
- patch: 20261008-design-rationale
- risk: low
- status: applied

## Intent

`design` 阶段的门禁只要求「至少两个可行方案 + 对比表」，对比维度是成本 / 风险 / 可逆性 / 工期 / 复杂度——全是项目管理轴，没有一条工程轴。架构、接口、技术栈的选择凭什么成立，方案稿里没有落点：`design-template.md` 的 `## Architecture` / `## Interfaces` / `## Recommended Approach` 都没有「依据」字段，`phase-design.md` 的边界只要求「必须有图和权衡表」。既有的 [external-precedent.md](../../references/external-precedent.md) 管的是「别人怎么做的出处」，不是「本选择凭什么成立」，两者不同。

于是模型默认给出方案，却不系统性地说明每个结构选择的依据，也无从分辨「方案」与「贴模式名（cargo cult）」。

要改变的行为：

1. `phase-design.md` 门禁追加一条：架构 / 接口 / 技术栈的选择都写得出依据（设计模式或软件工程原则）；写不出列入未决，不算设计完成；本任务不涉及这三类选择时写「不适用」并说明。
2. `phase-design.md` 新增「设计依据（架构 / 接口 / 技术栈）」小节：一行一条 `选择 → 模式 / 原则 → 为何适用 → 可检后果`，并写明「模式名本身不是依据」、可检后果只能写成「少了什么」、既有成熟做法优先对齐、写不出依据入未决。同时写明与「外部参照」的分工。
3. `phase-design.md` 三阶段第 2 步补一句：推荐方案的架构 / 接口 / 技术栈选择按「设计依据」逐条给出。
4. `design-template.md` 在 `## Recommended Approach` 与 `## Architecture` 之间插入 `## 设计依据`。
5. `phase-plan-review.md` 步骤 4 的委派要求补一句「设计依据核对」，让被派方知道要核这一项。

非目标：不改阶段表、加载表与 `SKILL.md`；不改 `design` 的其余门禁与「画像展开」；不改 `decide` / `handoff` / `archive` / `reopen` / `split`；不引入外部依赖（不引 `codebase-design`，故不动 README 外部依赖表与 Makefile）。

## Conflict check

- `phase-design.md` 门禁原有四条（目标一句话 / 成功标准可检验 / 画像快照 / 约束已知 / 两个可行方案）逐字保留，新条追加在其后，不替换任何一条。
- `phase-design.md` 原有「## 三阶段」「## 边界」「## 对比表 / 推荐」「## 交接」各节不动；新小节插在「画像展开」与「三阶段」之间，不改变既有小节的编号与措辞。
- 与既有「外部参照」不重叠：新小节末句显式写清分工（出处 vs 凭什么成立），两者互不替代，同一选择可以两者都有。
- 新小节不引入「架构 / 接口 / schema / 代码骨架设计」的产出要求：它约束的是**已经做出的**结构选择要不要写依据，与 `task-goal` 质量画像「不审」列不冲突。
- 与 `design-template.md` 既有 `## Architecture` / `## Interfaces` 不重复：新节写「为何这样选」，那两节写「选成了什么样」。
- 本 skill 的契约测试 `test_task_explore_contract.py` 未断言 `design-template.md` / `phase-plan-review.md` 的既有字符串，新增断言不影响既有 42 条。
- 族级契约 `TestFamilyLinksResolve`（task-goal/tests）会核新增的 `[external-precedent.md](external-precedent.md)` 与 `[phase-design.md](phase-design.md)` 同目录链接可达——两者均在同目录，可达。

## Rationale

按 writing-for-agents：**依据**是本次的锚点词（leading word），一个紧凑名词，在门禁、模板小节、评审要求三处重复同一 token，锚定同一行为——每个结构选择要能说出它依据的模式或原则，以及换来的可检后果。把它落在**门禁**而非仅模板字段，是因为模板字段只是建议填写，而门禁让它成为「不算设计完成」的硬约束，堵住「写了模式名就算交差」的滑坡。

可检后果只允许写成「少了什么」（耦合面、接口面、重复、可替换点、可测性、回归面），因为这是「真依据」与「贴名」的可观测分界：说不出少了什么，就没有收益，就不该引入结构。这也是与既有 engineer 角色「过度工程同样算复杂度问题」同源的一条纪律，只是方向相反（那条防多建，这条防说不出为何建）。

改动全部落在既有 reference 的文本上，措辞通用、无项目专有内容，可随 skill 分发；每条都可机械核对。不触碰状态集合、目录规则与 driver 命名，不新增阶段，风险低。

## Files

- `references/phase-design.md` — 门禁追加一条；新增「设计依据（架构 / 接口 / 技术栈）」小节；三阶段第 2 步补一句
- `references/design-template.md` — `## Recommended Approach` 后新增 `## 设计依据`
- `references/phase-plan-review.md` — 步骤 4 委派要求补「设计依据核对」
- `tests/test_task_explore_contract.py` — `setUpClass` 增读 `phase-plan-review.md` 与 `design-template.md`；新增 `test_design_requires_rationale_for_structure_choices`

## 承接方

评审侧的对应改动在 `skills/role-based-reviewer`（engineer 角色新增「结构选择的依据」条目），见该 skill `patches/20261008-design-rationale-engineer/`。单改设计侧会留下「写了依据但没人核」的缺口，故两侧同批。

## Validation

- 应用前（仓库根）：`git apply --check --recount skills/task-explore/patches/20261008-design-rationale/change.patch`
- 应用后：`git diff --check`；`python3 -m pytest skills -q` → **430 passed, 1 skipped**（改动前 428 passed, 1 skipped，新增 2 条断言）
- 本 patch 不 sync、不 commit、不 push。
