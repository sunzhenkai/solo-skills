"""visualize 文本契约测试：锁定触发、五步主流程、视觉简报、下游路由与降级、事实回查和交付形状。"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
BRIEF = (ROOT / "references" / "brief.md").read_text(encoding="utf-8")
ROUTING = (ROOT / "references" / "routing.md").read_text(encoding="utf-8")
VERIFY = (ROOT / "references" / "verify.md").read_text(encoding="utf-8")
ARCHIFY_TYPES = (
    "architecture", "workflow", "sequence", "dataflow", "lifecycle",
    "erd", "class", "tree", "timeline", "waterfall",
)


class VisualizeContractTest(unittest.TestCase):
    def test_frontmatter_routes_content_visualization(self) -> None:
        self.assertIn("id: visualize", SKILL)
        self.assertIn("description: 内容可视化编排", SKILL)
        self.assertIn("把已有内容画成图、做成图解或可视化讲解页，或点名 visualize 时使用", SKILL)
        self.assertNotIn("disable-model-invocation: true", SKILL)
        self.assertIn("compatibility:", SKILL)

    def test_adjacent_skills_keep_their_scope(self) -> None:
        self.assertIn("以文字为主的阅读页由 `pretty-ui` 的 page 模式承接", SKILL)
        self.assertIn("产品界面、页面与组件由 `ui-kit` 分派", SKILL)
        self.assertIn("项目架构的持久文档由 `project-atlas` 维护", SKILL)
        self.assertIn("schema、布局和渲染由下游 skill 按各自当版正文完成", SKILL)

    def test_five_steps_each_end_with_done_marker(self) -> None:
        steps = re.findall(r"^### (\d)\. (.+)$", SKILL, flags=re.M)
        self.assertEqual(
            [name for _, name in steps],
            ["定读者问题", "写视觉简报", "选下游", "交给下游执行", "核对与交付"],
        )
        self.assertEqual(SKILL.count("完成标志："), 5)

    def test_reader_question_decides_whether_to_draw(self) -> None:
        self.assertIn("看完要回答的一个问题", SKILL)
        self.assertIn("线性不超过三步、单个数字或纯定义，默认用文字或列表回答并说明理由", SKILL)
        self.assertIn("用户明确要求出图时仍按主流程画", SKILL)

    def test_brief_carries_sourced_facts(self) -> None:
        self.assertIn("references/brief.md", SKILL)
        self.assertIn("图里要出现的每个标签、关系和数字都在事实清单里有出处", SKILL)
        self.assertIn("图里只放用户给出的值", SKILL)
        self.assertIn("用户也给不出时，按已知精度放置并标「不详」", SKILL)
        self.assertIn("下游字段留到第 3 步补写", SKILL)
        self.assertIn("简报、图和交付消息都不出现原值", SKILL)
        self.assertIn("下游在第 3 步选定后补写", BRIEF)
        self.assertIn("作为对比对象的备选方案照常列入", BRIEF)
        for field in ("读者问题", "结论句", "主形态", "交付", "约束", "输出目录"):
            self.assertIn(f"- {field}：", BRIEF)
        self.assertIn("| ID | 事实 | 出处 | 必须 |", BRIEF)
        self.assertIn("## 省略", BRIEF)
        self.assertIn("换下游时复用同一份简报", BRIEF)

    def test_routing_covers_archify_types_and_explainer(self) -> None:
        for kind in ARCHIFY_TYPES:
            self.assertIn(f"archify `{kind}`", ROUTING)
        self.assertIn("visual-explainer（archify 不画数值图表）", ROUTING)
        self.assertIn("两套渲染各出各的文件", ROUTING)

    def test_availability_probe_and_fallback_chain(self) -> None:
        self.assertIn("Archify is ready.", ROUTING)
        self.assertIn("kit/render.mjs", ROUTING)
        self.assertIn("这三项只用于 archify 与 visual-explainer，都通过才算可用", ROUTING)
        self.assertIn("`pretty-ui` 找到其 `SKILL.md` 即可用", ROUTING)
        self.assertIn("先按读者问题选第 2 节的形态", ROUTING)
        self.assertIn("故障时间线是 `timeline`", ROUTING)
        self.assertIn("visual-explainer 单图页（One diagram 形态）→ `pretty-ui` page 模式手画图解 → Mermaid 源码", ROUTING)
        self.assertIn("`pretty-ui` page 模式（阅读页 + 图解", ROUTING)
        self.assertIn("用户同意后走 `skills-store` 先审计再安装", ROUTING)
        self.assertIn("安装经 `skills-store` 审计且得到用户同意后才执行", SKILL)
        self.assertIn("降级会把以图为主改成以文字为主", SKILL)
        self.assertIn("推荐补齐，用户选定后再继续", SKILL)

    def test_downstream_gates_are_named(self) -> None:
        self.assertIn("archify.mjs finalize <type>", ROUTING)
        self.assertIn("--repo-root <repo>", ROUTING)
        self.assertIn("非零退出即失败", ROUTING)
        self.assertIn("修完它列出的每个 `✗`", ROUTING)
        self.assertIn("Before delivery", ROUTING)
        self.assertIn("下游门禁通过，产物可在浏览器打开", SKILL)

    def test_fact_check_and_visual_review(self) -> None:
        self.assertIn("references/verify.md", SKILL)
        self.assertIn("逐条对到简报事实清单的 ID", VERIFY)
        self.assertIn("原文没有、属于推断：删掉", VERIFY)
        self.assertIn("「必须」的事实都在图上有位置", VERIFY)
        self.assertIn("finalize 通过代表自动检查通过", VERIFY)
        self.assertIn("核对行写「未渲染验证」", VERIFY)
        self.assertIn("推断 <b>、示意 <c>", VERIFY)
        self.assertIn("要求离线时，产物不引用外部 URL", VERIFY)

    def test_repair_has_stop_point(self) -> None:
        self.assertIn("两轮仍不过就停下，报告卡在哪里", SKILL)
        self.assertIn("报告失败的门禁、已尝试的修改和剩余问题", VERIFY)

    def test_output_root_and_read_only_skill_dir(self) -> None:
        self.assertIn("用户指定路径 > 项目已有约定 > 当前工作目录下的 `visuals/<slug>-<YYYYMMDD-HHMMSS>/`", SKILL)
        self.assertIn("一律传入上面的路径", SKILL)
        self.assertIn("本 skill 目录保持只读", SKILL)
        self.assertIn("每张 archify 图一个子目录", SKILL)

    def test_delivery_shape(self) -> None:
        for line in ("[<描述性标题>](<产物绝对路径>)", "读法：", "核对：", "事实 <有出处>/<图中事实> 有出处", "未渲染验证"):
            self.assertIn(line, SKILL)
        self.assertIn("第 1 步决定用文字回答时，直接给文字或列表，加一句为何不画", SKILL)
        self.assertIn("命令、修复轮次和回执细节留在输出目录", SKILL)

    def test_downstreams_referenced_by_name_only(self) -> None:
        for text in (SKILL, BRIEF, ROUTING, VERIFY):
            self.assertNotRegex(text, r"\]\(\.\./\.\./")


if __name__ == "__main__":
    unittest.main()
