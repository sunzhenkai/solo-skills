# Result：评审角色改为按任务涉及面推断

`git apply --recount` 应用成功。

## 应用后的正文变化

- `task-delivery/references/loop-protocol.md` Stage 7：调用示例 `role-based-reviewer mode=review roles=product,design,engineer` → `roles=<按任务适用面推断>`，并新增推断规则段（基线取质量画像 `角色底线` 中可检查的几条，写「不适用」的不取；触及部署 / 模型 / 数据 / 运营配置 / 对外对接再补对应角色；依据与角色集写进 manifest 的 `role_review`）；「product / design / engineer 独立 findings」→「各生效角色的独立 findings」。
- `task-delivery/SKILL.md`：主循环第 9 步同步为推断制（标题「三角色评审」→「角色化评审」）；description 与「goal 模式的归属」中的「三角色评审」→「角色化评审」。
- `task-goal/SKILL.md`：审阅人选表 role-based-reviewer 行的派遣口径改为 `roles=<按任务适用面推断>`；「简单和中等不强制三角色」→「角色集不预置，按任务适用面推断；简单和中等不强制角色化评审」。
- 两处 `evals/cases.yaml` 期望同步。
- `task-delivery/tests/test_task_delivery_contract.py` 新增 `TestRoleReviewOnDemand`（3 条断言，含反例断言：正文与 loop-protocol 不得再出现 `roles=product,design,engineer`）。

## 测试

`python3 -m pytest skills -q`：426 passed, 1 skipped（基线 424 passed, 1 skipped，新增 2 个用例随本 patch 生效）。

`git apply --check --recount` 通过；`git diff --check` 无空白问题；族级链接测试（`test_task_family_contract.py`）仍全过。

## 未验证 / 待观察

- 推断规则的实际效果未在真实任务上跑过：基线取画像 `角色底线` 是否足以覆盖「评审该看哪些面」，需一次真实复杂档交付验证；若发现漏派，纠偏入口是 manifest 的 `role_review` 记录与 role-based-reviewer 的角色表。
- 未改 `role-based-reviewer` 的门 2：本方给的是「已指定」的 `roles`，不会触发「超过 2 个角色先问」；若某任务推断出 4 个以上角色，行为是照单执行而非反问——是否符合预期未验证。

## 遗留（本 patch 范围外）

- acceptance-rubric 无「某维度不适用时如何记分」的口径，无界面交付的 UI/UX 维度仍无明确处置。
- `taskflow` 侧的评分主体措辞（「按 product / design / engineer 分工」）未动。
- `role-based-reviewer` 门 1 第 4 条仍写「这类流程固定 3 个角色属预期，不算角色膨胀」——该句以上游固定三角色为前提，本轮改动后已不成立（传入的是推断集），属跟进项。

## 未执行

未 sync 到各 agent 安装目录，未 commit / push。
