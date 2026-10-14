---
slug: demo-list
status: handed-off
phase: propose
tier: medium
confirm_mode: human
criterion: "列表页在 1280x800 与 375x812 下四态可用，axe 无 serious/critical，焦点全程可见"
driver: "demo-list-driver"
---

# demo-list：最小 Web UI 列表页

## 方案
- 单页列表：加载中 / 空 / 出错 / 有数据 四态；复用已 frozen 的 Active Instance。

## 决策
- D-1：采纳单切片方案（medium）。

## 交接
- 交付类别：Web UI
- 适用门包：gate-packs.md「Web UI」
- Active Instance 根路径：design-system/v1
- contract digest：sha256:1f3a0c
- binding digest：sha256:2b7d41
- projection digest：sha256:3c9e52
- driver：demo-list-driver
- 证据要求：`ui_evidence_check.py ui-manifest.json` report exit 0 + design 评审 `--validate-review` exit 0
