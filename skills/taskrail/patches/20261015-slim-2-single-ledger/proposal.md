# Proposal：一本账：删 status×phase 矩阵，精简交接载荷

- target: taskrail 等（见 change.patch）
- mode: update
- patch: 20261015-slim-2-single-ledger
- risk: medium
- status: applied

## Intent

TASK.md 定为唯一任务账，driver 只是 OpenSpec 执行记录；删 status×phase 合法组合矩阵，改一句「status 随 phase 走」；propose 载荷行去掉重复的画像 / 降级 / 交接节字段罗列。check_handoff.py 及其测试保留未动。
