# 看图取证

[pretty-ui](../SKILL.md) 的看图步骤、page 模式的检查、上游流程的截图与量测读本页。截图分三档，按场合取，不多截。

## 1. 工具与打开方式

- 截图工具按序选：宿主的浏览器工具 → 项目已有的截图或 e2e 工具 → taskrail 的 `scripts/ui_evidence_check.py`（需要 playwright）。都用不了时，结论标“未渲染验证”，问题标 `code-only`。
- 本地页面用 `python3 -m http.server --bind 127.0.0.1 <端口>` 起服务再打开，部分浏览器工具拦截 `file://`；用完关掉服务。
- 页面开了 `scroll-behavior: smooth` 时，截某一区域前用 `window.scrollTo({ top, behavior: "instant" })` 跳过去，免得截到滚动中途。

## 2. 三档截图

| 档 | 何时 | 截什么 |
| --- | --- | --- |
| 基础档 | 每次看图、首轮评审 | 桌面 1280 与手机 375 各截首屏和整页，共四张；每个视口跑一次第 3 节的量测；静态页面跑 `check_page.py` |
| 状态档 | 交付前的最后一轮，截一次 | 本次新增或改动涉及的状态：空、加载、出错、长文本、数据很多；有交互的再截默认、悬停或聚焦、选中、禁用 |
| 复审档 | 第二轮起 | 只截上一轮问题涉及的区域和视口，同一路由、同一份演示数据 |

- 三秒测试用的缩略图（首屏缩到 480 宽，手机图缩到 180 宽）由基础档截图缩小得到，不另截；遮掉文字的版本只在评审者要求时另截。
- 关键区域按 100% 看，精致度按 200% 看，放大已有截图即可。
- **改前改后**：refine 和上游要求对比时，改前也截基础档，改后用同一路由、同一视口、同一份演示数据。

## 3. 量一量

浏览器工具能执行脚本时，在每个视口跑一次下面的片段，把结果和截图放在一起：

```js
(() => {
  const r = { 横向溢出: document.documentElement.scrollWidth > innerWidth, 行太长: [], 字太小: [], 行高过紧: [] };
  for (const el of document.querySelectorAll("p, li, dd, blockquote, td")) {
    const t = el.textContent.trim(), s = getComputedStyle(el), size = parseFloat(s.fontSize);
    if (t.length < 30 || !el.offsetWidth) continue;
    const zh = /[\u4e00-\u9fff]/.test(t), w = el.getBoundingClientRect().width;
    const perLine = Math.round(zh ? w / size : w / (size * 0.5));
    const lh = s.lineHeight === "normal" ? 1.2 : parseFloat(s.lineHeight) / size;
    const tag = el.tagName.toLowerCase() + "「" + t.slice(0, 12) + "」";
    if (perLine > (zh ? 46 : 95)) r.行太长.push(tag + " 约 " + perLine + (zh ? " 字" : " 字符"));
    if (size < 12.5) r.字太小.push(tag + " " + size + "px");
    if (lh < (zh ? 1.5 : 1.4)) r.行高过紧.push(tag + " " + lh.toFixed(2));
  }
  return r;
})()
```

表格单元格里的短行不算行太长；它只是线索，结论以截图为准。

## 4. 证据路径

截图、量测结果、评审记录放任务目录或项目约定位置，交付说明里写路径。
