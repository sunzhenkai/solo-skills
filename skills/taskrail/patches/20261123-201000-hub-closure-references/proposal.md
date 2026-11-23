# 补齐 taskrail 枢纽按需出链与 review.md

- target: skills/taskrail
- mode: update
- patch: 20261123-201000-hub-closure-references
- risk: medium
- status: proposed

## Intent

新增 `references/review.md` 统一分流 `role-based-reviewer` 与 `solo-code-review`，并在 `confirm-protocol.md`、`design.md`、`close.md` 下沉对 `agent-roster`、`project-design-patterns`、`session-wrap` 的可选软指针，保持 `SKILL.md` 体量克制且不增加硬依赖。

## Conflict check

配套 patch：role-based-reviewer、solo-code-review、trouble-grill、anti-lazy 同步补齐双向边界。

## Rationale

taskrail 作为仓库唯一编排入口，原文本中对 5 个核心下游 skill 均为 0 命中，造成枢纽失联；将软指针下沉到按需 reference 兼顾零日常 token 增量与闭环连通。

## Files

- `skills/taskrail/references/review.md`：新增符合 ref-contract 的独立评审路由细则
- `skills/taskrail/SKILL.md`：在路由型 references 表与正文直链 review.md
- `skills/taskrail/references/confirm-protocol.md`：异源模型审补充 agent-roster 可选委派指针
- `skills/taskrail/references/design.md`：补充 project-design-patterns 可选查卡指针
- `skills/taskrail/references/close.md`：补充 project-design-patterns 沉淀与 session-wrap 会话收尾衔接
- `skills/taskrail/tests/test_taskrail_contract.py`：新增 review.md 与枢纽软出链契约断言

## Validation

- `git apply --check --recount skills/taskrail/patches/20261123-201000-hub-closure-references/change.patch`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py'`
- `make check-style && make check-names`
