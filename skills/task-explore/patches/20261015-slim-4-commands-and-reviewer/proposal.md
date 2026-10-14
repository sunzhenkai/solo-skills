# Proposal：task-explore 命令细则压缩 + role-based-reviewer 协议合一、角色分核心 / 可选

- target: task-explore 等（见 change.patch）
- mode: update
- patch: 20261015-slim-4-commands-and-reviewer
- risk: medium
- status: applied

## Intent

archive-reopen.md 10.2K → 3.1K（通用原则：不覆盖、不搬未确认的、先列未结项）；commands.md 的 archive / reopen 改为指针；SKILL.md「Goal 里的确认」压成一段。对应 22 条逐字测试删除，改为 4 条行为检查。role-based-reviewer：constraints / preload-protocol / brief-protocol / role-vocabulary 合并为 references/protocol.md（内容未改，标题降级）；核心角色 engineer / product / design / qa / intent，可选角色 algo / data / sre / ops / biz / skill 不参与推断。
