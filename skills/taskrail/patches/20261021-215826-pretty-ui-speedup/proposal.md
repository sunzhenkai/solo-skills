# 观感验收改指 pretty-ui 的 evidence.md、轻量卡与单一停止标准

- target: skills/taskrail
- mode: update
- patch: 20261021-215826-pretty-ui-speedup
- risk: low
- status: proposed

## Intent

pretty-ui 同轮提速（`skills/pretty-ui/patches/20261021-215826-speedup/`）把取证拆进 `references/evidence.md`、轻量方向卡上移到 SKILL.md、critique.md 重编号且「迭代与停止」成为唯一停止标准。本轮只改 taskrail 的指针：

- `done.md` 观感验收：视觉方向指向 pretty-ui SKILL.md「轻量方向卡」（整体改版仍指 direction.md 第 6 节）；截图指向 evidence.md；评审材料按 critique.md「隔离评审」「评审手册」节名；goal 迭代的收敛与停止按 critique.md「迭代与停止」，卡住仍按 user-report 第 5 节。
- `confirm-protocol.md`：观感验收的收敛与停止以 critique.md「迭代与停止」为准；意图审、闸口审规则不变。

非目标：goal / human 确认方式不变；ui-delivery、证据门与交接四行不变。

## Conflict check

none（只换指针，链接解析由 `test_pretty_ui_links_resolve` 守住）

## Rationale

原文引用的“critique.md 第 1 节 / 第 3–4 节”在 pretty-ui 重编号后会指错；两边各有一套停止规则时 P1-only 的“需改”判定不一致。

## Files

- `skills/taskrail/references/done.md`
- `skills/taskrail/references/confirm-protocol.md`
- `skills/taskrail/tests/test_aesthetic_goal_contract.py`：新增轻量卡来源、evidence 与单一停止标准断言
- `skills/taskrail/evals/cases.yaml`：`aesthetic-goal-goal-mode` 措辞同步

## Validation

- 应用前：`git apply --check --recount`
- 应用后：`git diff --check`；`~/.local/bin/pytest -q`；`make check-style`；`make check-names`
