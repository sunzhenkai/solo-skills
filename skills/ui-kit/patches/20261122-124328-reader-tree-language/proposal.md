# 阅读页/目录树/导航选中：设计语言与验收补口

- target: skills/ui-kit
- mode: update
- patch: 20261122-124328-reader-tree-language
- risk: low
- status: proposed

## Intent

把一轮真实多页应用改造（设置分区、文档阅读、关系图、目录树导航）沉淀为设计语言与验收规则：

1. language.md 补页头动作预算、成对动作合并、画布节点 hover/详情弹窗、视图切换连续性、
   数据形状防御、settings/reader/tree-nav 三个页面模式，以及「导航层级与选中」小节；
2. verify.md 补三类此前漏检的验收：切页连续性、嵌套布局阈值、持久化偏好；并写清 mock 延迟
   验证法（瞬时返回会掩盖整页卸载重建）。

非目标：不改模板代码；模板侧规则见 ui-templates-skill 同批次 patch。

## Conflict check

- 只新增与澄清规则，不改既有小节编号；§9 表格新增两行、修订两行。
- 与 ui-template-apply 的 reader/tree-nav pattern 一一对应，不引入第二套说法。

## Validation

- 文档交叉引用检查：language.md / verify.md / 模板 pattern 术语一致。
- 消费项目按 verify.md 新清单复核：切页连续性、嵌套阈值、持久化均已实测通过。
