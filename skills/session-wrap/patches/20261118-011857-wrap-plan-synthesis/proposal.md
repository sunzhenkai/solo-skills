# 收尾输出改为单一方案

- target: skills/session-wrap
- mode: update
- patch: 20261118-011857-wrap-plan-synthesis
- risk: medium
- status: proposed

## Intent

收尾输出从四段发现清单加「待你确认」问题库，改为「结论 + 一个有序收尾方案 + 额外缺口 + 需单独授权」。低风险、结论唯一的收尾项默认完成；方案步骤一次确认后按序执行；额外缺口未点名时写入台账未决问题；push、合入、部署等外部或不可逆动作仍逐项授权。

## Conflict check

none。`anti-lazy` 仍负责交付前意图检查，taskrail `close` 仍负责 SUMMARY 与归档；本变更只调整 session-wrap 的合成、确认分档与输出结构。

## Rationale

原输出把决策成本转嫁给用户：多条发现各自成段，再附一组待确认问题。按三档归属后，用户只需对方案回答一次，风险动作保持独立授权；细则下沉 references 后正文仍在 8KB 内。

## Files

- skills/session-wrap/SKILL.md：新增「汇总成一个方案」，重写确认与授权、输出模板，缺口兜底写入台账。
- skills/session-wrap/references/plan-synthesis.md：新增三档判据、排序、缺口记账、确认语义与反例。
- skills/session-wrap/tests/test_session_wrap_contract.py：更新输出与授权断言，新增方案合成、默认收尾、台账兜底测试。
- skills/session-wrap/evals/cases.yaml：改写外部动作案例，新增单方案合成、低风险默认完成、缺口记账、方案确认不含风险动作。

## Validation

- 目标测试：`python3 -m pytest skills/session-wrap/tests tests/test_evals_structure.py -q`
- 全量：`python3 -m pytest skills -q`
- 仓库检查：`make check-style`、`make check-names`、`git diff --check`
