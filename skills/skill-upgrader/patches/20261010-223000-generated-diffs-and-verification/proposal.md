# patch 生成机械化 + 校验补读者与守卫测试

- target: skills/skill-upgrader
- mode: update
- patch: 20261010-223000-generated-diffs-and-verification
- risk: medium
- status: proposed

## Intent

把本轮真实踩坑固化成 skill-upgrader 工作流的两条通用纪律（不绑定任何具体 Skill、不含本仓特有内容）：

1. `change.patch` 用 `git diff --no-index` 机械生成，不手写 hunk；列出手写 hunk 的四个已知失败与 `git apply` 的上下文要求（本机 git 2.55.0 实测）。
2. 应用后校验补两件事：新规则要 grep 读者一并更新（防悬空引用）；目标 Skill 自带契约测试时同轮补守卫断言；`git diff --check` 只对生产文件跑。

非目标：不改模式门禁、patch 目录协议、风险分级，不改任何门禁语义。

## Conflict check

none —— 只加操作纪律，与既有「先 patch 后应用」「不自动 commit」「最小改动」一致；未新增目录或脚本。

## Rationale

本轮实测证据：1) 手写 hunk 失败尝试 ≥5 次，报错均为 `corrupt patch` 或 `patch does not apply`（只给行号），排查代价高；2) 在 `/tmp` 隔离仓库可稳定复现：hunk 无尾部上下文 → `patch does not apply`，补一行尾部上下文 → 通过，零上下文须 `--unidiff-zero`；3) 契约改动漏更新执行侧 phase 文档，另开一轮补丁追回；4) 目标 Skill 的契约测试在应用后才想起，守门断言又占一轮；5) `git diff --check -- <skill-dir>` 会把 patch 文件内的空上下文行报成 trailing whitespace，需限定到生产文件。

结论：这些都不依赖具体 Skill 内容，属通用纪律，写入本 Skill 工作流收益最大。

## Files

- `skills/skill-upgrader/SKILL.md` — 「### 4. 先写 patch」补机械生成纪律；「### 6. 应用与验证」补读者/守卫/空白检查。

## Validation

- 应用前：`git apply --check`（已通过）。
- 应用后：本 Skill 无自带测试（记录 not-available）；人工核对该两段与实测结论一致，frontmatter 未动。
