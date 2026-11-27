# 补强 taskrail 纠偏与交付验证的 anti-lazy 双层防线接线

- target: skills/taskrail
- mode: update
- patch: 20261127-105600-wire-anti-lazy-correction-and-verify
- risk: low
- status: proposed

## Intent

在 `taskrail` 的纠偏处理与交付验证环节补强 `anti-lazy` 接线，形成「全局/编排节点硬挂钩 + `anti-lazy` 深闸门」的双层防线：

1. `references/intent.md`：用户指出错误、方向不对或漏项时，按 `anti-lazy` 走纠偏重启（声明作废旧假设/改动，回一手资料重查并全量重扫同类遗漏）。
2. `references/verify.md`：按 `anti-lazy` 过交付闸门（逐条对账无静默漏项、按原始场景实跑验证而非静态替代、核对 diff 与同类点无半成品、阻塞缺口必补齐）。
3. `tests/test_neighbor_skill_contract.py`：将 `intent.md` 纳入 `anti-lazy` 接线守卫，并锁定纠偏重启与交付闸门断言。

非目标：不修改 `taskrail/SKILL.md`（保持零日常 token 增量）、不改动 `intent.md` 覆盖清单与复述示例、不新增跨 skill 硬相对链接。

## Conflict check

- 配套 patch：`skills/anti-lazy/patches/20261127-105500-harden-gates-and-conservative-trigger/`。
- 无规则冲突。

## Rationale

单靠 `anti-lazy` 自身触发存在「偷懒时不会主动加载自己」的盲区；在 `taskrail` 的 `intent.md` 纠偏入口和 `verify.md` 交付验证入口显式绑定纠偏重启与交付闸门，可在编排链路的关键节点稳定生效。

## Files

- `skills/taskrail/references/intent.md`：补强纠偏重启接线
- `skills/taskrail/references/verify.md`：补强交付闸门核对项
- `skills/taskrail/tests/test_neighbor_skill_contract.py`：扩展 `anti-lazy` 接线守卫测试

## Validation

- `git apply --check --recount skills/taskrail/patches/20261127-105600-wire-anti-lazy-correction-and-verify/change.patch`
- `python3 -m unittest discover -s skills/taskrail/tests -p 'test_*.py' -v`
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `make check-names && make check-style`
- `git diff --check -- skills/taskrail`
