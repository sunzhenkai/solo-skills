"""task* 族跨 skill 契约：载荷归属、真源、相对链接可达。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
TASK_SKILLS = (
    "taskrail",
    "task-confirm",
    "task-explore",
    "taskflow",
)
SKIP_DIRS = {"patches", "evolutions", "experience", "tests", "evals", "examples"}


def read(skill: str, rel: str) -> str:
    return (SKILLS_ROOT / skill / rel).read_text(encoding="utf-8")


def live_texts() -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for skill in TASK_SKILLS:
        for path in sorted((SKILLS_ROOT / skill).rglob("*.md")):
            if any(p in SKIP_DIRS for p in path.relative_to(SKILLS_ROOT / skill).parts):
                continue
            out.append(
                (str(path.relative_to(SKILLS_ROOT.parent)), path.read_text(encoding="utf-8"))
            )
    return out


class TestPayloadOwners(unittest.TestCase):
    def test_wizard_phase_provides_criterion(self) -> None:
        self.assertIn("## 完成判据", read("taskrail", "references/phase-wizard.md"))

    def test_confirm_owns_profile(self) -> None:
        self.assertIn("质量画像", read("task-confirm", "SKILL.md"))
        self.assertIn("角色底线", read("task-confirm", "references/quality-profile.md"))

    def test_no_stale_wizard_profile_attribution(self) -> None:
        stale = ("由 task-wizard 复杂档产出", "上游 task-wizard 复杂档")
        for path, text in live_texts():
            for s in stale:
                self.assertNotIn(s, text, f"{path} 仍把质量画像归给 task-wizard")


class TestFailureCountingSingleSource(unittest.TestCase):
    def test_confirm_defines_thresholds(self) -> None:
        confirm = read("task-confirm", "SKILL.md")
        self.assertIn("同一验证连败两次", confirm)
        self.assertIn("累计假设达 3", confirm)


class TestNoDeletedSkillIdsInLiveDocs(unittest.TestCase):
    """生产稿（非 patches/evolutions）不得再引用已删除 skill id 作路径。"""

    DELETED = ("task-wizard/", "task-goal/", "task-delivery/")

    def test_no_path_refs_to_deleted_skills(self) -> None:
        hits: list[str] = []
        for path, text in live_texts():
            for d in self.DELETED:
                if d in text:
                    hits.append(f"{path} contains {d}")
        self.assertEqual(hits, [], "live docs still reference deleted skill paths")


class TestFamilyLinksResolve(unittest.TestCase):
    def test_all_relative_links_reachable(self) -> None:
        broken: list[str] = []
        for skill in TASK_SKILLS:
            for path in sorted((SKILLS_ROOT / skill).rglob("*.md")):
                if any(p in SKIP_DIRS for p in path.relative_to(SKILLS_ROOT / skill).parts):
                    continue
                text = path.read_text(encoding="utf-8")
                for m in re.finditer(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", text):
                    target = m.group(1)
                    if target.startswith(("http://", "https://")):
                        continue
                    if not (path.parent / target).resolve().is_file():
                        broken.append(f"{path.relative_to(SKILLS_ROOT.parent)} -> {target}")
        self.assertEqual(broken, [], "存在不可达的相对链接")


class TestFamilyComplete(unittest.TestCase):
    def test_all_task_skills_present(self) -> None:
        missing = [s for s in TASK_SKILLS if not (SKILLS_ROOT / s / "SKILL.md").is_file()]
        self.assertEqual(missing, [])

    def test_deleted_skills_gone(self) -> None:
        for s in ("task-wizard", "task-goal", "task-delivery"):
            self.assertFalse(
                (SKILLS_ROOT / s / "SKILL.md").is_file(), f"{s} should be deleted"
            )

    def test_spine_and_confirm(self) -> None:
        self.assertIn("唯一编排入口", read("taskrail", "SKILL.md"))
        self.assertIn("| human |", read("task-confirm", "SKILL.md"))
        self.assertTrue(
            (SKILLS_ROOT / "task-confirm" / "references" / "suspension.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
