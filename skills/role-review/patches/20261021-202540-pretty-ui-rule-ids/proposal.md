# design 角色的视觉意见落到 pretty-ui 规则号

- target: skills/role-based-reviewer
- mode: update
- patch: 20261021-202540-pretty-ui-rule-ids
- risk: low
- status: proposed

## Intent

design 角色第 5 节「视觉与一致性」只有四条概括性检查，第 35 条 anti-slop 自 `20261015-234800-despecialize-task-boundary` 去掉具体样例后只剩一句“套用万能配色/版式套路”，评审者没有可指认的依据；「不算问题」又要求“视觉审美结论须能指到具体条目”，于是大多数视觉意见要么不报，要么落成口味之争。pretty-ui 重写后（`skills/pretty-ui/patches/20261021-200926-fuse-oil-ui-refactoring-ui/`）有一套带编号的视觉规则（H / S / T / C / D 与 X 组 AI 默认样貌），本 patch 让 design 角色引用它：

- 第 5 节开头一句：视觉意见写成「规则号 + 现状 + 改法」，级别仍按本清单。
- 第 35 条改为对照 X 组（X1–X12），命中时写规则号。
- 「不算问题」的“像素与间距口味”：落不到 token 判定或 pretty-ui 间距规则（S2、S3）时不报。
- 「天花板参照集」补一句参照集的常见来源（pretty-ui 方向卡）；「下游建议」补上视觉方向、设计体系与打磨交给 pretty-ui。

非目标：三道门、默认只报 Blocker / Major、quality floor 的 🔴 条、调用范围与速度、其余清单条目与级别都不变。pretty-ui 的 P0 / P1 / P2 用于它自己的评审与 taskrail 观感验收，本角色的级别仍按本清单判定，避免两套级别互相覆盖。

## Conflict check

- 测试锁定的 `## 调用范围与速度` 保留，`tier=simple` 仍不出现。
- 结构：本 skill 尚无 `examples/` / `evals/` / `experience/`；本轮只改指针，按 skill-upgrader 的 update 模式处理，不顺带补结构（结构升级需单独走 self-upgrade）。
- 跨 skill 链接 `../../../pretty-ui/references/rules.md` 由新测试校验可解析；条目文字本身仍可独立理解，单独安装本 skill 时只是少了规则号出处。

## Rationale

规则号让视觉意见可追溯、可争辩、可复核，也和 taskrail 观感验收、pretty-ui 评审用同一套词，跨 skill 的评审结论可以直接对照。

## Files

- `skills/role-based-reviewer/references/roles/design.md`
- `skills/role-based-reviewer/tests/test_role_based_reviewer_contract.py`（新增 `test_design_visual_rule_ids`）

## Validation

- 应用前：在仓库外的干净副本上 `git apply --check --recount`，应用后与候选树一致
- 应用后：`git diff --check`；`python3 -m pytest skills/role-based-reviewer/tests -q`；全量 `python3 -m pytest skills tests -q`；`make check-style`；`make check-names`
