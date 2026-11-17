# 门 1 与「仅手动调用」一致，缺 CLI 提示改用上游安装命令

- target: skills/lark-cli
- mode: update
- patch: 20261118-014610-manual-gate-wording
- risk: low
- status: proposed

## Intent

frontmatter 已设 `disable-model-invocation: true`，门 1 原写「或明确要操作飞书业务」也算触发，这半句不会生效。改为：仅手动进入；点名后要操作飞书业务才走门 2，只是问概念时直接回答。缺 CLI 时的 echo 提示改用上游 `npm install -g @larksuite/cli`，正文已有的 dotf 等效说明保留。非目标：路由、加载与禁止项不变。

## Conflict check

none。

## Rationale

消除 frontmatter 与门禁的矛盾；公开分发的 skill 默认提示不依赖个人环境工具。

## Files

- skills/lark-cli/SKILL.md：门 1；预检 echo。

## Validation

- 无自带测试；全量测试与 `make check-style`
