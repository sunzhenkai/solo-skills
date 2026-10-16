"""commit-push 契约：安全协议、规模分流、推送确认门、frontmatter 三件套。"""

from __future__ import annotations

import subprocess
import tempfile
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

    def test_description_positive_and_boundary_in_body(self) -> None:
        text = "\n".join(self.lines)
        front = text.split("---", 2)[1]
        self.assertNotIn("不用本 skill", front)
        self.assertIn("只看 diff 或逐文件评审交给 `solo-code-review`", text)


class SafetyProtocolContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")

    def test_safe_default_sentence(self) -> None:
        self.assertIn("## 安全默认", self.text)
        self.assertIn("安全默认：沿用现有 git config 与 hooks；路径级暂存；每次新建 commit；普通 `git push`", self.text)
        self.assertIn("以下情况先确认——用户明确要求才做，并先说明风险", self.text)

    def test_confirm_gates_kept(self) -> None:
        confirm = self.text.split("以下情况先确认", 1)[1].split("\n## ", 1)[0]
        for gate in ("`push --force`", "hard reset", "`main`/`master`", "`commit --amend`",
                     "`--no-verify`", "修改 git config", "`.env`、`credentials.json`"):
            self.assertIn(gate, confirm)

    def test_amend_conditions_and_hook_failure(self) -> None:
        self.assertIn("HEAD 由你在本会话创建、尚未 push、amend 非因 hook 失败", self.text)
        self.assertIn("hook 失败时修好问题后 **新建** commit", self.text)


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
        self.assertIn("从统计入手、按路径抽样", self.text)
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
        self.assertIn("若无上游或被拒绝，说明原因并停下，等用户决定", self.text)



class ConflictFlowContract(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL_MD.read_text(encoding="utf-8")
        self.ref = (SKILL_ROOT / "references" / "conflicts.md").read_text(encoding="utf-8")

    def test_conflict_section_points_one_level(self) -> None:
        self.assertIn("## 处理冲突", self.text)
        self.assertIn("](references/conflicts.md)", self.text)

    def test_conflict_types_are_routed(self) -> None:
        for kind in ("**追加型**", "**语义型**", "**危险型**"):
            self.assertIn(kind, self.text)
            self.assertIn(kind, self.ref)

    def test_conflict_inventory_uses_script(self) -> None:
        self.assertIn("scripts/commit_push_context.sh --conflicts", self.ref)

    def test_conflict_verification_steps(self) -> None:
        for s in ("git ls-files -u", "git diff --check"):
            self.assertIn(s, self.text)
            self.assertIn(s, self.ref)

    def test_conflict_does_not_bypass_push_gate(self) -> None:
        self.assertIn("冲突处理不会自动获得推送授权", self.text)


class ContextScriptContract(unittest.TestCase):
    def setUp(self) -> None:
        self.script = SKILL_ROOT / "scripts" / "commit_push_context.sh"

    def test_script_help(self) -> None:
        result = subprocess.run(
            ["bash", str(self.script), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Usage:", result.stdout)

    def test_summary_on_clean_repo(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", "-b", "main", d], check=True)
            subprocess.run(["git", "-C", d, "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", d, "config", "user.name", "Test"], check=True)
            Path(d, "a.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", d, "add", "a.txt"], check=True)
            subprocess.run(["git", "-C", d, "commit", "-q", "-m", "base"], check=True)

            result = subprocess.run(
                ["bash", str(self.script), "--summary"],
                cwd=d,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("branch: main", result.stdout)
            self.assertIn("changes: staged=0 unstaged=0 untracked=0 conflicts=0", result.stdout)

    def test_conflict_map_on_merge(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", "-b", "main", d], check=True)
            subprocess.run(["git", "-C", d, "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", d, "config", "user.name", "Test"], check=True)
            Path(d, "a.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", d, "add", "a.txt"], check=True)
            subprocess.run(["git", "-C", d, "commit", "-q", "-m", "base"], check=True)

            subprocess.run(["git", "-C", d, "checkout", "-q", "-b", "side"], check=True)
            Path(d, "a.txt").write_text("side\n", encoding="utf-8")
            subprocess.run(["git", "-C", d, "commit", "-q", "-am", "side"], check=True)

            subprocess.run(["git", "-C", d, "checkout", "-q", "main"], check=True)
            Path(d, "a.txt").write_text("main\n", encoding="utf-8")
            subprocess.run(["git", "-C", d, "commit", "-q", "-am", "main"], check=True)

            merge = subprocess.run(
                ["git", "-C", d, "merge", "--no-edit", "side"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(merge.returncode, 0)

            result = subprocess.run(
                ["bash", str(self.script), "--conflicts"],
                cwd=d,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("operation: merge", result.stdout)
            self.assertIn("file: a.txt", result.stdout)
            self.assertIn("conflicts: 1", result.stdout)



if __name__ == "__main__":
    unittest.main()
