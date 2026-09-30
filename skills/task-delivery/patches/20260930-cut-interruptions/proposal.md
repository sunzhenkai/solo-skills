# Proposal：缺依赖 skill 不原地停（task-delivery 侧）

## 背景

Stage 0 原文：「检查依赖 skill 可读。缺依赖时停止；不手写替代 OpenSpec / taskflow / reviewer 流程。」这是一条环境性停机：用户不在场时（goal 自动续跑）无法推进，而安装动作本身是一次性的、可预先给出的。

## 决定

改为：缺依赖时**不停在原地**——同一条回复里给出一次性安装提示与推荐项（`make install-deps` 或 `dotf agents -c`），用户确认安装后继续；用户明确表示不装时才停止。保留「不手写替代 OpenSpec / taskflow / reviewer 流程」。

## 理由

- 追加选项不违反「不发明等价流程」：安装提示指向本仓既有的 Makefile 与 dotf 入口，两者都在 README「外部依赖」里有记录。
- 与 taskflow 侧同批改动一致（同样把「停下报告并给出可选项」改为「同一条回复给全选项与推荐项，用户选完即继续」）。

## 验证

- `python3 -m pytest skills/task-delivery -q` 全过。

## 明确不改

`references/loop-protocol.md` 的其余 Stage、Stop conditions、增量验证协议、hard boundaries。
