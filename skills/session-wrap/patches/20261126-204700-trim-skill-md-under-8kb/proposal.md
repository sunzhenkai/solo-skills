# 精简 session-wrap SKILL.md 体积至 8KB 以内

- target: skills/session-wrap
- mode: update
- patch: 20261126-204700-trim-skill-md-under-8kb
- risk: low
- status: proposed

## Intent

精简 `skills/session-wrap/SKILL.md` 冗余措辞，使文件体积控制在 8192 字节以内，消除 `make check-style` 体积告警，同时完整保留所有门禁、路由、授权隔离与四态放手结论。

## Conflict check

none（不改变任何契约测试断言或跨 skill 边界）。

## Rationale

`AGENTS.md` 与 `check_output_style.py` 建议单个 `SKILL.md` 不超过 8192 字节，细则已下沉至 `references/`。

## Files

- `skills/session-wrap/SKILL.md`（紧凑措辞，保留全部核心规则与契约锚点）

## Validation

- `git apply --check --recount skills/session-wrap/patches/20261126-204700-trim-skill-md-under-8kb/change.patch`
- `wc -c skills/session-wrap/SKILL.md`
- `python3 -m unittest discover -s skills/session-wrap/tests -p 'test_*.py' -v`
- `make check-style`
