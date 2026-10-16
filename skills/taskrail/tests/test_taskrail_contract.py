"""taskrail 不可破契约：phase 枚举、handoff 入口、说决定真源、完成清单、档位、文件存在。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def read(*parts: str) -> str:
    return (ROOT.joinpath(*parts)).read_text(encoding="utf-8")


class ContractTest(unittest.TestCase):
    def test_skill_under_8kb(self) -> None:
        self.assertLessEqual(len((ROOT / "SKILL.md").read_bytes()), 8192)

    def test_references_exist(self) -> None:
        for name in ("contract.md", "done.md", "user-report.md", "confirm-protocol.md",
                     "phase-wizard.md", "ui-delivery.md", "quality-appendix.md", "external-precedent.md"):
            self.assertTrue((REF / name).is_file(), name)

    def test_phase_enum_closed(self) -> None:
        c = read("references", "contract.md")
        self.assertIn("wizard | explore | design | approve | propose | apply | archive | done", c)
        self.assertIn("tier: skip | full", c)
        self.assertIn("confirm_mode: human | goal", c)

    def test_pipeline_and_handoff(self) -> None:
        c = read("references", "contract.md")
        self.assertIn("wizard → explore(grill) → design → approve → [handoff] → propose → apply → archive", c)
        self.assertIn("check_handoff.py", c)
        self.assertIn("唯一下一步是 `handoff`", c)
        skill = read("SKILL.md")
        self.assertIn("check_handoff.py", skill)
        self.assertIn("done.md", skill)

    def test_skip_full_paths(self) -> None:
        c = read("references", "contract.md")
        self.assertIn("`skip`", c)
        self.assertIn("`full`", c)
        self.assertIn("simple` 按 `skip`", c)
        self.assertIn("medium` / `complex` 按 `full`", c)

    def test_say_decide_single_source(self) -> None:
        ur = read("references", "user-report.md")
        self.assertIn("说决定，不提问", ur)
        self.assertIn("真阻塞才停", ur)
        self.assertIn("唯一真源", ur)
        self.assertIn("已做决定", ur)

    def test_note_task_boundary_in_intent(self) -> None:
        # 真源在 task-intent；编排侧通过 wizard 委托到达
        intent = (ROOT.parent / "task-intent" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("注意任务边界", intent)

    def test_done_is_single_source(self) -> None:
        d = read("references", "done.md")
        self.assertIn("唯一真源", d)
        self.assertIn("观感验收", d)
        self.assertIn("pretty-view-html/references/frontend-design/REFERENCE.md", d)

    def test_wizard_delegates_task_intent(self) -> None:
        w = read("references", "phase-wizard.md")
        self.assertIn("task-intent", w)
        self.assertIn("## 目标", w)
        self.assertIn("## 完成判据", w)
        self.assertIn("## 步骤", w)
        self.assertIn("## 不做", w)

    def test_no_deleted_compat_shells_in_skill(self) -> None:
        skill = read("SKILL.md")
        self.assertNotIn("decide", skill)
        self.assertNotIn("plan-review", skill)
        self.assertNotIn("gate-packs", skill)


if __name__ == "__main__":
    unittest.main()
