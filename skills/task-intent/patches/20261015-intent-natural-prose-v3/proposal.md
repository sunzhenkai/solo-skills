# Proposal：意图复述改为自然口语，字段清单只作内部覆盖检查

- target: skills/task-intent（连带 scripts/check_output_style.py、tests/test_output_style.py、taskrail evals、docs/task-flow、README）
- mode: update
- patch: 20261015-intent-natural-prose-v3（承接 20261015-intent-template-v2）
- risk: low
- status: applied

## Intent

用户反馈：复述不要机械打印带标签的模板。参照输出：「好，我按仓库的约定挑个合适的位置写成一份文档，内容包括流程图、各 skill 的分工、两种模式、三个档位的区别和怎么用，并在 README 和 taskrail 里加链接。写完告诉你放在哪。」

- 7 项（要干嘛 / 怎么干 / 输出什么 / 上下文 / 不做 / 假设 / 拍板）降为内部覆盖清单，结构化写进 `wizard/intent.md`「覆盖清单」节。
- 给用户的复述：1–3 句第一人称口语，自然带出做什么 / 怎么做 / 产出落点，以接下来会发生什么收尾；上下文、假设、不做只在影响结果时顺带；最多一个问题自然嵌入并带推荐；不打标题、不加粗标签、不逐项列字段。
- references 给 3 条口语示例（用户参照原句、带假设、带问题）+ 1 份 intent.md 覆盖清单示例。
- check_output_style：覆盖清单缺字段 → 错误；口语示例出现加粗 / 标题 / 字段名开头 → 告警。

## 扩展：所有面向用户的输出都用口语（同一 patch）

用户补充：其他对用户输出的地方也应自然易懂，而不是冰冷的术语堆砌。

- taskrail 契约新增共用节「对用户说话」（唯一出处）：第一人称、结论先行；内部术语（driver / tier / criterion / gate / slice / OpenSpec / phase）不裸露或附白话；不倒「字段：值」、不贴 ID 堆；最多一问带推荐；结尾说下一步。附 3 组前后对比（闸口提问、进度、评审摘要）。落盘文件仍可结构化。
- 引用点（不复制规则）：taskrail SKILL.md、confirm-protocol human 闸口呈现、执行座位摘要转述、task-explore SKILL.md、taskflow SKILL.md、role-based-reviewer protocol 输出骨架、task-intent references。
- check_output_style：契约缺该节或前后对比少于 3 组 → 错误。测试 +2（共用节、各 skill 引用）；taskrail evals 加 `plain-talk-to-user`；docs/task-flow 加「对用户怎么说话」一节与 FAQ。
