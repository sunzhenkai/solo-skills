# writing-review：skills-store

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

正文留作用域与审计工作流；CLI flag、命令示例、用户说法映射下沉 references/cli.md（注明以 --help 为准，只留查不到的坑）；已知误报表下沉 references/known-false-positives.md（.audit-allow 路径同步）；Self-evolution 样板改一句指针；禁令改正向句，保留「禁止为放行删规则」硬闸并配正向句；测试同步。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
