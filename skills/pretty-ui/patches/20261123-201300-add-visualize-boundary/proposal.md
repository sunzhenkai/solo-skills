# 补齐与 visualize 的图解双向边界

- target: skills/pretty-ui
- mode: update
- patch: 20261123-201300-add-visualize-boundary
- risk: low
- status: proposed

## Intent

在 pretty-ui 路由段明确以图为主的讲解页或独立架构/流程/时序图优先交 `visualize`，本 skill 承接以文字为主的阅读页及降级图解。

## Conflict check

none（保持独立入口，不反向引用 ui-kit）。

## Rationale

visualize 已声明与 pretty-ui 的边界，但反向指针缺失易导致图解请求误落 pretty-ui 手画。

## Files

- `skills/pretty-ui/SKILL.md`：路由节补齐与 visualize 的边界一句
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`：新增 visualize 边界守卫断言

## Validation

- `git apply --check --recount skills/pretty-ui/patches/20261123-201300-add-visualize-boundary/change.patch`
- `python3 -m unittest discover -s skills/pretty-ui/tests -p 'test_*.py'`
- `make check-style && make check-names`
