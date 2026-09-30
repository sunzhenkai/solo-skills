# Result：审美 / 体验类目标的天花板参照集落进画像

三处 `change.patch` 已按序 `git apply --recount` 应用（task-goal → task-delivery → role-based-reviewer）。

## 应用后的正文变化

- `task-goal/references/quality-profile.md`
  - 字段模板 `design` 行追加「质量目标含审美 / 体验等无法用确定性度量完备验收的项时，另写天花板参照集」
  - 字段规则新增一条：参照集 = 可数构成件或外部参照（各指到具体件、写清取哪一点）；实测指标只声明「不低于」，替代不了参照集；写不出先走退出点「理解不够」，不以「无缺陷」默认收工
  - 新增 `## 天花板参照集的去向`：随画像快照进审阅边界 → design 角色据它出意见；不引入新审阅对象；参照集缺失或与完成判据冲突按缺字段（P0）处理，不改判据
- `task-goal/SKILL.md`：审阅边界的画像检查项并列「（含审美 / 体验类目标的天花板参照集）」
- `task-delivery/SKILL.md`：第 1 条「天花板前置」由「MUST 先定」改为指向画像 design 底线，写明参照集随快照进 Stage 7 审阅边界、本循环不另立评审主体
- `task-delivery/references/loop-protocol.md`：Stage 7「观感类目标」段补参照集来源；design 未生效或模板未给参照集时不补审天花板，按缺字段报
- `role-based-reviewer/SKILL.md`：`审阅边界输入` 条目补「含审美项时角色底线还须带天花板参照集」；门 1 第 4 条「这类流程固定 3 个角色属预期」→「角色集由调用方按任务适用面给定，数量随任务变」（见下「跨 patch 收口」）
- `role-based-reviewer/references/roles/design.md`：新增 `## 天花板参照集（仅当审阅边界给了参照集）`——三条规则：每条意见 MUST 指到参照集具体件并写清差在哪；未覆盖的报 Suggestion 并注明；参照集缺失或不一致时报告写明缺块，不自行拟定、也不放行地板判定
- 三个 skill 各增测试 / eval：`task-goal/tests`（参照集字段 + 去向节）、`task-goal/evals`（`aesthetics-ceiling-reference-set`）、`task-delivery/evals`（`aesthetics-ceiling-comes-from-profile`）、`role-based-reviewer/tests`（design 新节存在）

## 测试

- 三份 `git apply --check --recount` 各自通过；连续应用干净
- `python3 -m pytest skills -q`：428 passed, 1 skipped（基线 426 + 新增 2 条断言用例）
- 链接检查（`test_task_family_contract.py` 的族内相对链接）通过：`task-delivery → task-goal/references/quality-profile.md#天花板参照集的去向` 可达

## 跨 patch 收口

`role-based-reviewer` 门 1 那句「这类流程固定 3 个角色属预期」是本地固定 `roles=product,design,engineer` 的产物，`20260930-171920-roles-on-demand` 改掉了调用侧却漏改了它，该 patch 的 `result.md` 已把它列为遗留项；本 patch 一并改净，故 `role-based-reviewer` 侧改动超出「参照集」单一目的——已在此显式记录，避免两个 patch 相互推诿。

## 未验证 / 待观察

- 参照集在真实任务上的质量未验证：写「可数构成件」到什么粒度算够、`design` 角色能否稳定地把意见落到具体件而非滑回「不够精致」，需一次真实观感类交付检验。
- 适配噪声边界未验证：纯后端任务若误写了观感评估面，会不会引发无谓的参照集缺失 P0。画像规则允许 design 底线写「不适用」，理论上不触发；实际是否被正确判为「不适用」待观察——这是把「何时适用」留给设计判断的必然代价，本 patch 未引入用途探测。

## 未执行

未 sync 到各 agent 安装目录，未 commit / push。
