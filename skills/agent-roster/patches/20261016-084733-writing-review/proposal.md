# writing-review：agent-roster

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

description 收成 3 个真分支、关键词前置；SKILL.md 把 6 个只有指针的小节合并为「按需读取」表，从正文一层直链全部 references（含 flow-*、roles、trace-format、endpoint-schema），references 之间的链接改成文件名；flow.md「不要预加载其它 Stage」改正向句；gate_lines 同步。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
