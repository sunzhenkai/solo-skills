# Proposal：Web UI 重型门只留 complex；glossary 并入 contract；docs 同步

- target: taskrail 等（见 change.patch）
- mode: update
- patch: 20261015-slim-5-webui-glossary-docs
- risk: medium
- status: applied

## Intent

Active Instance freeze / digest、代表页 two-pass、ui_evidence_check 硬门、design 评审文件只对 complex；medium 改 SHOULD（未做登记 B 类显式降级）。glossary.md 并入 contract.md「术语」节并删除原文件，SKILL / AGENTS 链接改指 contract。evals 同步（删 simple-via-openspec / default-dispatch-digest / simple-driver-one-slice，新增 simple-direct-implement），新增 repo 级 tests/test_evals_structure.py。docs/task-flow/README.md 全量同步。
