# minimal-webui：handoff → check_handoff → ui_evidence 回归样例

最小 Web UI 任务（simple 档、单切片）交接后的台账与证据快照，供 `tests/test_e2e_handoff_flow.py` 端到端回放：

1. `workspace/tasks/ongoing/demo-list/TASK.md`：已 `handed-off`，「## 交接」带交付类别、门包与三条 digest。
2. `taskflow/scripts/check_handoff.py workspace demo-list` 应 exit 0；回退到 approve 态或删掉一条 digest 应 exit 1。
3. `ui_evidence_check.py workspace/ui-manifest.json --validate-only`、`--validate-report workspace/evidence/ui/sample/report.json`、`--validate-review workspace/tasks/ongoing/demo-list/design/review-ui.md` 均应 exit 0。
4. 交接节 digest 与 `design/contract.md` 一致（完成门第 7 条）。

`report.json` 是按脚本 schema 合成的样例（截图文件未入库）；装了 playwright + axe-core 时，测试另起本地静态页真跑一遍。
