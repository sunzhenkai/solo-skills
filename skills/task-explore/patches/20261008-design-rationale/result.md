# Result：design 的架构 / 接口 / 技术栈选择须有设计依据（task-explore 侧）

改动已落工作树（`change.patch` 由 `git diff` 生成，`git apply --check --reverse` 与工作树一致）。

## 应用后的正文变化

- `references/phase-design.md`
  - 门禁追加第 5 条：「架构 / 接口 / 技术栈的选择都写得出依据（设计模式或软件工程原则）；写不出就列入未决，不算设计完成。本任务不涉及这三类选择时写「不适用」并说明，不为凑数贴模式名」。
  - 「画像展开」与「三阶段」之间新增 `## 设计依据（架构 / 接口 / 技术栈）`：一行一条 `选择 → 模式 / 原则 → 为何适用 → 可检后果`；可检后果只能写成少了什么（耦合面 / 接口面 / 重复 / 可替换点 / 可测性 / 回归面）；模式要落到具体变化点或重复点；拿不出可检后果写「不引入」；既有成熟做法优先对齐并链到「现状」节；写不出依据入未决。末句写明与「外部参照」的分工（出处 vs 凭什么成立，互不替代）。
  - 三阶段第 2 步补「推荐方案的架构 / 接口 / 技术栈选择按「设计依据」逐条给出」。
- `references/design-template.md`：`## Recommended Approach` 与 `## Architecture` 之间新增 `## 设计依据`（含三条骨架行：常规选择、不引入模式的选择、「不适用」分支）。
- `references/phase-plan-review.md`：步骤 4 委派要求补「评审要求须含**设计依据核对**」一句，指明按 `phase-design.md` 逐条核模式与变化点是否匹配、可检后果是否兑现、有无写不出依据却当成已设计的选择。
- `tests/test_task_explore_contract.py`：`setUpClass` 增读 `phase-plan-review.md` 与 `design-template.md`；新增 `test_design_requires_rationale_for_structure_choices`（8 条断言）。

## 测试

- `python3 -m pytest skills -q` → **430 passed, 1 skipped**（改动前 428 passed, 1 skipped）。
- 新增断言在改动前的正文下会失败（`## 设计依据` 不存在），确认它不是恒真断言。
- `TestFamilyLinksResolve` 通过：新增的 `[external-precedent.md](external-precedent.md)` 与 `[phase-design.md](phase-design.md)` 均为同目录相对链接，可达。

## 未验证 / 待观察

- 真实 design 回合里，「设计依据」小节能否稳定逼出「少什么」而不是滑回「更优雅 / 更规范」，需一次真实方案设计检验。本仓无自动 runner（`evals/` 是声明式案例），本轮未新增 case。
- 门禁新增条目后，纯探索型任务（不涉及架构 / 接口 / 技术栈选择）会走「不适用」分支；该分支是否被稳定识别（而非被沉默跳过）同样只能在真实回合里观察。

## 未执行

未 sync 到各 agent 安装目录，未 commit / push。评审侧对应改动在 `skills/role-based-reviewer/patches/20261008-design-rationale-engineer/`。
