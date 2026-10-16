# writing-review：project-spec-mirror

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

description 去掉「不用于…」，边界放正文；禁写清单、占用目录、experience 说明改正向句，测试改断言正向句。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
