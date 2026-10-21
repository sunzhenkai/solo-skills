# writing-review：pretty-view-html

## 背景

按 writing-for-agents（context pointer、信息分层、completion criterion、正向表述、单一真源）与 create-skill（description 写 WHAT+WHEN、引用一层深、手动 skill 设 disable-model-invocation）复审本仓 skill 的写法。

## 改动

正文只留工作流与完成检查；文件组织 / 本地链接 / 同主题包 / 根聚合页下沉 references/organization.md，视觉语言 / 导航 / 表达组件 / 布局下沉 references/visual-components.md，下沉时禁令改正向；html-diagram 不再链 frontend-design（SKILL.md 已直链）；references/frontend-design/REFERENCE.md 路径不变；description 去掉「不做…」。

## 保留

说决定不提问、真阻塞才停、任务边界、source-first、goal/human、审美规则、无嵌套 SKILL.md；不可逆与安全硬闸原样保留并配正向句。

## 风险

low：只动文本组织与 frontmatter；行为由契约测试锁定。
