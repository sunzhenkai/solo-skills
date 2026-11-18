# 立锚点后按现象查已有的坑

- target: skills/trouble-grill
- mode: update
- patch: 20261118-103520-symptom-pitfall-lookup
- risk: low
- status: proposed

## Intent

锚点立好后先用现象词（报错原文、组件名、现象描述）查已有的坑：有 `wiki-data` 时走其 query 的执行前预检，否则检索工作区既有的经验库。命中时把「最短判别」作为第一个验证动作，旧根因在本次验证前按 `guess` 上板，记过的误判方向要有本次新证据才重新上板；未命中说明已查过并继续。

非目标：不改假设板、四道门禁、收口与落盘规则。

## Conflict check

none。旧结论按 `guess` 上板，仍须过本 skill 的证据升级与门禁，不绕过「只有 confirmed 才叫根因」。配套 patch：`skills/wiki-data/patches/20261118-103520-pitfall-pattern-experience/`、`skills/session-wrap/patches/20261118-103520-detour-review/`。

## Rationale

坑只存不查等于白存；排查开始时是检索旧坑最便宜、收益最大的时机。

## Files

- skills/trouble-grill/SKILL.md：「先立锚点」加一段。
- skills/trouble-grill/tests/test_trouble_grill_contract.py：守卫断言。

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/trouble-grill/tests -q`
- 全量 `python3 -m pytest skills tests -q`；`make check-style`
