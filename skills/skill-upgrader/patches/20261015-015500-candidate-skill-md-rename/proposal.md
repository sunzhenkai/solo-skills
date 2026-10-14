# evolve 候选正文改名为 SKILL.md.candidate

- target: skills/skill-upgrader
- mode: update
- patch: 20261015-015500-candidate-skill-md-rename
- risk: low
- status: applied

## Intent

evolve 模式把候选正文存成 `evolutions/<slug>/SKILL.md`，与生产稿同名同 frontmatter。递归扫描 `SKILL.md` 的加载器会把每个快照都注册成同名 Skill，同一个 Skill 出现多次。改为与其他候选文件一致的 `.candidate` 后缀，晋升时写回 `SKILL.md`。

非目标：不改提案、评估、晋升门禁，不改目录协议的其余部分。

## Conflict check

none：第 6 条已规定其他候选文件加 `.candidate`，本次只取消 `SKILL.md` 的例外。

## Files

- `skills/skill-upgrader/references/evolve.md`：候选目录示例、规则 6、promote 行。
- `skills/skill-upgrader/tests/gate_lines.txt`：规则 6 锁定句同步。
- `skills/skill-upgrader/tests/test_skill_upgrader_contract.py`：新增候选正文命名断言。
