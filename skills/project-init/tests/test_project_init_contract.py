"""project-init：frontmatter、引用文件与门禁用语。"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(skill_md: str) -> str:
    parts = skill_md.split("---", 2)
    if len(parts) < 3:
        return ""
    return parts[1]


class ContractTest(unittest.TestCase):
    def test_frontmatter_name(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: project-init", text)
        self.assertIn("id: project-init", text)

    def test_description_omits_frameworks(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        fm = _frontmatter(text)
        for needle in (
            "Django",
            "django-rest-framework",
            "FastAPI",
            "Flask",
            "Pydantic",
            "SQLAlchemy",
            "Vite",
            "shadcn",
            "Tailwind",
            "React",
            "Next.js",
            "Playwright",
            "Storybook",
            "Zustand",
            "Vitest",
        ):
            self.assertNotIn(needle, fm)

    def test_reference_files_exist(self) -> None:
        for rel in ("references/python-api.md", "references/frontend.md"):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_gate_and_stacks(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("显式", text)
        self.assertIn("**算触发**（白名单", text)
        self.assertNotIn("不算触发", text)
        self.assertNotIn("⭐", text)
        self.assertIn("python-api", text)
        self.assertIn("frontend", text)
        self.assertIn("FastAPI", text)
        self.assertIn("按需求选层", text)
        self.assertIn("Playwright", text)
        self.assertIn("特定场景再用", text)

    def test_python_layers(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        py = (ROOT / "references/python-api.md").read_text(encoding="utf-8")
        for needle in (
            "FastAPI",
            "Django",
            "Flask",
            "Litestar",
            "Pydantic",
            "OpenAPI",
            "SQLModel",
            "SQLAlchemy",
            "Tortoise",
            "uvicorn",
            "Celery",
            "Dramatiq",
            "ARQ",
            "pytest",
            "httpx",
            "Ruff",
        ):
            self.assertIn(needle, skill)
            self.assertIn(needle, py)
        self.assertIn("| 层 | 选择 | 建议 |", py)
        self.assertIn("fastapi[standard]", py)
        self.assertIn("sqlalchemy", py.lower())
        self.assertIn("需要后台任务再用", skill)
        self.assertIn("startproject", py)
        self.assertIn("rest_framework", py)
        self.assertIn("只装所选层", py)

    def test_frontend_layers(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        fe = (ROOT / "references/frontend.md").read_text(encoding="utf-8")
        for needle in (
            "TypeScript",
            "TanStack Query",
            "Zod",
            "React Hook Form",
            "OpenAPI",
            "Playwright",
            "Storybook",
            "Lucide",
            "Radix",
            "DESIGN.md",
            "Design Tokens",
            "Motion",
            "Next.js",
            "Zustand",
            "Vitest",
        ):
            self.assertIn(needle, skill)
            self.assertIn(needle, fe)
        self.assertIn("| 层 | 选择 | 建议 |", fe)
        self.assertIn("需要表单再用", fe)
        self.assertIn("需要客户端全局状态再用", fe)
        self.assertIn("需要动效再用", fe)
        self.assertIn("需要单元测试再用", fe)
        self.assertIn("toHaveScreenshot", fe)
        self.assertIn("playwright", fe.lower())
        self.assertIn("storybook", fe.lower())
        self.assertIn("react-hook-form", fe)
        self.assertIn("tokens.css", fe)

    def test_nextjs_path(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        fe = (ROOT / "references/frontend.md").read_text(encoding="utf-8")
        # SKILL.md 声明两条前端路径，且 Next 不再只是单行备注
        self.assertIn("Next.js 路径", skill)
        self.assertIn("Vite 与 Next 并存", skill)
        self.assertIn("create-next-app", skill)
        # reference 有完整 Next.js 路径：官方命令、shadcn 接入、目录、冒烟、align
        self.assertIn("## Next.js 路径", fe)
        self.assertIn("create-next-app", fe)
        self.assertIn('--import-alias "@/*"', fe)
        self.assertIn("shadcn", fe)
        self.assertIn("App Router", fe)
        self.assertIn("use client", fe)
        self.assertIn("route.ts", fe)
        self.assertIn("next-env.d.ts", fe)
        self.assertIn("pnpm build", fe)
        self.assertIn("storybook build", fe)
        self.assertIn("align 对照（Next.js 路径）", fe)

    def test_nextjs_not_in_frontmatter(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        fm = _frontmatter(text)
        self.assertNotIn("Next.js", fm)
        self.assertNotIn("create-next-app", fm)

    def test_plan_confirm_and_tool_cli(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        py = (ROOT / "references/python-api.md").read_text(encoding="utf-8")
        fe = (ROOT / "references/frontend.md").read_text(encoding="utf-8")
        self.assertIn("最终方案", skill)
        self.assertIn("询问是否补齐", skill)
        self.assertIn("优先借助", skill)
        self.assertIn("官方工具命令", skill)
        self.assertIn("工具命令优先", py)
        self.assertIn("询问是否补齐", py)
        self.assertIn("工具命令优先", fe)
        self.assertIn("询问是否补齐", fe)

    def test_references_name_defaults(self) -> None:
        py = (ROOT / "references/python-api.md").read_text(encoding="utf-8")
        fe = (ROOT / "references/frontend.md").read_text(encoding="utf-8")
        self.assertIn("fastapi[standard]", py)
        self.assertIn("pydantic-settings", py)
        self.assertIn("startproject", py)
        self.assertIn("rest_framework", py)
        self.assertIn("react-ts", fe)
        self.assertIn("shadcn", fe)
        self.assertIn("Tailwind", fe)
        self.assertIn("DESIGN.md", fe)
        self.assertIn("lucide-react", fe)
