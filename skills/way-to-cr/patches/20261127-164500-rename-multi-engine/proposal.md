# 改名 way-to-cr 并重构为多引擎代码审查

- target: skills/way-to-cr
- mode: update
- patch: 20261127-164500-rename-multi-engine
- risk: medium
- status: applied

## Intent

将 `solo-code-review` 改名为 `way-to-cr`，支持内置审查（`builtin`）、Claude Code（`claude`）、Codex（`codex`）与 Open Code Review（`ocr` / `delegate`）四种方案，并落地四步主流程：先思考审查内容与范围 → 选择审查方案 → 外置引擎模型选择与记忆复用 → 出报告及可选落盘 / 发布 MR/PR 评论。

## Rationale

`ocr` 单独作为唯一入口过于笨重且耗时；个人日常开发优先需要零依赖的内置审查或复用已有 Claude Code / Codex CLI 订阅，同时保留 OCR 作为可选增强，并在外置引擎间持久化用户的模型选择。

## Files

- `skills/way-to-cr/SKILL.md`：重写为四步流程与多引擎路由
- `skills/way-to-cr/references/builtin-review.md`：新增内置审查细则（含 `AGENTS.md` 对齐）
- `skills/way-to-cr/references/external-agents.md`：新增 Claude Code 与 Codex CLI 细则
- `skills/way-to-cr/references/ocr-mode.md`：拆出 OCR 引擎细则
- `skills/way-to-cr/references/delegate-mode.md` / `mr-mode.md`：对齐多引擎与 `way-to-cr` 流程
- `skills/way-to-cr/scripts/reviewctl.py`：新增 `prefs`、`probe`、`preview`、`render`，扩展 `write`
- `skills/way-to-cr/tests/` & `evals/cases.yaml`：补充多引擎、偏好、预览与契约测试

## Validation

- `python3 -m unittest discover -s skills/way-to-cr/tests -p 'test_*.py'`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `make check-names && make check-style`
