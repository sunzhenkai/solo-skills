# 意图确认先推词义、按序读一手资料、默认范围、纠偏先重查

- target: skills/taskrail
- mode: update
- patch: 20261015-231500-source-first-intent
- risk: medium
- status: applied

## Intent

一次「架构图映射物理部署」任务被误做成可编辑数据模型，范围先扩到全部机器又漏掉 Dify / postgres，复述前没读工作区说明与目标的 README / compose，被纠正后继续提问。task-intent 加三条（先推词义与产物、固定读资料顺序、默认范围=目标+直接依赖且摸底带出处），纠偏改为先重查再带出处陈述、用户不满立即停问；intent 评审加三项检查；task-intent / taskrail 加复现 eval。

## Conflict check

接续 no-bookkeeping-questions；不改真阻塞清单。

## Files

见 change.patch。
