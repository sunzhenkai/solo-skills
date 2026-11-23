"""trouble-grill：wiki-data 可选归档与独立落盘契约。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


class WikiDataHandoffContract(unittest.TestCase):
    def test_archive_is_explicit_and_preserves_evidence(self) -> None:
        self.assertIn("用户明确要求把排查结果沉淀到知识 wiki 时", SKILL)
        self.assertIn("`wiki-data` 的 `ingest`", SKILL)
        for field in ("锚点", "证据等级", "用户输入", "dead-end", "验证盲区", "回退条件"):
            self.assertIn(field, SKILL)
        self.assertIn("只有 `confirmed` 可作为根因归档", SKILL)

    def test_default_persistence_remains_independent(self) -> None:
        self.assertIn("未提出归档或没有 `wiki-data` 时", SKILL)
        self.assertIn("仍按上述位置落盘，排查流程不变", SKILL)

    def test_taskrail_persistence_follows_ledger_contract(self) -> None:
        self.assertIn("`evidence/diagnose.md` 追加每轮记录", SKILL)
        self.assertIn("tasks/ongoing/<parent>/subtasks/<child>/", SKILL)
        self.assertIn("写入 `context/current.md` 的结论表", SKILL)
        self.assertIn("`TASK.md` 只保留热状态，由 taskrail 维护", SKILL)
        self.assertIn("本 skill 是 diagnose 环节的排查方法", SKILL)

    def test_anchor_triggers_symptom_lookup_of_known_pitfalls(self) -> None:
        self.assertIn("锚点立好后先查已有的坑：用现象词", SKILL)
        self.assertIn("有 `wiki-data` 时走其 `query` 的执行前预检", SKILL)
        self.assertIn("把它的「最短判别」作为第一个验证动作", SKILL)
        self.assertIn("旧根因在本次验证前按 `guess` 上板", SKILL)
        self.assertIn("未命中就说明已查过", SKILL)

    def test_detour_handoff_to_session_wrap(self) -> None:
        self.assertIn("session-wrap", SKILL)
        self.assertIn("弯路复盘", SKILL)

    def test_description_states_positive_trigger(self) -> None:
        head = SKILL.split("---", 2)[1]
        self.assertIn("多轮或易发散的排查", head)
        self.assertNotIn("不走本流程", head)


if __name__ == "__main__":
    unittest.main()
