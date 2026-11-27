"""way-to-cr 文本契约测试：校验 SKILL.md 与 5 个 references 的流程、多引擎、模型记忆与硬闸。"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
BUILTIN = (ROOT / "references" / "builtin-review.md").read_text(encoding="utf-8")
EXTERNAL = (ROOT / "references" / "external-agents.md").read_text(encoding="utf-8")
OCR = (ROOT / "references" / "ocr-mode.md").read_text(encoding="utf-8")
DELEGATE = (ROOT / "references" / "delegate-mode.md").read_text(encoding="utf-8")
MR = (ROOT / "references" / "mr-mode.md").read_text(encoding="utf-8")


class DescriptionAndSizeTest(unittest.TestCase):
    def test_frontmatter_and_alias(self) -> None:
        head = SKILL.split("---", 2)[1]
        self.assertIn("id: way-to-cr", head)
        self.assertIn("name: way-to-cr", head)
        self.assertIn("原 solo-code-review", head)
        self.assertIn("P0~P3", head)
        self.assertNotIn("docs/reviews", head)

    def test_skill_under_8kb_and_direct_links(self) -> None:
        self.assertLessEqual(len(SKILL.encode("utf-8")), 7800)
        for rel in (
            "references/builtin-review.md",
            "references/external-agents.md",
            "references/ocr-mode.md",
            "references/delegate-mode.md",
            "references/mr-mode.md",
        ):
            self.assertIn(rel, SKILL)
            self.assertTrue((ROOT / rel).is_file(), rel)


class FourStepFlowTest(unittest.TestCase):
    def test_four_steps_present(self) -> None:
        self.assertIn("### 1. 思考审查内容与范围（范围确认门）", SKILL)
        self.assertIn("### 2. 选择 Review 方案（方案确认门）", SKILL)
        self.assertIn("### 3. 模型选择与记忆复用 + 执行审查", SKILL)
        self.assertIn("### 4. 分级出报告、可选落盘与可选发布 MR/PR", SKILL)

    def test_confirm_gate_table_and_preview(self) -> None:
        for rec in ("uncommitted", "default-branch", "ask", "nothing"):
            self.assertIn(f"| `{rec}` |", SKILL)
        self.assertIn("必须让用户二选一，禁止默默合并两种 diff", SKILL)
        self.assertIn("reviewctl preview", SKILL)

    def test_four_engines_in_step2(self) -> None:
        self.assertIn("reviewctl probe", SKILL)
        for eng in ("builtin", "claude", "codex", "ocr"):
            self.assertIn(f"| `{eng}` |", SKILL)


class ModelMemoryTest(unittest.TestCase):
    def test_model_selection_and_reuse_rules(self) -> None:
        self.assertIn("仅 `claude`、`codex`、`ocr`（原生 `review`）需要选定模型", SKILL)
        self.assertIn("prefs.json", SKILL)
        self.assertIn("严禁写入 key/token", SKILL)
        self.assertIn("reviewctl prefs set", SKILL)
        self.assertIn("自动复用已记住模型", SKILL)
        self.assertIn("换模型", SKILL)


class BuiltinAndExternalAgentsTest(unittest.TestCase):
    def test_builtin_covers_guidelines_and_checklist(self) -> None:
        self.assertIn("AGENTS.md", BUILTIN)
        self.assertIn("干净会话", BUILTIN)
        self.assertIn("七维审查清单", BUILTIN)
        self.assertIn('"engine": "builtin"', BUILTIN)

    def test_external_agents_claude_and_codex(self) -> None:
        self.assertIn("claude --model <model> -p", EXTERNAL)
        self.assertIn("/code-review", EXTERNAL)
        self.assertIn("codex review --uncommitted", EXTERNAL)
        self.assertIn("codex review --base", EXTERNAL)
        self.assertIn("codex review --commit", EXTERNAL)
        self.assertIn("codex exec --sandbox read-only", EXTERNAL)


class OcrAndDelegateTest(unittest.TestCase):
    def test_ocr_flags_and_failure_options(self) -> None:
        self.assertIn("ocr review --audience agent --format json --repo <git_root_abs> -o /tmp/ocr.json", OCR)
        for flag in ("--effort", "--exclude", "--max-tokens-budget", "--resume", "--provider", "--model"):
            self.assertIn(flag, OCR)
        self.assertIn("`ocr llm test` 失败时停下", OCR)
        self.assertIn("ocr llm providers", OCR)

    def test_delegate_steps_and_schema(self) -> None:
        for cmd in ("ocr delegate preview --format json", "ocr delegate rule --format json"):
            self.assertIn(cmd, DELEGATE)
        for field in ("path", "content", "start_line", "severity", "category"):
            self.assertIn(f"`{field}`", DELEGATE)
        self.assertIn("reviewed 或 skipped（带原因）", DELEGATE)
        self.assertIn("`--provider/--model` 不适用", DELEGATE)


class FetchOnlyAndArtifactTest(unittest.TestCase):
    def test_mr_fetch_only(self) -> None:
        self.assertIn("**只 fetch，不 checkout、不 stash**", MR)
        self.assertIn("refs/code-review/mr-<iid>", MR)
        self.assertIn("refs/code-review/pr-<iid>", MR)
        self.assertIn("不执行 `checkout` / `stash` / `reset`", SKILL)

    def test_optional_artifacts_and_summary_only(self) -> None:
        self.assertIn("docs/reviews/{YYYY-MM-DD}/{change-name}/", SKILL)
        for name in ("raw.json", "review.md", "summary.md", "plan.md", "INDEX.md"):
            self.assertIn(name, SKILL)
        self.assertIn("reviewctl render", SKILL)
        self.assertIn("仅输出 `reviewctl render` / `write` 返回的 `summary`", SKILL)

    def test_remote_write_and_credentials(self) -> None:
        self.assertIn("MR/PR 评论确认门", SKILL)
        self.assertIn("`glab mr note` / `gh pr comment`", SKILL)
        self.assertIn('GITLAB_TOKEN="$GITLAB_TOKEN" glab', SKILL)
        self.assertIn("严禁编造凭据", SKILL)


class BoundaryAndEvolutionTest(unittest.TestCase):
    def test_boundaries_and_self_evolution(self) -> None:
        self.assertIn("无 diff 的全仓静态扫描直接用 `ocr scan`", SKILL)
        self.assertIn("默认只审查、不改代码", SKILL)
        self.assertIn("交给 `role-based-reviewer`", SKILL)
        self.assertIn("evals/cases.yaml", SKILL)
        self.assertIn("skill-upgrader", SKILL)

    def test_optional_post_cr_fix_prompt(self) -> None:
        self.assertIn("修复提示（可选）", SKILL)
        self.assertIn("无 findings 时省略", SKILL)
        self.assertIn("确认修复范围后再改代码", SKILL)
        self.assertIn("way-to-fix", SKILL)


if __name__ == "__main__":
    unittest.main()
