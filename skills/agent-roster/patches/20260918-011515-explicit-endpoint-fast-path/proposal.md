# 明确指定 Endpoint 时增加快速路径并限制 references 预加载

- target: skills/agent-roster
- mode: update
- patch: 20260918-011515-explicit-endpoint-fast-path
- risk: medium
- status: proposed

## Intent

当使用者明确指定唯一 Endpoint 且任务线性时，只读取与选人直接相关的证据，不再枚举无关候选；references 改为按步骤加载，避免路由开始时预读全部文档。保留 decision-before-execution、acpx 安装门禁、权限两档、回收、Trace 与固化规则。

## Conflict check

不改 frontmatter、不删除任一硬门禁、不扩大触发范围，也不把完整路由替换掉；需要自行选人时仍走完整流程。该改动只缩窄“证据面与加载时机”，不改变委派执行层。

## Rationale

真实执行中，使用者已明确指定 Endpoint 的连续 5 次委派仍可能加载 7 份 Endpoint 画像、3 份 references 和相关 Trace，约 2.5 万字符，其中大部分与选人无关。快速路径把“已指定”与“需自选”分开，references 只在执行对应步骤时读取。

## Files

- `skills/agent-roster/SKILL.md`：新增快速路径、references 按需加载规则、完整路由适用条件。

## Validation

- `git apply --check --recount` 通过。
- 应用后与已确认候选稿逐字一致。
- `git diff --check` 通过。
- frontmatter `name` 保持 `agent-roster`。
- 既有 10 条 evals 逐项人工回归通过；无主机名、绝对家目录、内部 URL 或凭据新增。
