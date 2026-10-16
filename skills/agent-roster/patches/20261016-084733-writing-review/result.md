# 结果

- status: applied（未 commit）
- SKILL.md：8021 B → 7940 B
- description：320 → 133 字符
- disable-model-invocation：False
- 验证：`python3 -m pytest -q`、`make check-names`、`make check-style` 通过（check-style 0 告警）。
