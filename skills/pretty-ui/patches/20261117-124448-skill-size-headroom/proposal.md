# 压缩 SKILL.md，恢复体量余量

- target: skills/pretty-ui
- mode: update
- patch: 20261117-124448-skill-size-headroom
- risk: high
- status: proposed

## Intent

在不改变触发、路由、设计流程、完成门禁、确认方式和交付契约的前提下压缩 `SKILL.md`，从贴近 8 KiB 上限恢复到可持续维护的余量。保留三条信条、轻量方向卡、十条铁律及数值阈值；不迁移 references，不修改测试。

## Conflict check

与现有 frontmatter、契约测试及其他 Skill 职责无冲突。工作区已有未提交的 pretty-ui 改动，本 patch 以当前生产稿为基线，只压缩 `SKILL.md`，不覆盖其他改动。

## Rationale

正文与 references 存在重复解释。缩短重复表述比迁移规则或放宽测试改动更小，并可沿用现有 58 个契约与脚本测试验证行为锚点。临时副本中的候选稿为 7315 字节，原有测试全部通过。

## Files

- `skills/pretty-ui/SKILL.md`：压缩路由、build 主流程、十条铁律、看图确认、交付与按需读取的重复表述。

## Validation

- `git apply --check --recount skills/pretty-ui/patches/20261117-124448-skill-size-headroom/change.patch`
- `git diff --check -- skills/pretty-ui/SKILL.md`
- `python3 -m pytest skills/pretty-ui/tests -q`
- `make check-names`
- `make check-style`
- 确认 `SKILL.md` 小于 8192 字节，frontmatter 与引用路径有效，无隐私信息。
