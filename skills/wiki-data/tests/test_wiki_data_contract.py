"""wiki-data：本地文档 wiki 的契约与边界。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.layout = (ROOT / "references" / "layout.md").read_text(encoding="utf-8")
        cls.types = (ROOT / "references" / "page-types.md").read_text(encoding="utf-8")
        cls.ingest = (ROOT / "references" / "ingest.md").read_text(encoding="utf-8")
        cls.query = (ROOT / "references" / "query.md").read_text(encoding="utf-8")
        cls.lint = (ROOT / "references" / "lint.md").read_text(encoding="utf-8")
        cls.organize = (ROOT / "references" / "organize.md").read_text(encoding="utf-8")

    def test_frontmatter_name_matches_directory(self) -> None:
        self.assertIn("name: wiki-data", self.skill)
        self.assertEqual(ROOT.name, "wiki-data")

    def test_reference_and_script_exist(self) -> None:
        for rel in (
            "references/layout.md",
            "references/page-types.md",
            "references/ingest.md",
            "references/query.md",
            "references/lint.md",
            "references/organize.md",
            "scripts/lint_wiki.py",
            "agents/openai.yaml",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_no_runtime_service_dependency(self) -> None:
        self.assertIn("不依赖 llmwiki 服务、MCP 或 SQLite", self.skill)
        self.assertIn("不启动 llmwiki 应用", self.skill)
        self.assertNotIn("Call the MCP", self.skill)
        self.assertNotIn(".llmwiki/index.db", self.skill)
        self.assertIn("工作区只含纯 Markdown 目录", self.skill)

    def test_raw_is_readonly(self) -> None:
        self.assertIn("`raw/` 只读", self.skill)
        self.assertIn("不编辑 `raw/`", self.skill)

    def test_init_requires_confirm(self) -> None:
        init = self.skill.split("## `init`", 1)[1].split("## ", 1)[0]
        self.assertIn("必须先获得确认", init)
        self.assertIn("未确认则停止", init)
        self.assertIn("必须先获得确认", self.layout)
        self.assertIn("未确认则停止", self.layout)

    def test_phases_are_named(self) -> None:
        for phase in ("guide", "init", "ingest", "query", "organize", "lint"):
            self.assertIn(f"`{phase}`", self.skill)

    def test_handoff_boundaries(self) -> None:
        self.assertIn("project-spec-mirror", self.skill)
        self.assertIn("code-explore", self.skill)
        self.assertIn("用户明确要求查证原因时交给 `trouble-grill`", self.skill)

    def test_trouble_grill_records_use_existing_page_types(self) -> None:
        self.assertIn("用户明确要求归档 `trouble-grill` 记录时", self.ingest)
        self.assertIn("wiki/sources/", self.ingest)
        self.assertIn("wiki/synthesis/", self.ingest)
        self.assertIn("只有 `confirmed` 假设可写成根因", self.ingest)
        for field in ("锚点", "证据等级", "用户输入", "dead-end", "验证盲区", "回退条件"):
            self.assertIn(field, self.ingest)

    def test_context_ingest_extracts_and_lists_before_writing(self) -> None:
        for term in ("当前对话", "自动提取", "知识", "主题", "经验", "踩坑", "操作信息"):
            self.assertIn(term, self.ingest)
        self.assertIn("先向用户展示**归档列表**，再按列表摄入", self.ingest)
        self.assertIn("候选 `type`", self.ingest)
        self.assertIn("新建 / 更新 / 合并目标", self.ingest)
        self.assertIn("上下文证据", self.ingest)
        self.assertIn("归档列表即本次写入范围", self.ingest)
        self.assertIn("写盘前完成", self.ingest)

    def test_privacy_gate(self) -> None:
        self.assertIn("摄入前做隐私自查", self.skill)
        self.assertIn("<REDACTED>", self.skill)
        self.assertIn("<REDACTED>", self.ingest)

    def test_log_contract(self) -> None:
        self.assertIn("## [YYYY-MM-DD] action | description", self.skill)
        self.assertIn("仅追加", self.skill)

    def test_typed_plural_directories(self) -> None:
        self.assertIn("wiki/entities/", self.layout)
        self.assertIn("应用复数目录名", self.layout)
        self.assertIn("不是 `entity/`", self.layout)

    def test_entity_concept_split(self) -> None:
        self.assertIn("概念标题保持中性", self.types)
        self.assertIn("渐进披露", self.types)

    def test_experience_and_ledger_contract(self) -> None:
        for path in ("wiki/experiences/", "wiki/ledgers/"):
            self.assertIn(path, self.layout)
            self.assertIn(path, self.types)
        for field in ("适用场景", "证据", "边界与失效条件", "last_verified"):
            self.assertIn(field, self.types)
        self.assertIn("当前状态", self.types)
        self.assertIn("纠正历史也追加新条目", self.ingest)
        self.assertIn("业务台账与操作日志分离", self.skill)

    def test_query_reads_pages_and_preserves_status(self) -> None:
        self.assertIn("references/query.md", self.skill)
        self.assertIn("页面全文才是回答依据", self.query)
        self.assertIn("status: draft", self.query)
        self.assertIn("当前状态", self.query)
        self.assertIn("wiki 尚未覆盖", self.query)

    def test_confidence_and_freshness_are_distinct(self) -> None:
        for field in ("confidence: high | medium | low", "last_verified", "review_after"):
            self.assertIn(field, self.types)
        self.assertIn("证据强度", self.types)
        self.assertIn("复审", self.types)
        self.assertIn("主张级", self.query)
        self.assertIn("页面级高置信度不能覆盖主张级低置信度", self.query)
        self.assertIn("不等于已经证伪", self.query)
        for code in ("confidence_invalid", "verification_missing", "date_invalid", "review_overdue"):
            self.assertIn(code, self.lint)

    def test_experience_supports_prevention_and_reuse(self) -> None:
        for section in ("触发信号", "预防与处理", "验证方式"):
            self.assertIn(section, self.types)
            self.assertIn(section, self.ingest)
            self.assertIn(section, self.query)
        self.assertIn("相似任务执行前查经验", self.skill)
        self.assertIn("执行前预检", self.query)
        self.assertIn("未检索到匹配经验", self.query)
        self.assertIn("只有「验证方式」已有对应结果和来源时才改为 `validated`", self.ingest)

    def test_corrections_and_deprecated_knowledge_keep_history(self) -> None:
        self.assertIn("已更正", self.ingest)
        self.assertIn("替代页链接", self.ingest)
        self.assertIn("`deprecated` 只作历史参考", self.query)
        self.assertIn("时效缺口", self.query)

    def test_phase_loaded_on_demand(self) -> None:
        self.assertIn("只读该阶段详情", self.skill)
        self.assertIn("其它 reference 等用到时再读", self.skill)
        self.assertIn("references/layout.md", self.skill)
        self.assertIn("references/organize.md", self.skill)

    def test_guide_and_init_live_in_layout(self) -> None:
        self.assertIn("## `guide`", self.layout)
        self.assertIn("真实 `ls`", self.layout)
        self.assertIn("只建上述纯 Markdown 骨架", self.layout)
        guide = self.skill.split("## `guide`", 1)[1].split("## ", 1)[0]
        self.assertNotIn("缺哪个就说哪个", guide)

    def test_organize_procedure_lives_in_reference(self) -> None:
        organize = self.skill.split("## `organize`", 1)[1].split("## ", 1)[0]
        self.assertNotIn("只描述 lint 实际报出的目录", organize)
        self.assertIn("只描述 lint 实际报出的目录", self.organize)
        self.assertIn("确认前不改", self.organize)


if __name__ == "__main__":
    unittest.main()
