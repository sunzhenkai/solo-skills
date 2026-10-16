"""solo-code-review 文本契约测试：校验 SKILL.md 与 references 的门禁、落点与硬闸。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
DELEGATE = (ROOT / "references" / "delegate-mode.md").read_text(encoding="utf-8")
MR = (ROOT / "references" / "mr-mode.md").read_text(encoding="utf-8")


class ScopeConfirmGateTest(unittest.TestCase):
    def test_confirm_gate_table_present(self) -> None:
        self.assertIn("确定审查范围（确认门）", SKILL)
        for rec in ("uncommitted", "default-branch", "ask", "nothing"):
            self.assertIn(f"| `{rec}` |", SKILL)

    def test_mixed_changes_must_ask(self) -> None:
        self.assertIn("**必须**让用户选其一，禁止默默合并两种 diff", SKILL)

    def test_preview_before_llm(self) -> None:
        self.assertIn("仍要先 `ocr review --preview` 展示文件列表再跑 LLM", SKILL)


class CommitModeTest(unittest.TestCase):
    def test_commit_mode_declared(self) -> None:
        self.assertIn("mode=uncommitted|default-branch|commit", SKILL)
        self.assertIn("`-c <hash>`", SKILL)

    def test_change_name_carries_commit(self) -> None:
        self.assertIn("mode=commit 时带 `--commit <hash>`", SKILL)
        self.assertIn("mode=commit 加 `commit`（短 hash）", SKILL)


class DelegateModeTest(unittest.TestCase):
    def test_llm_failure_offers_delegate(self) -> None:
        self.assertIn("`ocr llm test` 失败时停下，让用户在两条路里选一条", SKILL)
        self.assertIn("delegate 模式", SKILL)
        self.assertIn("references/delegate-mode.md", SKILL)

    def test_no_fabricated_key(self) -> None:
        self.assertIn("禁止编造 API key", SKILL)

    def test_delegate_steps_and_schema(self) -> None:
        for cmd in ("ocr delegate preview --format json", "ocr delegate rule --format json"):
            self.assertIn(cmd, DELEGATE)
        for field in ("path", "content", "start_line", "severity", "category"):
            self.assertIn(f"`{field}`", DELEGATE)

    def test_delegate_coverage_mandatory(self) -> None:
        self.assertIn("reviewed 或 skipped（带原因）", DELEGATE)

    def test_delegate_returns_to_main_flow(self) -> None:
        self.assertIn("4. 分级并落盘", DELEGATE)
        self.assertIn("产物落盘、分级、总结打印、MR/PR 评论确认门与主流程完全一致", DELEGATE)


class FetchOnlyTest(unittest.TestCase):
    def test_mr_fetch_only(self) -> None:
        self.assertIn("**只 fetch，不 checkout、不 stash**", MR)
        self.assertIn("refs/code-review/mr-<iid>", MR)
        self.assertIn("refs/code-review/pr-<iid>", MR)
        # SKILL.md 正文保留门禁要点并指向细则
        self.assertIn("references/mr-mode.md", SKILL)
        self.assertIn("不 checkout、不 stash", SKILL)

    def test_no_checkout_in_boundaries(self) -> None:
        self.assertIn("不 `checkout` / `stash` / `reset` 目标仓", SKILL)


class ArtifactTest(unittest.TestCase):
    def test_output_paths(self) -> None:
        self.assertIn("docs/reviews/{YYYY-MM-DD}/{change-name}/", SKILL)
        for name in ("ocr-raw.json", "review.md", "summary.md", "INDEX.md"):
            self.assertIn(name, SKILL)

    def test_native_output_flag(self) -> None:
        self.assertIn("-o /tmp/ocr.json", SKILL)

    def test_summary_only_chat(self) -> None:
        self.assertIn("对话输出 **仅** `write` 返回的 `summary`", SKILL)


class CommentConfirmGateTest(unittest.TestCase):
    def test_remote_write_requires_confirm(self) -> None:
        self.assertIn("MR/PR 评论确认门", SKILL)
        self.assertIn("在用户明确确认前，禁止调用 `glab mr note`、`gh pr comment`", SKILL)

    def test_repo_mode_never_publishes(self) -> None:
        self.assertIn("仓库模式不询问，也不发布评论", SKILL)


class CredentialTest(unittest.TestCase):
    def test_gitlab_token_via_env(self) -> None:
        self.assertIn("GITLAB_TOKEN=\"$GITLAB_TOKEN\" glab", SKILL)
        self.assertIn("token 不写入命令行参数、日志或审查产物", SKILL)
        self.assertIn("禁止编造或输出 token", SKILL)


class OcrFlagsTest(unittest.TestCase):
    def test_core_flags_always(self) -> None:
        self.assertIn("--audience agent --format json --repo <git_root_abs> -o /tmp/ocr.json", SKILL)

    def test_optional_flags_documented(self) -> None:
        for flag in ("--effort", "--exclude", "--max-tokens-budget", "--resume"):
            self.assertIn(flag, SKILL)

    def test_background_file(self) -> None:
        self.assertIn("-B <md路径>", SKILL)

    def test_provider_model_override(self) -> None:
        self.assertIn("[provider=<name>] [model=<name>]", SKILL)
        self.assertIn("--provider <name> --model <name>", SKILL)
        self.assertIn("单次覆盖", SKILL)

    def test_llm_test_only_default_config(self) -> None:
        self.assertIn("只验证**默认配置**", SKILL)
        self.assertIn("ocr llm providers", SKILL)

    def test_llm_recorded_from_ocr_json(self) -> None:
        self.assertIn("llm.{provider,model}", SKILL)

    def test_delegate_no_provider_model(self) -> None:
        self.assertIn("`--provider/--model` 不适用", DELEGATE)


class BoundaryTest(unittest.TestCase):
    def test_scan_out_of_scope(self) -> None:
        self.assertIn("无 diff 的全仓静态扫描直接用 `ocr scan`，不经本 skill", SKILL)

    def test_read_only_default(self) -> None:
        self.assertIn("默认只审查、不改代码", SKILL)
        self.assertIn("用户明确要求「顺手修」才可改代码", SKILL)


class InjectionTest(unittest.TestCase):
    def test_self_evolution_pointer(self) -> None:
        self.assertIn("## 自进化", SKILL)
        self.assertIn("evals/cases.yaml", SKILL)
        self.assertIn("单次失败不直接改本文件", SKILL)


if __name__ == "__main__":
    unittest.main()
