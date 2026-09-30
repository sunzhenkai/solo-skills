# Eval：hypothesis-sync

## 回归

- 全仓契约测试：405 passed, 1 skipped（候选 staged 后）；红绿验证：
  2 条新断言对旧生产稿失败、对候选稿全过（第三条断言直接读
  task-goal 源定义，两边都绿——同步锁语义）。
- 其余停止条件与硬边界未动；diff 为两行。

## 模式

- 交界一致性：task-goal 侧定义与 task-delivery 两处副本同口径
  （同假设两败 + 判伪差异 + 封顶 3）。✔

## 契约

- `python3 -m pytest skills/task-delivery/tests -q`：17 passed。
- `python3 -m pytest skills -q`：405 passed, 1 skipped。

## 副作用

- 无新机制；假设记录进验证记录的要求与 task-goal 侧一致。

## 结论

pass
