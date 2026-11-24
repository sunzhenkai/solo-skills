# 验收

新建、定制、升级之后都跑同一套，按顺序，全部通过才算完成：

```bash
npx tsc -b
npx eslint .
python3 <kit>/skills/ui-template-apply/scripts/validate_package.py project .
python3 <kit>/skills/ui-template-apply/scripts/verify_fidelity.py --project .
npm run build
```

## 结果怎么读

| 结果 | 含义 | 修法 |
| --- | --- | --- |
| C01 / C02 | 定制后对比度不足 | 调明度 L，不降门槛 |
| J12 | 主题在白名单外偏离风格包 | 改回包值，或记入 `theme_deviations` |
| J03（警告） | 模板文件被改 | 撤回；确要保留记 `local_edits`，该文件退出保真 |
| `fidelity: FAIL` | 模板组件或页面模板渲染得和模板不一样 | 看 `test-results/` 的差异图，找到被改的模板文件或渲染配置并撤回 |
| J10（已有 `pages`） | 缺 `ui-review.md`、缺路由，或某个声明过的状态没有审查行 | 按 ui-template-apply 的 07 补拍并写上 `- [x] state <name>` |
| J11 | 审查里还有 `- [ ]` 或 `status: pending` | 修完再勾；受锁文件走 `upstream:`，见 update.md |
| J13 | 审查点名了锁内文件，但锁版本还低于 `upstream:` | 升级模板到该版本后重拍该路由 |

两条都要过，互不替代：

- **保真**：`verify_fidelity.py` 通过，只说明模板文件和 `ui-kit/*` story 没被改。页面文案、空态、390 宽和自定义画布不在保真范围内。
- **产品页**：`validate_package.py project` 0 error。已经写了 `pages` 时，缺 `ui-review.md`、缺路由、缺声明过的状态都是 J10 错误；未结项或 `status: pending` 是 J11 错误。还没有页面清单时，J10 仍是警告（刚装完的骨架）。J06 仍是缺 `ui-decisions.yaml` 的警告。

不要用保真通过代替产品页目检。

## 校准不是保真

保真证明「项目 = 模板」，**不证明「模板 = 参照产品」**。风格包与参照的偏差（字重、行高、控件档位、
浮层阴影）只能靠 `ui-template-author` 的采集校准（见该 skill 的 `references/calibration.md`）与部署后
线上复核发现——本地全绿但线上仍能查出错位是常态（quiet-inset 0.6.0 的浮层阴影接线缺口即如此）。

模板或主题改动后的验证顺序，三者互不替代：

1. **校准**：参照产品实测 vs 包 token / 组件类，采样驱动；
2. **保真**：项目渲染 = 模板渲染（本文件本节的流程）；
3. **线上复核**：部署后对真实页面抽 computed style，核对目标值。

## 交互态必须打开检查

页面默认可见内容只是验收的一半。**详情抽屉、确认对话框、表单弹窗、命令面板、下拉菜单、tooltip
不会出现在 fidelity 基线里**（story 不含页面自定义组合），默认截图也看不到——它们的 padding/边框/
层级问题只能靠「打开一次」发现。每轮验收按清单逐类打开并检查（2026-11-21 timeline 详情抽屉内容
贴边 bug 即此盲区漏检）：

- 列表行 → 详情抽屉/面板（Sheet）
- 危险操作 → 确认对话框（Dialog/AlertDialog）
- 新建/编辑 → 表单弹窗
- 页头搜索 → 命令面板；筛选 → 下拉/Tooltip
- 每一类都检查：内边距（内容是否贴容器边框）、边框是否与容器线相邻成双线、滚动区域边界、焦点进入与 `Esc` 归还。接入 taskrail 运行态机械门时，可把上述交互浮层写进 manifest 的 `overlays` 自动核对。

## 连续性、嵌套布局与持久化

默认截图与保真都看不到「切换过程」和「跨刷新状态」，每轮验收补三类检查：

- **切页连续性**：连续点击列表/树里的条目切换文档，页面壳（页头、导航、目录）不得卸载重建，
  不得整页骨架/白屏；切换过程允许保留上一份内容。验证时给关键接口加 ≥800ms 人为延迟
  （mock 瞬时返回会把「整页卸载重建」掩盖成肉眼看不到的闪烁）。
- **嵌套布局阈值**：正文 + 右栏这类嵌套 `Split`，显隐阈值按「页面宽度 − 已占列宽」判断，
  不要拿页面宽度和内层容器宽度混用；窄屏回退（弹窗/横向滚动）要实际缩窗口验证。
- **持久化偏好**：目录/侧栏的显隐、折叠记忆等写入本地存储后，刷新与重进页面仍生效；
  无痕窗口不报错（存储不可用时静默回退）。

## 保真比对做了什么

`verify_fidelity.py` 在 `.ui-kit/` 下现场生成基线：骨架 + 项目的依赖锁 + 纯净模板文件 + 项目的 `theme.css` / `fonts.css`，渲染所有 `ui-kit/*` story（浅、深各一张）；再渲染项目自己的同一批 story，零像素容差比对。所以白名单内的定制不会失败，模板文件或渲染配置一改就失败。

- 首次运行要给基线装依赖，较慢；`--reuse-baseline` 跳过基线重建（主题没变时用）。
- `.ui-kit/`、`storybook-static/`、`test-results/` 不提交（骨架的 `.gitignore` 已包含）。
- Playwright 浏览器缺失时先 `npx playwright install chromium`。
- **skip 不算绿**：渲染/保真用例因浏览器或依赖缺失被 skip 时，结果必须写明实际运行数而不是报「全绿」。python 侧先 `python3 -m pip install playwright` 再实跑（本机可能从未装过 python 包，历史 skip 常源于此）。
