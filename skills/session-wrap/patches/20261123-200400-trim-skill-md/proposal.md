# 压缩 SKILL.md 重复表述，留出 8KB 演进裕度

- target: skills/session-wrap
- mode: update
- patch: 20261123-200400-trim-skill-md
- risk: low
- status: proposed

## Intent

在不改变任何门禁、规则与两轮输出契约的前提下，压缩第 3、4 节和「确认与授权」的冗长表述，解除贴近 8192B 上限的压力。

## Conflict check

none

## Rationale

原 SKILL.md 为 8033B，接近 8KB 告警线；精简后所有契约断言完整保留且体量更具安全裕度。

## Files

- `skills/session-wrap/SKILL.md`：紧凑合并第 3、4 节与「确认与授权」段落

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261123-200400-trim-skill-md/change.patch`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py'`
- `make check-style && make check-names`
