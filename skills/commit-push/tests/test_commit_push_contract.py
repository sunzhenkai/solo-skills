"""commit-push 契约：安全协议、耗时分流、推送确认门、frontmatter 三件套。"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"


class FrontmatterContract(unittest.TestCase):
    def setUp(self) -> None:
        self.lines = SKILL_MD.read_text(encoding="utf-8").splitlines()

    def test_three_fields_present_and_id_matches_dir(self) -> None:
        frontmatter = "\n".join(self.lines[:6])
        self.assertIn("id: commit-push", frontmatter)
        self.assertIn("name: commit-push", frontmatter)
        self.assertIn("description:", frontmatter)


class SafetyProtocolContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_never_touch_git_config(self) -> None:
        self.assertIn("- **不要** 修改 git config", self.text)

    def test_never_skip_hooks(self) -> None:
        self.assertIn("**不要** 跳过 hooks（`--no-verify` 等）", self.text)

    def test_never_force_push_default_branch(self) -> None:
        self.assertIn("**不要** force push 到 `main`/`master`；若用户要求则警告", self.text)

    def test_hook_failure_creates_new_commit_not_amend(self) -> None:
        self.assertIn("hook 失败：修问题后 **新建** commit，不要 amend", self.text)
        self.assertIn("**避免** `commit --amend`", self.text)

    def test_secret_like_files_not_committed(self) -> None:
        self.assertIn("疑似密钥文件（`.env`、`credentials.json` 等）不要提交", self.text)

    def test_destructive_commands_require_explicit_request(self) -> None:
        self.assertIn("**不要** 用破坏性命令（`push --force`、hard reset 等），除非用户明确要求", self.text)


class LargeChangeContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_stat_first_never_full_diff(self) -> None:
        self.assertIn("## 耗时优化（大改动必读）", self.text)
        self.assertIn("禁止** 一上来对整库跑完整 `git diff`", self.text)
        self.assertIn("**先摸规模**", self.text)
        self.assertIn("**按规模分流**", self.text)
        self.assertIn("只对 **核心逻辑文件** 抽样", self.text)

    def test_do_not_read_generated_or_huge_files(self) -> None:
        self.assertIn("lockfile、生成物、vendor、大 JSON/YAML、资源文件", self.text)


class PushGateContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_shared_remote_push_needs_separate_confirmation(self) -> None:
        self.assertIn("- 目标是共享远程（生产、预发、共享分支）或默认分支：推送前单独向用户确认", self.text)

    def test_push_rejected_never_force(self) -> None:
        self.assertIn("若无上游或被拒绝，说明原因并停下，不要强推", self.text)

    def test_description_has_negative_trigger(self) -> None:
        self.assertIn("仅查看变更/diff 或需要逐文件评审时不用本 skill", self.text)


if __name__ == "__main__":
    unittest.main()
