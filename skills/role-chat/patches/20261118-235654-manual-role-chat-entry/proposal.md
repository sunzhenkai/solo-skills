# 对齐 role-chat 的手动入口

- target: skills/role-chat
- mode: update
- patch: 20261118-235654-manual-role-chat-entry
- risk: high
- status: proposed

## Intent

让 description 和门 1 都只把点名 role-chat 或 slash 调用视为入口，把 `roles=`、角色短名和多视角要求定义为进入后的输入。保持角色注册、组合、切换和输出行为不变，避免与 role-based-reviewer 的 `roles=` 自动触发冲突。

## Conflict check

符合 `disable-model-invocation: true` 的调用机制；role-based-reviewer 继续独立处理自己的 `roles=` 触发，本次不修改其契约。

## Rationale

原描述和正文宣称单独写 `roles=` 或角色短名即可触发，但模型无法发现禁用自动调用的 Skill。统一手动入口后，调用说明与运行机制一致，并可通过文本契约测试守护。

## Files

- `skills/role-chat/SKILL.md`：修改 description 与门 1。
- `skills/role-chat/tests/test_role_chat_contract.py`：守护手动入口和参数边界。

## Validation

- `git apply --check --recount` 校验 patch。
- 运行 role-chat 契约测试。
- 运行 `make check-style`、仓级检查与全量测试。
