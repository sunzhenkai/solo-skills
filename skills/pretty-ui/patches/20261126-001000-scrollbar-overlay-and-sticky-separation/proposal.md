# 滚动条 0px 覆盖式方案与固定头分离

- target: skills/pretty-ui
- mode: update
- patch: 20261126-001000-scrollbar-overlay-and-sticky-separation
- risk: low
- status: applied

## Intent

1. 修正 `G-L5` 滚动条方案：将应用壳 / 多栏 / 带通栏分隔线容器的首选方案从“占位透明轨道 + `scrollbar-gutter: stable`”改为 **0px 占位的覆盖式滚动条**（避免占位轨道截断贴边横线、避免把原生悬浮滚动条降级为占位槽）。
2. 明确整页文档流与固定头边界：整页 `html` 不强加占位滚动条与 `scrollbar-gutter: stable`；要求底线贴边且滚动条起于头部下沿的固定头，必须与滚动容器物理分离，不把固定头用 `position: sticky; top: 0` 塞进滚动容器内部。
3. 补齐 CSS 反模式与检查脚本：`check_page.py` 新增“混写非 `none` `scrollbar-width` 与 `::-webkit-scrollbar`”及“对 `::-webkit-scrollbar-thumb` 直接写 `transition`”两条 `[G-L5]` 提示；`evidence.md` 补充 Headless 默认 overlay 滚动条的取证盲区提示。
4. 同步更新 `reading-page.html`、`evals/cases.yaml`、`test_pretty_ui_contract.py` 与 `test_pretty_ui_scripts.py`。
