# 移动端 375 检查改为分级组合（跳过 / 基础检查 / 完整验证）

- target: skills/pretty-ui
- mode: update
- patch: 20261126-155500-mobile-viewport-tiers
- risk: low
- status: applied

## Intent

1. 将 `pretty-ui` 的视口验证从“响应式或无法判断一律双视口完整三档”调整为**方案三（分级组合）**：默认以桌面 `1280` 为主视口，手机 `375` 按「明确要求必须 + 未明说自动推断」分为 **跳过（默认）/ 基础检查 / 完整验证（必须）** 三档。
2. 明确「基础检查」口径：仅在交付前复用当前浏览器会话切一次 `375`，跑 `evidence.md` 第 3 节 DOM 量测并截 1 张首屏快看；只修 P0 破损，不补整页与状态档、不入隔离评审的精致度/设计感打磨。
3. 明确「跳过（默认）」需在交付说明未验证项写明「移动端 375 未检查（按需开启）」。
4. 同步更新 `SKILL.md`、`references/evidence.md`、`references/rules.md`、`references/page.md`、`tests/test_pretty_ui_contract.py` 与 `evals/cases.yaml`。
