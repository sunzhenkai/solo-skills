# 加固 anti-lazy 门禁与保守自动触发描述

- target: skills/anti-lazy
- mode: update
- patch: 20261127-105500-harden-gates-and-conservative-trigger
- risk: high
- status: proposed

## Intent

将 `anti-lazy` 从开放式自我反思提示升级为可核查的反偷懒硬闸门，并收紧 `description` 触发条件为保守自动引入：

1. 优化 `description` 为正向 WHAT + WHEN，限定在用户纠正方向/指出偷懒、多要求或高歧义复杂任务起手、以及实质改动宣称完成前引入。
2. 正文增加「保守触发与豁免」白名单、「入口分流」（起手对齐 / 纠偏重启 / 交付闸门）、「纠偏重启协议」、1–3 节完成门、6 类高频偷懒信号强制自检表，以及「5. 收口硬闸」。
3. 在 `evals/cases.yaml` 补齐对抗性反偷懒与保守触发边界用例，在 `tests/test_anti_lazy_contract.py` 锁定关键门禁与描述约束。

非目标：不新增 `examples/` 或 `experience/` 目录（恪守 `update` 模式边界），不改变向 `trouble-grill`、`taskrail`、`session-wrap` 的升格边界。

## Conflict check

- 配套 patch：`skills/taskrail/patches/20261127-105600-wire-anti-lazy-correction-and-verify/`（负责 `taskrail` 的纠偏与交付验证双层防线接线）。
- 沿用现有升格出口：`trouble-grill`（多轮根因排查）、`taskrail`（跨会话台账与父子拆分）、`session-wrap`（会话收尾）；不与它们重复造轮子。

## Rationale

开放式问句缺少可判定完成门与拦截红线，容易在内部思考中滑过；通过明确豁免白名单、三入口分流、6 类反模式自检与收口硬闸，同时收紧 `description` 避免简单任务误触，既能拦截漏项与假验证，又保持零模板负担。

## Files

- `skills/anti-lazy/SKILL.md`：重构 `description` 与正文门禁结构
- `skills/anti-lazy/evals/cases.yaml`：追加 5 条对抗性与保守触发边界用例
- `skills/anti-lazy/tests/test_anti_lazy_contract.py`：更新契约断言以守卫触发约束与核心门禁

## Validation

- `git apply --check --recount skills/anti-lazy/patches/20261127-105500-harden-gates-and-conservative-trigger/change.patch`
- `python3 -m unittest discover -s skills/anti-lazy/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-names && make check-style`
- `git diff --check -- skills/anti-lazy`
