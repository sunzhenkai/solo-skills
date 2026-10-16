# writing-review：commit-push

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

description 只留正向 WHAT+WHEN，边界移到正文一句；安全协议七条「不要」改为「安全默认 + 以下情况先确认」，force / amend / 跳过 hooks / 改 git config / 提交密钥文件等硬闸全部保留；冲突细则下沉 references/conflicts.md，正文留入口与做完的标志；契约测试改断言正向句与硬闸清单。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
