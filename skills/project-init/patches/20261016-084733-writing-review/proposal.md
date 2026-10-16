# writing-review：project-init

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

门禁改「算触发」白名单，删「不算触发」清单；两张分层表移入各自 reference（去星级），正文改「默认 + 例外」；非目标改为正向「范围」；工作流关键步补做完的标志；测试同步。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
