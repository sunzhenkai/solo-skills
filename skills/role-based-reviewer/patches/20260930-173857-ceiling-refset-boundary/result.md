# Result：天花板参照集接入 design 审阅边界

`git apply --recount` 应用成功（与 task-goal / task-delivery 侧连续应用）。

## 应用后的正文变化

- `SKILL.md` 门 1 第 4 条：「这类流程固定 3 个角色属预期，不算角色膨胀」→「角色集由调用方按任务适用面给定，数量随任务变，不算角色膨胀」。**注意**：这一句不在本 patch 的原始目的内，是收口 `20260930-171920-roles-on-demand` 的残留——该 patch 把调用侧的角色集改成按任务涉及面推断后，此处仍以「上游固定三角色」为前提书写，两处口径相反。改动已在本目录 `proposal.md` 与本 skill 说明中标出。
- `SKILL.md` `审阅边界输入` 条目：补「质量目标含审美 / 体验等无法用确定性度量完备验收的项时，角色底线里还须带天花板参照集（把『卓越』落成可数构成件或外部参照）」；缺项行为不变。
- `references/roles/design.md`：`## 不算问题` 之前新增 `## 天花板参照集（仅当审阅边界给了参照集）`，三条规则（须指到具体件并写清差在哪 / 未覆盖的报 Suggestion 并注明 / 缺失或不一致时写明缺块，不自行拟定也不放行地板判定），并声明不受「像素与间距口味」「设计趋势追逐」两条免报保护。
- `tests/test_role_based_reviewer_contract.py`：新增 `test_design_has_ceiling_reference_section`。

## 测试

- `git apply --check --recount`：通过
- `python3 -m pytest skills/role-based-reviewer/tests -q`：通过（含新增 1 条）
- `python3 -m pytest skills -q`：428 passed, 1 skipped

## 未验证 / 待观察

- `design` 角色在真实评审中能否稳定落到「参照集里的哪一件、差在哪」而非滑回「不够精致」，需一次带参照集的真实观感类评审检验。
- 若上游未传参照集而任务确属观感类，本 skill 的行为是「报告写明缺块 + 按调用方规则处理」——即不补审天花板；该缺块是否会在此后落回上游补画像，取决于上游实现，本侧不保证。

## 未执行

未 sync 到各 agent 安装目录，未 commit / push。
