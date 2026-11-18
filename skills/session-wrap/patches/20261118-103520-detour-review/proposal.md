# 收尾时的弯路复盘

- target: skills/session-wrap
- mode: update
- patch: 20261118-103520-detour-review
- risk: medium
- status: proposed

## Intent

会话里有付出明显代价的排查（有死路、方向被纠正、根因出乎最初猜测或明显超时）时，收尾第 6 步按新增的 `references/detour-review.md` 做弯路复盘：优先取 `trouble-grill` 的排查记录，用五问（现象、误判、决定性证据、最短路径、可迁移规律）提炼按现象可检索的坑候选，放进收尾方案的知识落点步骤交 `wiki-data` 写入；排查方法本身的同类弯路再次出现时才建议走 `skill-upgrader`。没有排查代价的会话跳过。

非目标：不改变三档确认与授权；不让 session-wrap 自己写 wiki 或改 skill。

## Conflict check

none。写 wiki 仍是方案步骤，随收尾方案一次确认；「单次失败先留作经验」不变。配套 patch：`skills/wiki-data/patches/20261118-103520-pitfall-pattern-experience/`（坑页格式与摄入规则）、`skills/trouble-grill/patches/20261118-103520-symptom-pitfall-lookup/`。

## Rationale

原第 6 步只把「踩坑」路由到知识库，不回看排查绕了哪些路，沉淀下来的多是根因，缺少下次能缩短排查的误判与最短判别。细则放 references，正文只加一句指针，保持在 8KB 内。

## Files

- skills/session-wrap/SKILL.md：第 6 步加弯路复盘指针。
- skills/session-wrap/references/detour-review.md：触发信号、取材、五问、分流与坑候选格式。
- skills/session-wrap/tests/test_session_wrap_contract.py：守卫断言。
- skills/session-wrap/evals/cases.yaml：多轮排查产出坑候选；顺利会话跳过复盘。

## Validation

- `git apply --check --recount`
- `python3 -m pytest skills/session-wrap/tests tests/test_evals_structure.py -q`
- 全量 `python3 -m pytest skills tests -q`；`make check-style`、`make check-names`、`git diff --check`
