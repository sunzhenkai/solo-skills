# eval：role-thicken-batch1

## 回归

- 编排零改动：SKILL.md 三道门禁、preload-protocol、brief-protocol、role-vocabulary
  逐字未动；角色文件仍只在生效时加载（preload-protocol 不变，加厚的是文件内容不是加载面）。
- 原清单条目全部保留（engineer 10 条、qa 原 7 条扩为 8 条、product 原 6 条扩为 7 条），
  只追加命中判据与新小节，无删除既有检查项。
- 分级符号与「拿不准降一级」「运行态降级」约定逐字保留。

## 模式

- 原先「同级别问题口径不稳」：每条清单现在有可对照的命中判据（给得出具体路径/输入/证据才报）。
- 门 3「防吹毛求疵」原来只有全局约束，现在三个高频角色各有「不算问题」反例小节可援引。
- 参照来源已按 task-wizard 外部参照细则记录：eng-practices 对上原文（事实）；
  OWASP / testing.googleblog / 需求评审清单仅搜索命中未读原文（假设，已在 proposal 声明）。

## 契约

- 新增 tests/test_role_based_reviewer_contract.py：门禁存在性、角色枚举不变、
  加厚三角色的结构断言（命中判据 / 不算问题 / redirect / 优先锚点 / 分级符号）、
  其余 6 角色文件存在性。
- `python3 -m pytest skills -q`：305 passed, 1 skipped（2026-09-29）。

## 副作用

- 触发范围、权限、破坏性操作、密钥处理均无变化。
- 文件变长（engineer 36→60 行级别），但按 preload-protocol 只在角色生效时加载，不占默认上下文。

## 结论

pass
