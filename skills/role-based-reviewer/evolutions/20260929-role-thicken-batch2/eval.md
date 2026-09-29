# eval：role-thicken-batch2

## 回归

- 编排零改动：SKILL.md / preload-protocol / brief-protocol / role-vocabulary 逐字未动。
- 原清单条目全部保留，只追加命中判据与「不算问题」小节；design 的 62 条清单
  与 Blocker 门槛未动，只新增反例小节。
- 分级符号、「拿不准降一级」、运行态降级约定逐字保留。

## 模式

- algo 对上原文 Google Rules of ML（事实）：train/serve 一致（Rule #29/32）、
  评估按时间切分（Rule #33）、特征 owner 文档（Rule #11）、静默失败（Rule #10）
  已融入判据 6/8/9，未照抄条目。
- data / sre / ops / biz 未命中权威原文，判据按公开共识写并在 proposal 记为假设；
  design 沿用文件内已声明来源，未新增参照。

## 契约

- test_role_based_reviewer_contract.py 扩展：THICKENED_FULL 覆盖 8 角色
  （判据/不算问题/redirect/优先锚点/分级符号），design 单独断言「不算问题」小节。
- `python3 -m pytest skills -q`：305 passed, 1 skipped（2026-09-29）。

## 副作用

- 触发范围、权限、密钥处理无变化；文件变长但仍在角色生效时才加载。

## 结论

pass
