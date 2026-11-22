# Result — 阅读页/目录树设计语言补口

## 落点

- `references/language.md`：§7 页头动作预算（默认 2、iconOnly 4–5、destructive 永不内联）与成对动作合并、
  画布 hover 浮层/详情弹窗；§8 `keepPreviousData` 连续性与形状防御；§9 settings 行改写、
  新增 reader / tree-nav 两行、detail 行补目录与弹窗；新增 §9.1 导航层级与选中。
- `references/verify.md`：新增「连续性、嵌套布局与持久化」小节（切页不卸载、mock 延迟 ≥800ms、
  嵌套 Split 阈值、跨刷新偏好）。

## 验证

- 术语与模板仓 `patterns/reader.md`、`patterns/tree-nav.md` 对齐。
- 相关规则在消费项目实测通过（切页连续性、窄屏回退、目录隐藏跨刷新）。
