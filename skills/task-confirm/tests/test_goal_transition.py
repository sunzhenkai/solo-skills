"""goal_transition.py 的单元测试：网格解析、迁移判定、state-file 读写、event-tag 映射、事件推断。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import goal_transition as gt  # noqa: E402


class TestGridParsing(unittest.TestCase):
    def setUp(self) -> None:
        text = (gt.SKILL_ROOT / "references" / "legacy" / "state-machine.md").read_text(encoding="utf-8")
        self.grid = gt._parse_grid(text)

    def test_four_states_present(self) -> None:
        for st in gt.STATES:
            self.assertIn(st, self.grid)

    def test_stopped_row_has_11_events(self) -> None:
        self.assertEqual(len(self.grid["已停"]), 11)

    def test_event_names_match_enum(self) -> None:
        for ev in gt.EVENTS:
            self.assertIn(ev, self.grid["已停"])


class TestDecide(unittest.TestCase):
    def test_stopped_user_auth(self) -> None:
        out = gt.decide("已停", "用户授权", None)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "执行中")

    def test_stopped_user_continue(self) -> None:
        out = gt.decide("已停", "用户继续", None)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "已停")
        self.assertIn("重申", out["action"])

    def test_stopped_autocontinue_first(self) -> None:
        out = gt.decide("已停", "goal 自动续跑", 1)
        self.assertTrue(out["defined"])
        self.assertNotIn("blocked", out["action"])

    def test_stopped_autocontinue_third_blocks(self) -> None:
        out = gt.decide("已停", "goal 自动续跑", 3)
        self.assertTrue(out["defined"])
        self.assertIn("blocked", out["action"])

    def test_stopped_autocontinue_beyond_third_still_blocked(self) -> None:
        out = gt.decide("已停", "goal 自动续跑", 5)
        self.assertTrue(out["defined"])
        self.assertIn("blocked", out["action"])

    def test_stopped_autocontinue_requires_count(self) -> None:
        out = gt.decide("已停", "goal 自动续跑", None)
        self.assertFalse(out["defined"])

    def test_running_review_converged(self) -> None:
        out = gt.decide("执行中", "审阅收敛", None)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "已交接")

    def test_running_criterion_met(self) -> None:
        out = gt.decide("执行中", "判据成立", None)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "已完成")

    def test_handsoff_step_progress(self) -> None:
        out = gt.decide("已交接", "步骤推进", None)
        self.assertTrue(out["defined"])
        self.assertEqual(out["next_state"], "已交接")

    def test_undefined_combo_returns_none(self) -> None:
        out = gt.decide("已停", "判据成立", None)
        self.assertFalse(out["defined"])
        self.assertIsNone(out["next_state"])

    def test_unknown_event_rejected(self) -> None:
        out = gt.decide("已停", "天气不错", None)
        self.assertFalse(out["defined"])

    def test_unknown_state_rejected(self) -> None:
        out = gt.decide("摸鱼中", "用户授权", None)
        self.assertFalse(out["defined"])

    def test_event_substring_match(self) -> None:
        out = gt.decide("已停", "自动续跑", 1)
        self.assertTrue(out["defined"])
        self.assertEqual(out["event"], "goal 自动续跑")


class TestStateFileIO(unittest.TestCase):
    def test_write_then_read_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停",
                "exit_point": "降级未确认",
                "autocontinue_count": 2,
                "last_input_event": "goal 自动续跑",
                "blocked": False,
                "handoff_summary": None,
            })
            data = gt.read_state_file(p)
            self.assertEqual(data["state"], "已停")
            self.assertEqual(data["exit_point"], "降级未确认")
            self.assertEqual(data["autocontinue_count"], 2)
            self.assertEqual(data["last_input_event"], "goal 自动续跑")
            self.assertFalse(data["blocked"])
            self.assertIsNone(data["handoff_summary"])

    def test_read_missing_file_returns_empty(self) -> None:
        data = gt.read_state_file(Path("/tmp/definitely-not-exist-goal-state.yaml"))
        self.assertEqual(data, {})

    def test_read_ignores_unknown_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "s.yaml"
            p.write_text("state: 已停\nunknown_key: ignore-me\nautocontinue_count: 1\n", encoding="utf-8")
            data = gt.read_state_file(p)
            self.assertNotIn("unknown_key", data)
            self.assertEqual(data["state"], "已停")
            self.assertEqual(data["autocontinue_count"], 1)

    def test_write_skips_missing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "s.yaml"
            gt.write_state_file(p, {"state": "执行中", "autocontinue_count": 0})
            text = p.read_text(encoding="utf-8")
            self.assertIn("state: 执行中", text)
            self.assertNotIn("exit_point:", text)


class TestCLIWithStateFile(unittest.TestCase):
    def _run(self, *args: str) -> tuple[int, dict]:
        script = Path(__file__).resolve().parents[1] / "scripts" / "goal_transition.py"
        proc = subprocess.run(
            ["python3", str(script), *args],
            capture_output=True, text=True, timeout=10,
        )
        try:
            out = json.loads(proc.stdout)
        except json.JSONDecodeError:
            self.fail(f"not JSON: stdout={proc.stdout!r} stderr={proc.stderr!r}")
        return proc.returncode, out

    def test_state_file_drives_state_and_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停",
                "exit_point": "降级未确认",
                "autocontinue_count": 2,
                "last_input_event": "goal 自动续跑",
                "blocked": False,
            })
            code, out = self._run("--state-file", str(p), "--event", "goal 自动续跑")
            self.assertEqual(code, 0)
            self.assertTrue(out["defined"])
            # count=2 from file → 这次相当于第 3 次自动续跑 → blocked
            self.assertIn("blocked", out["action"])

    def test_write_back_increments_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停", "exit_point": "降级未确认",
                "autocontinue_count": 0, "blocked": False,
            })
            code, out = self._run("--state-file", str(p), "--event", "goal 自动续跑", "--write")
            self.assertEqual(code, 0)
            self.assertTrue(out["wrote_back"])
            data = gt.read_state_file(p)
            self.assertEqual(data["autocontinue_count"], 1)
            self.assertEqual(data["last_input_event"], "goal 自动续跑")

    def test_write_back_third_time_marks_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停", "exit_point": "降级未确认",
                "autocontinue_count": 2, "blocked": False,
            })
            code, out = self._run("--state-file", str(p), "--event", "goal 自动续跑", "--write")
            self.assertEqual(code, 0)
            self.assertIn("blocked", out["action"])
            data = gt.read_state_file(p)
            self.assertTrue(data["blocked"])
            self.assertEqual(data["state"], "已停")

    def test_event_tag_auto_continue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停", "exit_point": "x",
                "autocontinue_count": 0, "blocked": False,
            })
            code, out = self._run("--state-file", str(p), "--event-tag", "auto-continue")
            self.assertEqual(code, 0)
            self.assertEqual(out["event"], "goal 自动续跑")

    def test_unknown_event_tag_errors(self) -> None:
        script = Path(__file__).resolve().parents[1] / "scripts" / "goal_transition.py"
        proc = subprocess.run(
            ["python3", str(script), "--state", "已停", "--event-tag", "nope"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("未知 event-tag", proc.stderr)

    def test_non_autocontinue_event_resets_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "goal-state.yaml"
            gt.write_state_file(p, {
                "state": "已停", "exit_point": "x",
                "autocontinue_count": 2, "blocked": False,
            })
            code, out = self._run("--state-file", str(p), "--event", "用户授权", "--write")
            self.assertEqual(code, 0)
            data = gt.read_state_file(p)
            self.assertEqual(data["autocontinue_count"], 0)


class TestEventInferenceTable(unittest.TestCase):
    """references/legacy/state-file.md 必须含「事件推断顺序」与关键条目。"""

    def setUp(self) -> None:
        self.text = (Path(__file__).resolve().parents[1] / "references" / "legacy" / "state-file.md").read_text(encoding="utf-8")

    def test_inference_section_present(self) -> None:
        self.assertIn("## 事件推断顺序", self.text)

    def test_inference_entries(self) -> None:
        for phrase in (
            "逐字相同",
            "用户授权",
            "用户继续",
            "用户改向",
            "用户补充信息",
            "无进展轮",
        ):
            self.assertIn(phrase, self.text)

    def test_producer_tag_section(self) -> None:
        self.assertIn("goal-event:", self.text)
        self.assertIn("auto-continue", self.text)


if __name__ == "__main__":
    unittest.main()
