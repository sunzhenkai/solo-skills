"""taskflow 核心契约：direct/OpenSpec 共用 worktree，OpenSpec 独占 handoff。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TaskflowContractTest(unittest.TestCase):
    def test_skill_identity_and_size(self) -> None:
        raw = (ROOT / "SKILL.md").read_bytes()
        self.assertLessEqual(len(raw), 8192)
        text = raw.decode("utf-8")
        self.assertRegex(text, r"(?m)^id: taskflow$")
        self.assertRegex(text, r"(?m)^name: taskflow$")

    def test_both_adapters_share_real_git_worktrees(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        worktree = (ROOT / "references" / "worktree.md").read_text(encoding="utf-8")
        self.assertIn("两个执行适配器，一套隔离协议", skill)
        self.assertIn("direct", skill)
        self.assertIn("openspec", skill)
        self.assertIn("prepare_worktree.py", skill)
        self.assertIn("worktrees/<task-id>/<repo-id>/", worktree)
        self.assertIn("git worktree", worktree)
        self.assertIn("task/<task-id>", worktree)

    def test_direct_has_no_driver_or_handoff(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        direct = skill.split("## direct", 1)[1].split("## OpenSpec", 1)[0]
        self.assertIn("不建 driver", skill)
        self.assertIn("不需要 handoff / approve / driver", direct)
        self.assertNotIn("check_handoff.py", direct)

    def test_openspec_has_entry_gate(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("check_handoff.py", skill)
        self.assertIn("gate_bypass", skill)
        self.assertTrue((ROOT / "scripts" / "check_handoff.py").is_file())

    def test_driver_protocol_uses_workspace_and_script(self) -> None:
        template = (ROOT / "references" / "driver-template.md").read_text(encoding="utf-8")
        self.assertIn("## Driver 协议", template)
        self.assertIn("skip_specs: true", template)
        self.assertIn("留给 stock openspec-propose", template)
        self.assertIn("workspace 是唯一 planning root", template)
        self.assertIn("prepare_worktree.py", template)
        self.assertIn("不 push", template)

    def test_default_serial_and_context_bounded_workers(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        workers = (ROOT / "references" / "multi-worker.md").read_text(encoding="utf-8")
        self.assertIn("默认串行", skill)
        self.assertIn("默认串行", workers)
        self.assertIn("不给完整历史、兄弟子任务或无关评审", workers)
        self.assertIn("原始日志留文件", workers)

    def test_self_evolution_out_of_runtime(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("self-evolution.md", skill)
        self.assertNotIn("## Self-evolution", skill)
        self.assertTrue((ROOT / "references" / "self-evolution.md").is_file())

    def test_done_belongs_to_taskrail(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("done.md", skill)
        self.assertIn("不在 taskflow 自行判 done", skill)


if __name__ == "__main__":
    unittest.main()
