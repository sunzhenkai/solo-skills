# 将 session-wrap SKILL.md 压至 8192 字节以内

- target: skills/session-wrap
- mode: update
- patch: 20261126-204800-trim-skill-md-8kb
- risk: low
- status: proposed

## Intent

将 `skills/session-wrap/SKILL.md` 从 8211 B 进一步精简至 8192 B 以内，使 `make check-style` 达到 0 告警。

## Conflict check

none

## Rationale

满足 `AGENTS.md` 与 `check_output_style.py` 的 8192 B 阈值要求。

## Files

- `skills/session-wrap/SKILL.md`

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261126-204800-trim-skill-md-8kb/change.patch`
- `wc -c skills/session-wrap/SKILL.md`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-style && make check-names`
