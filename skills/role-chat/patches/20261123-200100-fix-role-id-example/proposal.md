# 修正示例角色 id 并补齐注册表一致性断言

- target: skills/role-chat
- mode: update
- patch: 20261123-200100-fix-role-id-example
- risk: low
- status: proposed

## Intent

将示例中的 `roles=product,finance` 修正为与注册表一致的 `roles=product-manager,finance`，并在契约测试中锁定示例角色均来自已注册 role-id。

## Conflict check

none

## Rationale

注册表第 43 行声明的 role-id 为 `product-manager`，示例误用相邻 skill（role-based-reviewer）的短名 `product`，容易误导调用者。

## Files

- `skills/role-chat/SKILL.md`：修正示例中的角色 id 为 `product-manager`
- `skills/role-chat/tests/test_role_chat_contract.py`：新增示例角色 id 必须属于注册表的守卫断言

## Validation

- `git apply --check --recount skills/role-chat/patches/20261123-200100-fix-role-id-example/change.patch`
- `python3 -m unittest discover -s skills/role-chat/tests -p 'test_*.py'`
- `make check-style && make check-names`
