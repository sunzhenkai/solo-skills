# 来源与许可

本 skill 融合了下列开源项目的方法。除标明“移植”的脚本和原样收录的图解参考外，正文都是按本 skill 的场景（中文界面、阅读页、上游任务流）用自己的话重写的，取舍和改动由本仓负责。

| 来源 | 许可 | 用在哪里 | 许可全文 |
| --- | --- | --- | --- |
| [oil-oil/oil-ui](https://github.com/oil-oil/oil-ui)（参考版本 `7002e1a`） | MIT © 2026 oil-oil | 方向方法（品类与标杆、调性刻度、生成引擎、首屏骨架、方向卡、差异检验、记忆点）、评审手册（三秒测试、提升三项、重做与保留）、AI 默认样貌清单、中文行长阈值 | [licenses/oil-ui-MIT.txt](licenses/oil-ui-MIT.txt) |
| [edisonmbli/refactoring-ui-skill](https://github.com/edisonmbli/refactoring-ui-skill)（参考版本 `4459662`） | MIT © 2026 Edison Li | 规则镜头与扫查顺序、严重度与问题字段、误报与矫枉过正、默认刻度；`scripts/palette.py`、`scripts/contrast.py` 由其 `generate_palette.py`、`check_contrast.py` 移植并改写 | [licenses/refactoring-ui-skill-MIT.txt](licenses/refactoring-ui-skill-MIT.txt) |
| [plannotator/effective-html](https://github.com/plannotator/effective-html) 的 `html-diagram` | MIT © 2026 plannotator | 收录于 `references/html-diagram/REFERENCE.md`，正文原样，只改写了 frontmatter 的 description 并加了与本 skill 衔接的说明 | [references/html-diagram/LICENSE](references/html-diagram/LICENSE) |
| [anthropics/skills](https://github.com/anthropics/skills) 的 `frontend-design` | Apache-2.0 | 早期版本曾原样收录；其中的设计思路已并入 `direction.md` 与 `rules.md` 的 X 组，收录副本已移除 | — |

refactoring-ui-skill 的设计原则源自 Adam Wathan 与 Steve Schoger 的《Refactoring UI》。本 skill 只用自己的话复述方法和必要的数值阈值，没有收录书中的文字或插图；它与原书作者及 Tailwind Labs 没有关联。想系统学习这些原则，请阅读原书。
