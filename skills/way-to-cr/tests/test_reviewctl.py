from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reviewctl.py"


def load_reviewctl():
    spec = importlib.util.spec_from_file_location("reviewctl", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["reviewctl"] = mod
    spec.loader.exec_module(mod)
    return mod


rc = load_reviewctl()


class ReviewctlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "repos").mkdir()

    def _git(self, repo: Path, *args: str) -> str:
        proc = subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)
        return proc.stdout.strip()

    def _init_repo(self, rel: str) -> Path:
        repo = self.tmp / "repos" / rel
        repo.mkdir(parents=True)
        self._git(repo, "init")
        self._git(repo, "config", "user.email", "test@example.invalid")
        self._git(repo, "config", "user.name", "tester")
        (repo / "README").write_text("init\n", encoding="utf-8")
        self._git(repo, "add", ".")
        self._git(repo, "commit", "-m", "init")
        self._git(repo, "branch", "-M", "main")
        return repo

    def test_resolve_by_basename_and_ambiguous(self) -> None:
        self._init_repo("group/service")
        hit = rc.resolve_repo(self.tmp, "service")
        self.assertEqual(hit["basename"], "service")
        self.assertTrue(hit["git_root"].endswith("service"))

        self._init_repo("other/service")
        amb = rc.resolve_repo(self.tmp, "service")
        self.assertTrue(amb.get("ambiguous"))
        self.assertEqual(len(amb["candidates"]), 2)

    def test_inspect_recommends_uncommitted_vs_default_branch(self) -> None:
        repo = self._init_repo("svc")
        (repo / "dirty.txt").write_text("x\n", encoding="utf-8")
        payload = rc.inspect_repo(self.tmp, "svc")
        self.assertEqual(payload["recommendation"], "uncommitted")
        self.assertTrue(payload["needs_confirm"])

        self._git(repo, "add", "dirty.txt")
        self._git(repo, "commit", "-m", "dirty")
        self._git(repo, "checkout", "-b", "feat-x")
        (repo / "feat.txt").write_text("y\n", encoding="utf-8")
        self._git(repo, "add", "feat.txt")
        self._git(repo, "commit", "-m", "feat")
        payload = rc.inspect_repo(self.tmp, "svc")
        self.assertEqual(payload["recommendation"], "default-branch")
        self.assertEqual(payload["ahead_of_default"], 1)

        (repo / "wip.txt").write_text("z\n", encoding="utf-8")
        payload = rc.inspect_repo(self.tmp, "svc")
        self.assertEqual(payload["recommendation"], "ask")

    def test_preview_modes_exclusions_and_guidelines(self) -> None:
        repo = self._init_repo("app")
        (repo / "AGENTS.md").write_text("- Check error handling\n", encoding="utf-8")
        (repo / "src.py").write_text("print(1)\n", encoding="utf-8")
        (repo / "package-lock.json").write_text("{}\n", encoding="utf-8")
        self._git(repo, "add", ".")
        self._git(repo, "commit", "-m", "base files")

        # uncommitted: tracked change + untracked + lockfile + custom exclude
        (repo / "src.py").write_text("print(1)\nprint(2)\n", encoding="utf-8")
        (repo / "new.py").write_text("a = 1\nb = 2\n", encoding="utf-8")
        (repo / "bundle.min.js").write_text("var a=1;", encoding="utf-8")
        (repo / "skip.tmp").write_text("ignored", encoding="utf-8")
        prev = rc.preview_changes(self.tmp, "app", mode="uncommitted", exclude="*.tmp")
        self.assertEqual(prev["guidelines"], ["AGENTS.md"])
        rev_paths = {f["path"] for f in prev["reviewable_files"]}
        exc_map = {f["path"]: f["reason"] for f in prev["excluded_files"]}
        self.assertEqual(rev_paths, {"src.py", "new.py"})
        self.assertEqual(exc_map["bundle.min.js"], "generated")
        self.assertIn("excluded", exc_map["skip.tmp"])

        # commit mode
        self._git(repo, "add", "src.py", "new.py")
        self._git(repo, "commit", "-m", "feat commit")
        sha = self._git(repo, "rev-parse", "--short", "HEAD")
        cprev = rc.preview_changes(self.tmp, "app", mode="commit", commit=sha)
        self.assertEqual(cprev["commit"], sha)
        self.assertEqual({f["path"] for f in cprev["reviewable_files"]}, {"src.py", "new.py"})

        # default-branch / range mode
        self._git(repo, "checkout", "-b", "feat-branch")
        (repo / "branch.py").write_text("x = 42\n", encoding="utf-8")
        self._git(repo, "add", "branch.py")
        self._git(repo, "commit", "-m", "branch work")
        bprev = rc.preview_changes(self.tmp, "app", mode="default-branch")
        self.assertEqual(bprev["from"], "main")
        self.assertEqual(bprev["to"], "HEAD")
        self.assertEqual({f["path"] for f in bprev["reviewable_files"]}, {"branch.py"})

    def test_prefs_get_set_clear_and_reject_sensitive(self) -> None:
        prefs_path = self.tmp / "cfg" / "prefs.json"
        initial = rc.load_prefs(prefs_path)
        self.assertEqual(initial["engines"]["claude"]["model"], "")

        rc.set_prefs(prefs_path, engine="claude", model="sonnet", mode="plugin", set_default_engine=True, persist_default="true")
        rc.set_prefs(prefs_path, engine="codex", model="o3")
        loaded = rc.load_prefs(prefs_path)
        self.assertEqual(loaded["default_engine"], "claude")
        self.assertTrue(loaded["persist_default"])
        self.assertEqual(loaded["engines"]["claude"]["model"], "sonnet")
        self.assertEqual(loaded["engines"]["claude"]["mode"], "plugin")
        self.assertEqual(loaded["engines"]["codex"]["model"], "o3")

        rc.clear_prefs(prefs_path, engine="claude")
        after_clear = rc.load_prefs(prefs_path)
        self.assertEqual(after_clear["engines"]["claude"]["model"], "")
        self.assertEqual(after_clear["default_engine"], "")
        self.assertEqual(after_clear["engines"]["codex"]["model"], "o3")

        with self.assertRaises(rc.ReviewError):
            rc._assert_safe_value("api_key", "secret-123")

    def test_probe_reads_configs_without_leaking_secrets(self) -> None:
        prefs_path = self.tmp / "prefs.json"
        rc.set_prefs(prefs_path, engine="codex", model="gpt-5.2")

        claude_cfg = self.tmp / "claude_settings.json"
        claude_cfg.write_text(
            json.dumps(
                {
                    "model": "claude-sonnet-4-6",
                    "enabledPlugins": ["code-review@anthropic"],
                    "env": {"ANTHROPIC_API_KEY": "sk-ant-do-not-leak"},
                }
            ),
            encoding="utf-8",
        )
        codex_cfg = self.tmp / "codex_config.toml"
        codex_cfg.write_text(
            'model = "o3"\nmodel_provider = "openai"\n\n[profiles.fast]\nmodel = "gpt-5.1-codex"\n',
            encoding="utf-8",
        )

        with mock.patch("shutil.which", return_value=None):
            probed = rc.probe_engines(prefs_path, claude_settings=claude_cfg, codex_config=codex_cfg)

        raw_dump = json.dumps(probed)
        self.assertNotIn("sk-ant-do-not-leak", raw_dump)
        self.assertTrue(probed["engines"]["builtin"]["available"])
        self.assertFalse(probed["engines"]["builtin"]["needs_model_selection"])
        self.assertTrue(probed["engines"]["claude"]["has_code_review_plugin"])
        self.assertIn("claude-sonnet-4-6", probed["engines"]["claude"]["models"])
        self.assertEqual(probed["engines"]["codex"]["saved_model"], "gpt-5.2")
        self.assertTrue(probed["engines"]["codex"]["has_saved_model"])
        self.assertIn("o3", probed["engines"]["codex"]["models"])
        self.assertIn("gpt-5.1-codex", probed["engines"]["codex"]["models"])

    def test_parse_mr_urls(self) -> None:
        gl = rc.parse_mr_url("https://gitlab.example.invalid/group/service/-/merge_requests/88")
        self.assertEqual(gl["kind"], "gitlab")
        self.assertEqual(gl["project"], "group/service")
        self.assertEqual(gl["iid"], 88)
        self.assertEqual(gl["repo_hint"], "service")

        gh = rc.parse_mr_url("https://github.example.invalid/example-org/example-repo/pull/12")
        self.assertEqual(gh["kind"], "github")
        self.assertEqual(gh["project"], "example-org/example-repo")
        self.assertEqual(gh["iid"], 12)

    def test_change_name_and_priority(self) -> None:
        self.assertEqual(
            rc.change_name(repo_basename="service", mode="mr", mr_iid=88, title="Fix timeout"),
            "service-mr-88-fix-timeout",
        )
        self.assertEqual(
            rc.change_name(repo_basename="service", mode="commit", commit="abc1234def"),
            "service-commit-abc1234def",
        )
        self.assertEqual(rc.classify_priority("SQL injection in query builder"), "P0")
        self.assertEqual(rc.classify_priority("nil deref on empty payload"), "P1")
        self.assertEqual(rc.classify_priority("missing test for retry path"), "P2")
        self.assertEqual(rc.classify_priority("rename helper for clarity"), "P3")

    def test_severity_mapping_beats_heuristic(self) -> None:
        comments = rc.normalize_comments(
            {
                "comments": [
                    {"path": "a.go", "content": "rename helper for clarity", "severity": "critical"},
                    {"path": "b.go", "content": "SQL injection in query builder", "severity": "low"},
                    {"path": "c.go", "content": "rename helper for clarity"},
                    {"path": "d.go", "content": "whatever", "priority": "P1", "severity": "low"},
                ]
            }
        )
        by_path = {c["path"]: c["priority"] for c in comments}
        self.assertEqual(by_path["a.go"], "P0")
        self.assertEqual(by_path["b.go"], "P3")
        self.assertEqual(by_path["c.go"], "P3")
        self.assertEqual(by_path["d.go"], "P1")
        self.assertEqual([c["priority"] for c in comments], ["P0", "P1", "P3", "P3"])

    def test_write_review_commit_mode(self) -> None:
        ocr = {
            "engine": "ocr-delegate",
            "status": "complete",
            "session_id": "delegate-20261016-120000",
            "summary": {"files_reviewed": 1, "comments": 1},
            "comments": [
                {"path": "a.go", "content": "SQL injection", "severity": "critical", "start_line": 1, "end_line": 2},
            ],
            "warnings": ["b.go: skipped, binary file"],
        }
        meta = {"repo": "group/service", "mode": "commit", "date": "2026-10-16", "branch": "main", "commit": "abc1234", "default_branch": "main"}
        result = rc.write_review(self.tmp, ocr, meta)
        self.assertEqual(result["change_name"], "service-commit-abc1234")
        review = (self.tmp / result["review"]).read_text(encoding="utf-8")
        self.assertIn("commit: abc1234", review)
        self.assertIn("- Commit：`abc1234`", review)
        self.assertIn("delegate-20261016-120000", review)
        self.assertIn("### P0", review)
        self.assertIn("b.go: skipped, binary file", review)
        self.assertNotIn("- LLM：", review)
        self.assertTrue((self.tmp / result["raw"]).exists())

    def test_write_review_with_plan_and_render_without_disk(self) -> None:
        res = {
            "engine": "codex",
            "status": "complete",
            "session_id": "codex-20261127",
            "llm": {"provider": "codex", "model": "o3"},
            "summary": {"files_reviewed": 2, "comments": 1},
            "comments": [
                {"path": "main.py", "content": "race condition in cache", "priority": "P1", "start_line": 12, "end_line": 18}
            ],
        }
        meta = {
            "repo": "group/service",
            "mode": "uncommitted",
            "date": "2026-11-27",
            "branch": "main",
            "default_branch": "main",
            "guidelines": ["AGENTS.md"],
        }
        rendered = rc.render_result(res, meta, fmt="summary")
        self.assertIn("`codex / o3`", rendered["output"])
        self.assertNotIn("完整文档", rendered["output"])
        self.assertFalse((self.tmp / "docs").exists())

        written = rc.write_review(self.tmp, res, meta, plan_text="# Review Plan\n\n- Focus on concurrency")
        self.assertIn("plan", written)
        self.assertTrue((self.tmp / written["plan"]).is_file())
        review = (self.tmp / written["review"]).read_text(encoding="utf-8")
        self.assertIn("- 引擎：`codex`", review)
        self.assertIn("- LLM：`codex` / `o3`", review)
        self.assertIn("`AGENTS.md`", review)
        index_text = (self.tmp / "docs/reviews/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("| codex |", index_text)

    def test_write_review_records_llm_backend(self) -> None:
        ocr = {
            "status": "complete",
            "session_id": "s1",
            "llm": {"provider": "anthropic", "model": "claude-opus-4-6"},
            "summary": {"files_reviewed": 1, "comments": 0},
            "comments": [],
        }
        meta = {"repo": "group/service", "mode": "default-branch", "date": "2026-10-16", "branch": "feat", "from": "origin/main", "to": "HEAD", "default_branch": "main"}
        result = rc.write_review(self.tmp, ocr, meta)
        review = (self.tmp / result["review"]).read_text(encoding="utf-8")
        self.assertIn("- LLM：`anthropic` / `claude-opus-4-6`", review)

    def test_write_review_sorted_summary(self) -> None:
        ocr = {
            "status": "success",
            "session_id": "abc",
            "summary": {"files_reviewed": 2, "comments": 2, "elapsed": "1s"},
            "comments": [
                {"path": "b.go", "content": "rename helper for clarity", "start_line": 3, "end_line": 3},
                {
                    "path": "a.go",
                    "content": "SQL injection in query builder",
                    "start_line": 10,
                    "end_line": 12,
                    "existing_code": "db.Exec(q)",
                    "suggestion_code": "db.Exec(q, args)",
                    "thinking": "user input concatenated",
                },
            ],
        }
        meta = {
            "repo": "group/service",
            "mode": "default-branch",
            "date": "2026-08-13",
            "change_name": "service-feat-x",
            "branch": "feat-x",
            "from": "origin/main",
            "to": "HEAD",
        }
        result = rc.write_review(self.tmp, ocr, meta)
        review = (self.tmp / result["review"]).read_text(encoding="utf-8")
        self.assertIn("### P0", review)
        self.assertIn("### P3", review)
        self.assertLess(review.index("### P0"), review.index("### P3"))
        summary = result["summary"]
        self.assertIn("P0=1", summary)
        self.assertIn("[P0] SQL injection", summary)
        self.assertTrue(summary.index("### P0") < summary.index("### P3"))
        self.assertTrue((self.tmp / "docs/reviews/INDEX.md").exists())
        printed = rc.render_summary(meta, [], result["review"])
        self.assertIn("No findings.", printed)


if __name__ == "__main__":
    unittest.main()
