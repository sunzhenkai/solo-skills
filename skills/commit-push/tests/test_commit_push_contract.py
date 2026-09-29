"""commit-push 契约：安全协议、规模分流、推送确认门、frontmatter 三件套。"""

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

    def test_description_has_negative_trigger(self) -> None:
        self.assertIn("仅查看变更/diff 或需要逐文件评审时不用本 skill", "\n".join(self.lines))


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


class ScaleRoutingContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_routing_section_exists(self) -> None:
        self.assertIn("## 收集（按规模分流）", self.text)
        self.assertIn("**仅 push**", self.text)
        self.assertIn("**小改动**", self.text)
        self.assertIn("**大改动**", self.text)

    def test_push_only_skips_diff(self) -> None:
        self.assertIn("跳过 diff 收集", self.text)
        self.assertIn("git log @{u}..HEAD --oneline", self.text)

    def test_small_change_single_batch(self) -> None:
        self.assertIn("一条并行批次收齐，不再单独摸规模", self.text)
        self.assertIn("git diff HEAD", self.text)

    def test_large_change_never_full_diff_first(self) -> None:
        self.assertIn("禁止**一上来对整库跑完整 `git diff`", self.text)
        self.assertIn("只对**核心逻辑文件**抽样", self.text)
        self.assertIn("git diff HEAD --stat", self.text)

    def test_do_not_read_generated_or_huge_files(self) -> None:
        self.assertIn("lockfile、生成物、vendor、大 JSON/YAML、资源文件", self.text)
        self.assertIn("**只看路径与是否应纳入提交，不读内容**", self.text)


class StagingContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_path_scoped_add(self) -> None:
        self.assertIn("git add -- <paths>", self.text)
        self.assertIn("git add -A", self.text)

    def test_browser_debug_artifacts_excluded(self) -> None:
        self.assertIn("playwright-report/", self.text)
        self.assertIn("trace.zip", self.text)


class FastPathContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_non_shared_remote_uses_chained_command(self) -> None:
        self.assertIn("**非共享远程且非默认分支**——一条链式命令跑完", self.text)
        self.assertIn("&& git push -u origin HEAD && git status -sb", self.text)

    def test_shared_remote_splits_before_push(self) -> None:
        self.assertIn("**默认分支或共享远程**（生产、预发、共享分支）——拆成两步", self.text)
        self.assertIn("推送前单独向用户确认，确认后再", self.text)


class PushGateContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_shared_remote_push_needs_separate_confirmation(self) -> None:
        self.assertIn("- 目标是共享远程（生产、预发、共享分支）或默认分支：推送前单独向用户确认", self.text)

    def test_push_rejected_never_force(self) -> None:
        self.assertIn("若无上游或被拒绝，说明原因并停下，不要强推", self.text)


if __name__ == "__main__":
    unittest.main()
