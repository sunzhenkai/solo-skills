# 保真与产品页目检拆开

- target: skills/ui-kit
- mode: update
- patch: 20261119-193500-review-gate
- risk: medium
- status: proposed

## Intent

模板路线的完成条件分成两条，互不替代：保真只证明模板文件和 story 没被改；已经登记页面后，产品页目检（J10 / J11）必须通过。删掉「J10 可忽略」。

不改触发条件，不改通用路线，不把后端契约或数据迁移写进本 skill。

配套：`ui-templates-skill` 的 `skills/ui-template-apply/patches/20261119-193500-state-matrix`。那边把 J10 在已有 `pages` 时改为错误，并要求状态矩阵。本文件只改 ui-kit 怎么读这些结果。

## Conflict check

与 `references/language.md`「页面内容不在保真范围内」一致，并消掉 verify.md 与该句的矛盾。`tests/test_ui_kit_contract.py` 仍要求完成句包含 `validate 0 error` 与 `fidelity: pass`，本轮保留该前缀并补上产品页条件。不改 pretty-ui。

## Rationale

像素保真对照的是固定 fixture 的 story。空态、390 宽、同名行和自定义画布不会让保真失败。验收文档若允许忽略 J10，模型会把保真通过当成页面已验收。

## Files

- skills/ui-kit/references/verify.md：两条完成条件；J10 在已有页面清单时是错误
- skills/ui-kit/references/update.md：升级后重拍带 `upstream` 的路由
- skills/ui-kit/SKILL.md：完成句补上产品页审查
- skills/ui-kit/tests/test_ui_kit_contract.py：守卫「不可忽略 J10」

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`python3 skills/ui-kit/tests/test_ui_kit_contract.py`；确认 verify.md 不含「可忽略」
