# Decision: promote

- patch: evolutions/20260930-minimal-unblock
- decision: promote
- date: 2026-09-30
- 用户确认: Phase 5 计划（最小解除集 + 升档补画像两小轮）当轮以
  「继续」确认执行；risk: low。

## 原因

- 真实 blocked case 的解除成本可复核（推荐句覆盖两个退出点但
  需读者自行拼出）；呈现规则缺口稳定。
- eval pass：diff 一段；全仓 406 passed。

## 晋升后验证

- `python3 -m pytest skills -q` → 406 passed, 1 skipped。

## 未做

- commit 由本轮统一提交；未 push、未 dotf 同步。
- 5b（升档补画像草稿）属下一小轮。
