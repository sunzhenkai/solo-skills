"""意图确认：注意任务边界、覆盖清单、goal 清单真源、轻入口。"""
from __future__ import annotations
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class IntentContractTest(unittest.TestCase):
    def test_note_task_boundary(self) -> None:
        intent = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("注意任务边界", intent)

    def test_intent_detail_has_checklist(self) -> None:
        text = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("## 5. 代审（goal）与审查清单", text)
        for s in ("添目标", "漏约束", "自加限制", "形态不符", "该查没查"):
            self.assertIn(s, text)

    def test_cover_fields(self) -> None:
        text = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        for f in ("要干嘛", "怎么干", "输出什么", "上下文", "不做", "我的假设", "我的决定"):
            self.assertIn(f, text)

    def test_points_user_report(self) -> None:
        intent = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("user-report.md", intent)

    def test_skip_rule(self) -> None:
        intent = (ROOT / "references" / "intent.md").read_text(encoding="utf-8")
        self.assertIn("先定做多少", intent)
        self.assertIn("一句话能描述改动", intent)

    def test_light_entry(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("taskrail intent <一句话目标>", skill)
        self.assertIn("只做意图确认", skill)
        self.assertIn("没有任务目录就只在对话里给复述", skill)


if __name__ == "__main__":
    unittest.main()
