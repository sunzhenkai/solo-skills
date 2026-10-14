# 内置子参考改名 REFERENCE.md

- target: skills/pretty-view-html
- mode: update
- patch: 20261015-015500-reference-md-rename
- risk: low
- status: applied

## Intent

`references/{frontend-design,html-diagram}/SKILL.md` 带完整 frontmatter，递归扫描的加载器会把它们注册成独立 Skill。改名为 `REFERENCE.md`（git mv），正文不变，只更新链接。

## Conflict check

none

## Files

- `skills/pretty-view-html/SKILL.md`：引用路径。
- `skills/pretty-view-html/references/html-diagram/REFERENCE.md`：指向 frontend-design 的相对链接。
