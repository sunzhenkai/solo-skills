---
id: role-based-reviewer
name: role-based-reviewer
description: "可组合的角色化只读评审：engineer、algo、data、sre、ops、biz、product、design（别名 uiux）、qa、skill、intent。仅在用户显式点名（/role-based-reviewer）、指定 roles=、明确要求按岗位/多角色视角，或上游工作流以 mode=review + 完整 roles 结构化调用时使用。普通「看看代码」「帮我 review」不要自动加载。"
---

# 角色化评审

面向用户默认简体中文；命令名、路径、代码、状态值保持原文。

- `mode=ask`：按岗位回答问题，标明证据与下游建议。
- `mode=review`：多视角审查，输出分级发现；默认目标为当前工作区变更。

只读：不改代码、不落盘。用户要求修复时再动手。

## 三道门

1. **触发要窄**：用户点名本 skill / `{{slash:role-based-reviewer}}`、写出 `roles=` 或岗位短名、明确要多角色视角，或上游以 `mode=review` + 完整 `roles=` 调用。单独的「看看这段」「帮我 review」「有没有 bug」不算。上游给的审阅边界（判据、审与不审、证据）缺项不拒审：按已有边界审，报告开头写明缺哪块，受影响条目标「未验证」。
2. **角色要少**：未指定 `roles` 时只开 `engineer`；其它角色要主体强信号（文件名沾边不够）；推断超过 2 个只留信号最强的 2 个并在报告开头说一句。调用方或用户给定的 `roles` 照单执行，不增删。
3. **发现要克制**：默认只报 Blocker 与 Major；Minor / Suggestion 仅在用户要求「仔细 / 全面」时给。拿不准不当 Blocker；没问题就说没有，不为每个角色凑一条。

## 输入

- `roles=<逗号分隔>`：`engineer`、`algo`、`data`、`sre`、`ops`、`biz`、`product`、`design`（别名 `uiux`）、`qa`、`skill`、`intent`（仅调用方显式传入，清单见 [references/roles/intent.md](references/roles/intent.md)）。
- `mode=<ask|review>`：默认 `ask`；用户说评审 / review / 审查时为 `review`。
- 范围：未给时默认当前 `git diff`。
- 审阅边界（上游调用时）：判据原文、「审 / 不审」范围、运行态证据（截图 / 断言输出）、观感任务的参照与截图。
- 产物状态：提交号或未提交改动摘要；未给就自取并在报告注明。
- `model=` / `endpoint=`：可选。`endpoint` 经 agent-roster 委派；仅 `model` 时按角色派本机 subagent 并指定模型；都不给就自己审。指定了却都派不出时停下报告调用方，不静默改成同源自审。

示例与调用样例见 [references/inference-and-speed.md](references/inference-and-speed.md)。

## 流程

1. 过三道门，解析 `mode` / `roles` / `model` / `endpoint`。
2. 先读 [references/protocol.md](references/protocol.md)，对每个生效角色加载 `references/roles/<role>.md`；跨角色复用文件，合计宜约 6 个文件。大目标先摸规模再抽样。
3. `ask`：按角色给结论、证据、边界与下游建议。
4. `review`：按角色给 findings，带严重级别与 `path:line`；Blocker / Major 用稳定编号 `F-n`。只合并「同一证据支持的同一风险」，不混写成无归属意见。
5. 下一步默认只推荐一个主责动作。

严重级别定义见 [references/severity.md](references/severity.md)。

## 输出

骨架见 protocol「输出骨架」。review 至少有：依据状态（产物状态 + 边界缺项）、生效角色及依据、各角色 findings 与证据、共享风险的主责、未覆盖项、下一步与置信度。报告只对所标产物状态有效；findings 的处置（`fixed` / `accepted-recorded`）由调用方记录，本 skill 不代判收敛。
