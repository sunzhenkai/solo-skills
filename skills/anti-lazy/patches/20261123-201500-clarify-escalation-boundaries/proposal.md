# 明确 anti-lazy 到 taskrail 与 session-wrap 的升格出口

- target: skills/anti-lazy
- mode: update
- patch: 20261123-201500-clarify-escalation-boundaries
- risk: low
- status: proposed

## Intent

明确定位为轻量通用元检查，补充跨会话台账升级到 `taskrail`、会话收尾核对交给 `session-wrap` 的边界指针。

## Conflict check

none

## Rationale

消除与 taskrail 意图/验证、session-wrap 目标对照的重叠感，使定位清晰。

## Files

- `skills/anti-lazy/SKILL.md`：补充 taskrail 与 session-wrap 升格出口
- `skills/anti-lazy/tests/test_anti_lazy_contract.py`：新增相邻 skill 升格边界断言

## Validation

- `git apply --check --recount skills/anti-lazy/patches/20261123-201500-clarify-escalation-boundaries/change.patch`
- `python3 -m unittest discover -s skills/anti-lazy/tests -p 'test_*.py'`
- `make check-style && make check-names`
