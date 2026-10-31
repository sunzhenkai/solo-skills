"""pretty-ui 文本契约：路由、信条、说决定、看图分档、单一停止标准、问题字段、中文排版数值、阅读页模板与落盘、来源许可。"""

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
        self.assertEqual(fm["id"], "pretty-ui")
        self.assertEqual(fm["name"], "pretty-ui")
        self.assertLessEqual(len(fm["description"]), 300)
        for word in ("设计方向", "设计体系", "截图", "评审", "阅读页"):
            self.assertIn(word, fm["description"])

    def test_three_creeds(self) -> None:
        for creed in ("地板靠规则", "天花板靠方向", "以画面为准"):
            self.assertIn(creed, SKILL)

    def test_routing_modes(self) -> None:
        for mode in ("| 小改 |", "| build |", "| refine |", "| review |", "| system |", "| page |"):
            self.assertIn(mode, SKILL)
        self.assertIn("只读，不改文件", SKILL)
        self.assertIn("system 再 build", SKILL)
        self.assertIn("工程化检查", SKILL)
        self.assertIn("references/engineering.md", SKILL)
        self.assertIn("脚手架先 project-init", SKILL)

    def test_direction_decided_not_asked(self) -> None:
        self.assertIn("自选一个方向，写方向卡和理由，直接说决定、接着做", SKILL)
        self.assertIn("用户点名要多个方案时才出三个候选", SKILL)
        self.assertIn("| build 轻量 |", SKILL)

    def test_confirm_modes(self) -> None:
        self.assertIn("**goal 模式或无人值守**：不停下等确认", SKILL)
        self.assertIn("对照参照页看改前改后截图", SKILL)
        self.assertIn("**human 模式**", SKILL)
        self.assertIn("用户说可以才算完成", SKILL)

    def test_light_card_in_skill(self) -> None:
        self.assertIn("## 轻量方向卡", SKILL)
        self.assertIn("写清取它哪一点", SKILL)

    def test_steps_have_done_criteria(self) -> None:
        flow = SKILL.split("## build 主流程", 1)[1].split("## 轻量方向卡", 1)[0]
        self.assertGreaterEqual(flow.count("完成："), 6)
        self.assertIn("critique.md「迭代与停止」，那一节是唯一标准", flow)

    def test_size_budget(self) -> None:
        self.assertLess(len(SKILL.encode("utf-8")), 8192)

    def test_evolution_pointer_only(self) -> None:
        self.assertIn("经验沉淀与正文演进走 `skill-upgrader`", SKILL)
        self.assertNotIn("cases.yaml", SKILL)

    def test_render_gate(self) -> None:
        self.assertIn("1280", SKILL)
        self.assertIn("375", SKILL)
        self.assertIn("未渲染验证", SKILL)
        self.assertIn("code-only", SKILL)
        self.assertIn("scripts/check_page.py", SKILL)

    def test_ten_laws_numbers(self) -> None:
        for phrase in ("每屏一个主角", "先灰度后上色", "取值来自刻度", "组外距离大于组内", "既有体系优先"):
            self.assertIn(phrase, SKILL)
        self.assertIn("30–40 字（上限 46）", SKILL)
        self.assertIn("16–18px", SKILL)
        self.assertIn("4.5:1", SKILL)

    def test_linked_files_exist(self) -> None:
        links = re.findall(r"\]\(([^)#]+)\)", SKILL)
        self.assertTrue(links)
        for link in links:
            self.assertTrue((ROOT / link).exists(), link)
        for name in ("direction.md", "system.md", "engineering.md", "evidence.md", "rules.md", "critique.md", "page.md"):
            self.assertIn(f"references/{name}", SKILL)
        self.assertIn("assets/reading-page.html", SKILL)

    def test_runtime_artifacts_outside_skill(self) -> None:
        self.assertIn("本 skill 目录保持只读", SKILL)


class DirectionTest(unittest.TestCase):
    TEXT = ref("direction.md")

    def test_card_fields(self) -> None:
        for field in ("北极星", "调性", "标杆与取舍", "生成引擎", "首屏骨架", "字体", "色彩", "主视觉", "控件语法", "动效", "记忆点", "放弃什么"):
            self.assertIn(f"| {field} |", self.TEXT)

    def test_benchmarks_from_real_screens(self) -> None:
        self.assertIn("未看图，凭记忆", self.TEXT)
        self.assertIn("取到 1 家标杆的首屏截图", self.TEXT)
        self.assertIn("品类不清或用户点名多个方向时再取第 2 家", self.TEXT)
        self.assertIn("一次搜索和一次打开仍未拿到画面", self.TEXT)
        self.assertIn("隔离评审的参照集", self.TEXT)
        for word in ("基线", "套路", "撞脸"):
            self.assertIn(word, self.TEXT)

    def test_difference_check(self) -> None:
        self.assertIn("四项至多一项相同", self.TEXT)
        self.assertIn("至少一个打破品类套路", self.TEXT)
        self.assertIn("两遍法", self.TEXT)
        self.assertIn("### 出多个候选时", self.TEXT)
        self.assertIn("## 8. 说决定", self.TEXT)

    def test_light_card_points_to_skill(self) -> None:
        self.assertIn("轻量方向卡", self.TEXT)
        self.assertIn("[SKILL.md](../SKILL.md)「轻量方向卡」", self.TEXT)


class SystemTest(unittest.TestCase):
    TEXT = ref("system.md")

    def test_scripts_and_outputs(self) -> None:
        for word in ("scripts/palette.py", "scripts/contrast.py", "tokens.css", "DESIGN.md", "preview.html"):
            self.assertIn(word, self.TEXT)

    def test_two_layer_tokens(self) -> None:
        self.assertIn("两层 token", self.TEXT)
        for token in ("--surface", "--text-muted", "--action", "--danger"):
            self.assertIn(token, self.TEXT)

    def test_existing_system_first(self) -> None:
        self.assertIn("已有的部分原样沿用", self.TEXT)
        self.assertIn("ui-delivery.md", self.TEXT)

    def test_decides_missing_items(self) -> None:
        self.assertIn("## 2. 缺项自定", self.TEXT)
        self.assertIn("用陈述句写下决定与理由", self.TEXT)
        self.assertIn("assets/reading-page.html", self.TEXT)


class EngineeringTest(unittest.TestCase):
    TEXT = ref("engineering.md")

    def test_branches_and_boundary(self) -> None:
        for phrase in ("`init`", "`audit`", "只读产品代码、依赖与配置", "project-init", "不新增依赖"):
            self.assertIn(phrase, self.TEXT)

    def test_token_and_component_checks(self) -> None:
        for phrase in ("组件消费语义 token", "刻意差异", "一次性结构", "API / 变体", "可达性", "保留 / 合并 / 扩展 / 退役"):
            self.assertIn(phrase, self.TEXT)

    def test_audit_and_migration(self) -> None:
        for phrase in ("UI_AUDIT.md", "文件与行号", "使用次数", "代表页面", "清理旧实现", "批次与风险"):
            self.assertIn(phrase, self.TEXT)

    def test_native_verification_and_done(self) -> None:
        for phrase in ("typecheck、lint、test、build", "scripts/contrast.py", "scripts/check_page.py", "evidence.md", "audit` 完成只要求报告"):
            self.assertIn(phrase, self.TEXT)


class RulesTest(unittest.TestCase):
    TEXT = ref("rules.md")

    def test_sweep_order_and_lenses(self) -> None:
        self.assertIn("H 层级 → S 间距与布局 → T 排版 → C 色彩 → D 深度 → I 图像与图标 → F 收尾与状态 → M 动效", self.TEXT)
        for rule in ("**H1**", "**S3**", "**T2**", "**C4**", "**C5**", "**D2**", "**I2**", "**I6**", "**F4**", "**M4**", "**X1**", "**X12**"):
            self.assertIn(rule, self.TEXT)

    def test_severity_mapping(self) -> None:
        for row in ("| P0 |", "| P1 |", "| P2 |", "Blocker", "Major", "Minor"):
            self.assertIn(row, self.TEXT)
        self.assertIn("图解或关键插图渲染失败、离线缺失，只剩报错或空白（I6）", self.TEXT)

    def test_rule_id_gate_and_false_positives(self) -> None:
        self.assertIn("每条问题都要指得到一个规则号", self.TEXT)
        self.assertIn("## 4. 误报", self.TEXT)
        self.assertIn("## 5. 矫枉过正", self.TEXT)

    def test_cjk_numbers(self) -> None:
        self.assertIn("上限 46", self.TEXT)
        self.assertIn("1.6–1.75", self.TEXT)

    def test_target_viewports(self) -> None:
        self.assertIn("目标视口都没有横向溢出", self.TEXT)
        self.assertIn("响应式页面至少验 1280 与 375", self.TEXT)


class CritiqueTest(unittest.TestCase):
    TEXT = ref("critique.md")

    def test_finding_table(self) -> None:
        self.assertIn("| # | 镜头 | 严重度 | 位置 | 规则 | 现状 | 改法 | 验证 |", self.TEXT)
        self.assertIn("`rendered`", self.TEXT)
        self.assertIn("`code-only`", self.TEXT)

    def test_review_handbook(self) -> None:
        for phrase in ("三秒测试", "精致度", "设计感", "保留：", "重做：", "不打数字分"):
            self.assertIn(phrase, self.TEXT)

    def test_isolated_review(self) -> None:
        self.assertIn("交给评审者", self.TEXT)
        self.assertIn("留在手里", self.TEXT)
        self.assertIn("confirm-protocol.md", self.TEXT)

    def test_stop_rule(self) -> None:
        self.assertIn("## 6. 迭代与停止", self.TEXT)
        self.assertIn("唯一标准", self.TEXT)
        self.assertIn("结论是“通过”", self.TEXT)
        self.assertIn("同一个问题连续两轮没改好", self.TEXT)
        self.assertIn("新发现的 P2 与提升写进交付说明", self.TEXT)

    def test_self_check_light_with_isolated_review(self) -> None:
        self.assertIn("完整扫查和问题表交给评审者", self.TEXT)


class EvidenceTest(unittest.TestCase):
    TEXT = ref("evidence.md")

    def test_tiers(self) -> None:
        for tier in ("| 基础档 |", "| 状态档 |", "| 复审档 |"):
            self.assertIn(tier, self.TEXT)
        self.assertIn("每个目标视口截首屏", self.TEXT)
        self.assertIn("每个目标视口补整页", self.TEXT)
        self.assertIn("首屏已覆盖整页时复用首屏", self.TEXT)
        self.assertIn("只截上一轮问题涉及的区域和视口", self.TEXT)

    def test_target_viewports(self) -> None:
        self.assertIn("桌面专用选 1280，手机专用选 375", self.TEXT)
        self.assertIn("响应式或无法判断时选 1280 + 375", self.TEXT)
        self.assertIn("上游另有视口硬门时按上游", self.TEXT)

    def test_tools_and_measure(self) -> None:
        self.assertIn("未渲染验证", self.TEXT)
        self.assertIn("http.server --bind 127.0.0.1", self.TEXT)
        self.assertIn("复用本地服务和浏览器会话", self.TEXT)
        self.assertIn("横向溢出", self.TEXT)


class PageTest(unittest.TestCase):
    TEXT = ref("page.md")

    def test_output_root_and_legacy(self) -> None:
        self.assertIn("默认输出到 `docs/pretty-ui/`", self.TEXT)
        self.assertIn("`docs/pretty-view-html/index.html`", self.TEXT)

    def test_links_and_confirmation(self) -> None:
        self.assertIn("包含这个链接的 HTML 文件所在目录", self.TEXT)
        self.assertIn("用户明确确认后另起一次改动", self.TEXT)
        self.assertIn("已有文件不移动、不覆盖", self.TEXT)
        self.assertIn("check_page.py --offline", self.TEXT)

    def test_starts_from_template(self) -> None:
        self.assertIn("从 [assets/reading-page.html](../assets/reading-page.html) 起手", self.TEXT)
        self.assertIn("[evidence.md](evidence.md) 截图并量行长", self.TEXT)
        self.assertIn("阅读页默认响应式", self.TEXT)

    def test_reading_layout(self) -> None:
        self.assertIn("中文每行 30–40 字（上限 46）", self.TEXT)
        self.assertIn("用 `px` 或 `rem` 写在列容器上", self.TEXT)
        self.assertIn("16–18px", self.TEXT)
        self.assertIn("`text-wrap: balance`", self.TEXT)
        self.assertIn("先在灰度下", self.TEXT)


class NoticeTest(unittest.TestCase):
    def test_sources_and_licenses(self) -> None:
        notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        for src in ("oil-oil/oil-ui", "edisonmbli/refactoring-ui-skill", "plannotator/effective-html"):
            self.assertIn(src, notice)
        for path in ("licenses/oil-ui-MIT.txt", "licenses/refactoring-ui-skill-MIT.txt", "references/html-diagram/LICENSE"):
            self.assertIn(path, notice)
            self.assertIn("MIT License", (ROOT / path).read_text(encoding="utf-8"))

    def test_ported_scripts_name_source(self) -> None:
        for script in ("palette.py", "contrast.py"):
            head = (ROOT / "scripts" / script).read_text(encoding="utf-8")[:600]
            self.assertIn("edisonmbli/refactoring-ui-skill", head)
            self.assertIn("MIT", head)


if __name__ == "__main__":
    unittest.main()
