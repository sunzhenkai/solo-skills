# 补齐向 session-wrap 弯路复盘的收口衔接

- target: skills/trouble-grill
- mode: update
- patch: 20261123-201400-connect-session-wrap-detour
- risk: low
- status: proposed

## Intent

在「落盘」节补一句衔接：排查存在 dead-end 或方向纠正时，会话收尾可交 `session-wrap` 基于排查记录做弯路复盘。

## Conflict check

none（session-wrap/references/detour-review.md 已消费本记录，本 patch 补齐反向指针）。

## Rationale

打通「排查落盘 → 弯路复盘 → 坑候选入 wiki」闭环。

## Files

- `skills/trouble-grill/SKILL.md`：落盘节补充 session-wrap 弯路复盘衔接
- `skills/trouble-grill/tests/test_trouble_grill_contract.py`：新增 session-wrap 弯路复盘衔接断言

## Validation

- `git apply --check --recount skills/trouble-grill/patches/20261123-201400-connect-session-wrap-detour/change.patch`
- `python3 -m unittest discover -s skills/trouble-grill/tests -p 'test_*.py'`
- `make check-style && make check-names`
