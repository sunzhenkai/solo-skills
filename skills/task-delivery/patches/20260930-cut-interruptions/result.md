# Result：缺依赖 skill 不原地停

已 `git apply` 应用。

## 应用后的正文变化

`references/loop-protocol.md` Stage 0 原文「检查依赖 skill 可读。缺依赖时停止；不手写替代 OpenSpec / taskflow / reviewer 流程。」改为：

> 检查依赖 skill 可读。缺依赖时不停在原地：同一条回复里给出一次性安装提示与推荐项（`make install-deps` 或 `dotf agents -c`），用户确认安装后继续；用户明确表示不装时才停止。不手写替代 OpenSpec / taskflow / reviewer 流程。

## 测试

`python3 -m pytest skills/task-delivery -q` 全过；全仓 415 passed, 1 skipped。

## 遗留

- 无。

## 未验证 / 待观察

`make install-deps` 与 `dotf agents -c` 是本仓 README「外部依赖」记录的既有入口，尚未在实际缺依赖场景下验证该提示是否足够让用户一步装齐（尤其 acpx 是二进制、需手动装）。
