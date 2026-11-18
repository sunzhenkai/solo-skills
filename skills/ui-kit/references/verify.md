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

J06 / J10 是 ui-template-apply 目检流程的提示；ui-kit 用像素比对代替目检，可忽略。

## 保真比对做了什么

`verify_fidelity.py` 在 `.ui-kit/` 下现场生成基线：骨架 + 项目的依赖锁 + 纯净模板文件 + 项目的 `theme.css` / `fonts.css`，渲染所有 `ui-kit/*` story（浅、深各一张）；再渲染项目自己的同一批 story，零像素容差比对。所以白名单内的定制不会失败，模板文件或渲染配置一改就失败。

- 首次运行要给基线装依赖，较慢；`--reuse-baseline` 跳过基线重建（主题没变时用）。
- `.ui-kit/`、`storybook-static/`、`test-results/` 不提交（骨架的 `.gitignore` 已包含）。
- Playwright 浏览器缺失时先 `npx playwright install chromium`。
