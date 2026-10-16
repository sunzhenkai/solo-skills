# 结果

- status: applied（未 commit）
- SKILL.md：3210 B → 3243 B
- description：190 → 150 字符
- disable-model-invocation：False
- 验证：`python3 -m pytest -q`、`make check-names`、`make check-style` 通过（check-style 0 告警）。
