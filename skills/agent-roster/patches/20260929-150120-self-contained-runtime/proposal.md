# 安装副本自包含：Role 语义内联、源仓死链标注、真实主机名脱敏

- target: skills/agent-roster
- mode: update
- patch: 20260929-150120-self-contained-runtime
- risk: medium
- status: proposed

## Intent

review（2026-09-29，glm-5.3 版）实证三类问题：

1. 五个约定 Role 的一句话语义只存在于源仓 docs/agent-roster/CONTEXT.md，
   正文以 ../../ 相对路径引用——skill 安装是字节复制，docs/ 不随分发，
   运行时该链接必死、语义无处可读。
2. scripts 与 evolutions 候选稿示例 Endpoint 用真实主机别名（4+ 处，本仓统一改为 example-host），
   evolutions 另有真实项目/trace 名（llmwiki、agentweb），违反公开仓纪律。
3. ADR 链接（endpoint-schema.md:37、SKILL.md:155）同属源仓相对链接。

## Changes

1. roles.md：五个 Role 的一句话语义内联（取自 CONTEXT.md「角色」节）。
2. SKILL.md「角色」「固化」「相关」三处：删源仓相对链接，语义内联或标注
   「只在源仓存在，安装副本不随分发」；endpoint-schema.md 同。
3. example-host/codex → example-host/codex（scripts 与 evolutions 候选稿全部）；
   evolutions 里 llmwiki / agentweb 真实名 → 通用表述。

## Files

- skills/agent-roster/SKILL.md
- skills/agent-roster/references/roles.md
- skills/agent-roster/references/endpoint-schema.md
- skills/agent-roster/scripts/delegate.py、smoke_gate.py（help 文案）
- skills/agent-roster/evolutions/（候选稿同步脱敏）

## Validation

- change.patch 取自实际 git diff
- python3 -m pytest skills -q 全绿
- grep 真实主机别名 / llmwiki / agentweb 全目录 0 命中
