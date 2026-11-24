"""ui-kit 文本契约：入口与边界、模板仓定位、路由、语言分层与保真定义、token 契约真源与白名单、DESIGN.md 模板。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def ref(name: str) -> str:
    return (ROOT / "references" / name).read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    block = text.split("---", 2)[1]
    out = {}
    for line in block.strip().splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


class SkillEntryTest(unittest.TestCase):
    def test_frontmatter(self) -> None:
        fm = frontmatter(SKILL)
        self.assertEqual(fm["id"], "ui-kit")
        self.assertEqual(fm["name"], "ui-kit")
        self.assertLessEqual(len(fm["description"]), 300)
        for word in ("设计语言", "DESIGN.md", "主题", "模板"):
            self.assertIn(word, fm["description"])

    def test_creeds(self) -> None:
        self.assertIn("**外观只在代码里**", SKILL)
        self.assertIn("**模型只写内容**", SKILL)

    def test_boundary_with_pretty_ui(self) -> None:
        self.assertIn("与 pretty-ui 的边界", SKILL)

    def test_default_router_and_named_skill_priority(self) -> None:
        for phrase in ("默认 UI 总入口", "唯一主承接方", "默认入口不等于统一框架", "用户点名具体 skill"):
            self.assertIn(phrase, SKILL)

    def test_one_way_dependency_contract(self) -> None:
        self.assertIn("依赖保持单向", SKILL)
        self.assertIn("独立下游只描述自身契约", SKILL)
        self.assertIn("不反向引用 ui-kit", SKILL)

    def test_general_route_supports_existing_and_non_react(self) -> None:
        for phrase in ("已有项目、非 React", "沿用项目现有框架", "不生成 React 模板文件", "](../pretty-ui/SKILL.md)"):
            self.assertIn(phrase, SKILL)

    def test_template_and_style_package_routes(self) -> None:
        for phrase in ("ui-template.lock.json", "ui-template-apply/SKILL.md", "ui-template-design/SKILL.md", "ui-template-author/SKILL.md", "非模板项目要建设计体系"):
            self.assertIn(phrase, SKILL)

    def test_specialists_and_orchestration_handoff(self) -> None:
        for name in ("baseline-ui", "improve-ui", "fixing-accessibility", "fixing-metadata", "fixing-motion-performance", "component-canvas", "create-canvas", "create-design-md", "frontend-slides", "taskrail", "role-based-reviewer"):
            self.assertIn(f"`{name}`", SKILL)
        self.assertIn("视觉返修回本 skill 分派", SKILL)

    def test_template_repo_located(self) -> None:
        self.assertIn("github.com/sunzhenkai/ui-templates-skill", SKILL)
        self.assertIn("UI_TEMPLATES_DIR", SKILL)
        self.assertIn("按 tag 取用", SKILL)

    def test_routes_point_to_existing_references(self) -> None:
        for link in re.findall(r"\]\((references/[\w.-]+\.md)\)", SKILL):
            self.assertTrue((ROOT / link).is_file(), link)
        for name in ("init.md", "update.md", "migrate.md", "verify.md", "language.md", "tokens.md", "design-md.md"):
            self.assertIn(f"references/{name}", SKILL)

    def test_validation_command_and_done(self) -> None:
        self.assertIn("validate_package.py package", SKILL)
        self.assertIn("validate_package.py project", SKILL)
        self.assertIn("verify_fidelity.py --project", SKILL)
        self.assertIn("完成：validate 0 error，且保真比对 `fidelity: pass`", SKILL)
        self.assertIn("调明度（L），不降门槛", SKILL)

    def test_migration_route(self) -> None:
        self.assertIn("已有 React 项目迁入模板", SKILL)
        self.assertIn("references/migrate.md", SKILL)


class FlowTest(unittest.TestCase):
    def test_init(self) -> None:
        text = ref("init.md")
        self.assertIn("--package quiet-inset --init", text)
        self.assertIn("npx playwright install chromium", text)
        for owner in ("| 项目 | 可改 |", "| 风格包 | 只改白名单", "| 模板 | 不改"):
            self.assertIn(owner, text)
        self.assertIn("页面 = 页面模板 + 数据", text)
        self.assertIn("Zod 解析", text)
        self.assertIn("按 verify.md 跑完整验收", text)

    def test_update(self) -> None:
        text = ref("update.md")
        for state in ("`upstream`", "`local`", "`merge`", "`conflict`", "`new`"):
            self.assertIn(f"| {state} |", text)
        self.assertIn("--upgrade", text)
        self.assertIn("`DROPPED`", text)
        self.assertIn("--resolve", text)
        self.assertIn("按 verify.md 跑完整验收", text)

    def test_migrate(self) -> None:
        text = ref("migrate.md")
        self.assertIn("不要用 `--init`", text)
        for step in ("## 1. 盘点", "## 2. 安装", "## 3. 骨架", "## 4. 页面", "## 5. 适配层", "## 6. 验收", "## 回滚"):
            self.assertIn(step, text)
        self.assertIn("react-router@8", text)
        self.assertIn("proxy[...].bypass", text)
        self.assertIn("local_edits", text)
        self.assertIn("scrollWidth - clientWidth", text)
        self.assertIn("按 [verify.md](verify.md) 全套顺序执行", text)

    def test_verify(self) -> None:
        text = ref("verify.md")
        commands = ["npx tsc -b", "npx eslint .", "validate_package.py project .", "verify_fidelity.py --project .", "npm run build"]
        positions = [text.index(c) for c in commands]
        self.assertEqual(positions, sorted(positions))
        for code in ("J12", "J03", "`fidelity: FAIL`", "J10", "J11", "J13"):
            self.assertIn(code, text)
        self.assertIn("零像素容差", text)
        self.assertIn("白名单内的定制不会失败", text)
        self.assertIn("不要用保真通过代替产品页目检", text)
        self.assertIn("overlays", text)
        self.assertIn("`Esc` 归还", text)
        self.assertNotIn("可忽略", text)
        self.assertIn("每个声明过的状态都是 reviewed", SKILL)


class LanguageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = ref("language.md")

    def test_ownership_layers(self) -> None:
        for layer in ("| token |", "| 基础组件 |", "| blocks |", "| 应用骨架 |", "| 页面模板 |", "| 页面 |"):
            self.assertIn(layer, self.text)
        self.assertIn("lock 哈希校验", self.text)
        self.assertIn("local_edits", self.text)

    def test_surfaces(self) -> None:
        for token in ("`app-shell`", "`background`", "`card`", "`popover`"):
            self.assertIn(token, self.text)
        self.assertIn("阴影只给浮层", self.text)

    def test_selection_is_neutral(self) -> None:
        self.assertIn("选中态用中性灰底", self.text)

    def test_page_patterns(self) -> None:
        for pattern in ("shell", "collection", "detail", "form", "settings", "gallery", "empty", "conversation"):
            self.assertIn(f"| {pattern} |", self.text)

    def test_data_stack(self) -> None:
        self.assertIn("TanStack Query", self.text)
        self.assertIn("Zod 解析", self.text)

    def test_fidelity_definition(self) -> None:
        self.assertIn("**除自定义外视觉一致**", self.text)
        self.assertIn("逐像素一致", self.text)
        self.assertIn("**跨模型稳定**", self.text)
        self.assertIn("pretty-ui/references/guardrails.md", self.text)


class TokensTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text = ref("tokens.md")

    def test_contract_source_of_truth(self) -> None:
        self.assertIn("contract/tokens.json", self.text)
        self.assertIn("和消费这些变量的组件一起发版", self.text)

    def test_fields_documented(self) -> None:
        for field in ("colors.core", "colors.extensions", "scale.required", "scale.optional", "contrast", "tints", "customizable"):
            self.assertIn(f"`{field}`", self.text)

    def test_codes_documented(self) -> None:
        for code in ("T01", "T03", "T04", "T06", "C01", "C02", "J12"):
            self.assertIn(code, self.text)

    def test_whitelist_and_deviation(self) -> None:
        self.assertIn("项目只改 `customizable` 列出的项", self.text)
        self.assertIn("白名单外的改动视为偏离", self.text)
        self.assertIn("`theme_deviations`", self.text)

    def test_new_token_is_template_change(self) -> None:
        self.assertIn("属于模板改动而不是主题改动", self.text)
        self.assertIn("升主版本", self.text)


class DesignMdTest(unittest.TestCase):
    def test_sections(self) -> None:
        text = ref("design-md.md")
        for section in ("## 风格包", "## 自定义（白名单内）", "## 页面与页面模板", "## 偏离", "## 验收记录"):
            self.assertIn(section, text)
        self.assertIn("没跑的写“未验证”", text)


if __name__ == "__main__":
    unittest.main()
