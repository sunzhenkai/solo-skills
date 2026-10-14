# 结果

- 已应用 change.patch（`git apply -R --check` 通过）。
- 同轮仓库级配套（越出本 Skill 前缀）：各 Skill 历史 `evolutions/*/SKILL.md` 用 `git mv` 改名为 `SKILL.md.candidate`；`pretty-view-html/references/*/SKILL.md` 改名为 `REFERENCE.md` 并更新引用；新增 `tests/test_no_nested_skill_md.py` 禁止 Skill 根目录以外出现 `SKILL.md`。
- `references/self-upgrade.md`、`references/skill-injection.md` 只提 `evolutions/` 目录，不涉及候选文件名，无需改。
