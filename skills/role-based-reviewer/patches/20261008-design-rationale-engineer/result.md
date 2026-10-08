# Result：engineer 角色新增「结构选择的依据」检查

改动已落工作树（`change.patch` 由 `git diff` 生成，`git apply --check --reverse` 与工作树一致）。

## 应用后的正文变化

- `references/roles/engineer.md` 核心检查清单在 🟡 组内、第 7 条「与现有约定一致」之后插入第 8 条：

  > 8. 🟡 [代码][方案] 结构选择的依据：改动引入或更换架构 / 接口 / 技术栈时，依据（模式或原则）与换来的可检后果能否说出。
  >    命中判据：指出该选择对应的具体变化点或重复点；指不出则报，指出但模式与其不匹配（贴名而无收益）也报。方案评审按方案稿判定，纯 diff 只看已落地的结构。

  原第 8 / 9 / 10 条顺延为 9 / 10 / 11，措辞逐字未改。
- `## 不算问题` 追加第 5 条反例：「**模式命名**：名字本身（工厂 / 策略 / 观察者）既不是问题也不是依据；按它是否消掉具体变化点或重复点判断，没有可检收益时并入复杂度条目，不为命名单独报。」
- `tests/test_role_based_reviewer_contract.py`：`TestRoleFilesStructure` 新增 `test_engineer_checks_structure_rationale`（3 条断言）。

## 测试

- `python3 -m pytest skills -q` → **430 passed, 1 skipped**（改动前 428 passed, 1 skipped）。
- `python3 -m pytest skills/role-based-reviewer skills/task-explore -q` → 56 passed。
- 新增断言在改动前的正文下会失败（`结构选择的依据` 不存在于 HEAD 的 `engineer.md`），确认不是恒真断言。
- `test_thickened_roles_keep_level_marks` 仍通过：文件同时含 🔴 与 🟡。

## 未验证 / 待观察

- 方案评审（task-explore 的 `plan-review`）里，engineer 角色是否会稳定按「指不出变化点则报」出手、而不是滑向模式命名的口味之争，需一次带设计稿的真实评审检验。本仓 `evals/` 是声明式案例、无自动 runner，本轮未新增 case。
- 新条的 `[代码][方案]` 双标记是首次出现；文件头只对 `[运行态]` 定义了降级规则，新标记不触发降级，行为按字面（两种输入都可判）。若后续出现更多双标记条目，可考虑在文件头统一说明标记语义。

## 未执行

未 sync 到各 agent 安装目录，未 commit / push。上游设计侧改动在 `skills/task-explore/patches/20261008-design-rationale/`。
