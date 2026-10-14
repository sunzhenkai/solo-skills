# Proposal：数字门槛降为建议

- target: taskrail 等（见 change.patch）
- mode: update
- patch: 20261015-slim-3-thresholds-to-should
- risk: medium
- status: applied

## Intent

执行座位改为「宜派」：去掉交接 5 项缺一不派、Digest ≤10 行、1/3/5 上限、不派须写理由；保留永不派出（闸口 / 提问 / 危险退出）、详情落盘只回摘要。验收 rubric 去掉「五维均 ≥2、UI/UX 均值 ≥2.5」硬线，改为无未处置 Blocker/Major + 判据逐条有证据，分数作参考；旗舰先行 / 共享面广播限 complex 多切片；rbr 文件预算改建议；intent 角色去掉分数线、加「上下文不支撑做法」检查。check_output_style.py 改为：SKILL.md 超 8K 告警，意图模板缺字段才报错。
