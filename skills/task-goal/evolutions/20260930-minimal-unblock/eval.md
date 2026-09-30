# Eval：minimal-unblock

## 回归

- 全仓契约测试：406 passed, 1 skipped（候选 staged 后）；红绿验证：
  1 条新断言对旧稿失败、对候选稿通过。
- 判定规则零改动：只在 suspension.md blocked 段追加呈现排序，
  五元组/白名单/恢复语义未动。

## 模式

- 多退出点叠加的真实 case 复盘：推荐句同时解两个退出点的事实
  由摘要显式写出并置顶，读者不再自行拼接。✔

## 契约

- `python3 -m pytest skills -q`：406 passed, 1 skipped。

## 副作用

- 无（纯呈现规则）。

## 结论

pass
