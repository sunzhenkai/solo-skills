# 让量测与规则覆盖被祖先 overflow 裁掉的外扩环

- target: skills/pretty-ui
- mode: update
- patch: 20261117-113718-hairline-clipped
- risk: medium
- status: proposed

## Intent

量测片段（evidence.md 第 3 节）只检查内容层，抓不到「用 `0 0 0 1px` 外扩阴影或 outline 画的细线被祖先 `overflow` 裁掉」——这类缺陷不产生横向溢出，`scrollWidth > innerWidth` 结构上看不见。规则侧同样没有可指认的条目，评审即便看见也拿不到规则号。要改变的模型行为：

- 量测结果新增 `环被裁`，逐条给出元素、被裁的边、裁它的祖先。
- S8 明确外扩环被裁算裁切；H5 补限定（加粗对已被裁的环无效）；误报节补可滚动容器的豁免。
- system.md 边框条目给出 token 层规矩（留 1px 余量 / 不用 overflow / 换 inset 或真 border）。
- 路由把「报遮挡、缺线、看不清」从小改导向 refine，先诊断再改。
- 契约测试加守卫断言，防止能力退化只靠人眼发现。

非目标：不改 build 流程步骤、不改评审手册结构、不新增 reference 文件、不改截图三档的档位定义（只在 evidence 量测节说明 1px 级细线要看 DPR）。

## Conflict check

- SKILL.md 有 8192 字节硬上限（tests `test_size_budget`），原余量 20 字节。路由补句 +38 字节，故压缩同段一句 206→126 字节腾位。
- S8 原文「横向溢出、重叠、裁切」与新增的环被裁不是同一现象，属补充而非改写；不改 1280/375 与 40×40px 的既有阈值。
- H5「细线边框看不清时加粗而不是加深」在新场景下会误导修复方向（实测 2px/3px 外扩环在裁剪容器里同样不可见），加限定而非删除原意。
- 不触碰 worktrees/ 下的镜像检出，不改 `patches/` 历史。

## Rationale

实测（Playwright，遮蔽三档 fixture：无裁剪 / 有裁剪 / 可滚动）显示：原量测片段在三种情形下都返回空问题清单，而同一页实际有 2 处环被裁。加入边缘扫描后：bad 报 2 处（`div.pill 被裁左`、`div.card 被裁左右上下`），good 报 0 处，可滚动容器正确豁免。规则与 token 条目是让评审能指认、让实现能避开同一坑的必要条件，否则量测报出了也过不了「每条问题都要指得到一个规则号」这道门。

## Files

- `skills/pretty-ui/references/evidence.md`：量测片段加 `环被裁` 项，节末补判定口径与 DPR 说明。
- `skills/pretty-ui/references/rules.md`：S8 加外扩环被裁、H5 加限定、误报节加可滚动豁免。
- `skills/pretty-ui/references/system.md`：边框条目补外扩阴影代替 border 时的容器约束。
- `skills/pretty-ui/SKILL.md`：路由小改行末尾补症状转向 refine；压缩同段一句以守住字节上限。
- `skills/pretty-ui/tests/test_pretty_ui_contract.py`：为上述四处补守卫断言。

## Validation

- 应用前：`git apply --check --recount` 通过。
- 应用后：`python3 -m pytest skills/pretty-ui/tests -q` 全绿；`SKILL.md` 字节数 < 8192；量测片段在三个 fixture 上复跑结果与设计一致。
- 隐私：无主机名、绝对路径、私有仓库内容。
