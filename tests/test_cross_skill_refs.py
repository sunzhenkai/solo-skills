"""跨 skill 引用契约：被引用方改名、下线或删除概念后，调用方不残留旧引用；跨 skill 相对链接登记在 README 依赖组。

登记表：
- `archive/README.md`「条目」：已下线的 skill；「改名、合并与删除的概念」：旧名 → 现在的 skill（或 —）。
- `README.md`「依赖组」：用相对链接读取其他 skill 文件的 skill 及需要同装的 skill；「外部依赖」：仓外 skill。
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
RUNTIME_SUBDIRS = ("references", "examples")
# `$name` 里不是 skill 的固定写法（如 JSON Schema 的 `$id`）。
NON_SKILL_DOLLAR = {"id"}

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
DOLLAR_REF = re.compile(r"`\$([a-z][a-z0-9-]*)`")
SLASH_REF = re.compile(r"\{\{slash:([a-z][a-z0-9-]*)\}\}")
OPTIONAL_FILE_REF = re.compile(r"`([a-z][a-z0-9-]+/(?:SKILL\.md|references/[A-Za-z0-9_./-]+\.md))`")
BACKTICKED = re.compile(r"`([^`]+)`")


def skill_ids() -> list[str]:
    return sorted(p.parent.name for p in SKILLS.glob("*/SKILL.md"))


def runtime_files(skill: str) -> list[Path]:
    root = SKILLS / skill
    files = [root / "SKILL.md"]
    for sub in RUNTIME_SUBDIRS:
        if (root / sub).is_dir():
            files += sorted((root / sub).rglob("*.md"))
    return files


def prose_lines(path: Path) -> list[tuple[int, str]]:
    """去掉代码块后的行；保留行内代码，由调用方决定是否剥离。"""
    out, fenced = [], False
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            out.append((no, line))
    return out


def table_rows(text: str, heading: str) -> list[list[str]]:
    section = text.split(heading, 1)[1].split("\n#", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-", " "}:
            continue
        rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:]


def backticked(cell: str) -> list[str]:
    return BACKTICKED.findall(cell)


def renamed_and_retired() -> dict[str, str | None]:
    """旧名 → 现在的 skill；已下线或已删除的概念映射为 None。"""
    text = (ROOT / "archive" / "README.md").read_text(encoding="utf-8")
    old: dict[str, str | None] = {}
    for row in table_rows(text, "## 条目"):
        for name in backticked(row[0]):
            old[name] = None
    for row in table_rows(text, "## 改名、合并与删除的概念"):
        successor = backticked(row[1])
        for name in backticked(row[0]):
            old[name] = successor[0] if successor else None
    return old


def readme() -> str:
    return (ROOT / "README.md").read_text(encoding="utf-8")


def dependency_groups() -> dict[str, set[str]]:
    groups: dict[str, set[str]] = {}
    for row in table_rows(readme(), "### 依赖组"):
        for skill in backticked(row[0]):
            groups[skill] = set(backticked(row[1]))
    return groups


def external_skills() -> set[str]:
    names: set[str] = set()
    for row in table_rows(readme(), "## 外部依赖"):
        names.update(backticked(row[0]))
    return names


class RegistryTest(unittest.TestCase):
    def test_registries_parse_and_point_to_real_skills(self) -> None:
        ids = set(skill_ids())
        old = renamed_and_retired()
        self.assertIn("project-spec-mirror", old)
        self.assertEqual(old.get("skill-evolver"), "skill-upgrader")
        for name, successor in old.items():
            self.assertNotIn(name, ids, f"{name} 已登记为旧名，却仍是在役 skill")
            if successor:
                self.assertIn(successor, ids, f"{name} 的现名 {successor} 不存在")
        groups = dependency_groups()
        self.assertIn("taskflow", groups)
        for skill, needs in groups.items():
            self.assertIn(skill, ids)
            self.assertLessEqual(needs, ids, f"{skill} 的依赖组含不存在的 skill")


class OldNameTest(unittest.TestCase):
    def test_old_names_only_as_alias_or_in_successor(self) -> None:
        old = renamed_and_retired()
        patterns = {n: re.compile(r"(?<![\w.-])" + re.escape(n) + r"(?![\w-])") for n in old}
        offenders = []
        for skill in skill_ids():
            for path in runtime_files(skill):
                for no, line in prose_lines(path):
                    for name, pattern in patterns.items():
                        if not pattern.search(line) or old[name] == skill:
                            continue
                        if re.search(r"原\s*`?" + re.escape(name), line):
                            continue
                        offenders.append(f"{path.relative_to(ROOT)}:{no}: {name}")
        self.assertEqual(offenders, [], "旧名只能写成「原 `旧名`」，或出现在登记的现名 skill 里")


class DollarRefTest(unittest.TestCase):
    def test_dollar_refs_name_known_skills(self) -> None:
        known = set(skill_ids()) | external_skills() | NON_SKILL_DOLLAR
        unknown = []
        for skill in skill_ids():
            for path in runtime_files(skill):
                for no, line in prose_lines(path):
                    for name in DOLLAR_REF.findall(line):
                        if name not in known:
                            unknown.append(f"{path.relative_to(ROOT)}:{no}: ${name}")
        self.assertEqual(unknown, [], "`$name` 须是本仓 skill 或 README「外部依赖」登记的 skill")

    def test_slash_placeholders_name_known_skills(self) -> None:
        old = renamed_and_retired()
        known = set(skill_ids()) | external_skills()
        unknown = []
        for skill in skill_ids():
            for path in runtime_files(skill):
                for no, line in prose_lines(path):
                    for name in SLASH_REF.findall(line):
                        if name in known:
                            continue
                        if name in old and old[name] == skill:
                            continue
                        unknown.append(f"{path.relative_to(ROOT)}:{no}: {{{{slash:{name}}}}}")
        self.assertEqual(unknown, [], "`{{slash:name}}` 须是本仓 skill、外部依赖或当前 skill 登记的旧名")

    def test_optional_cross_skill_file_anchors_exist(self) -> None:
        ids = set(skill_ids())
        missing = []
        for skill in skill_ids():
            for path in runtime_files(skill):
                for no, line in prose_lines(path):
                    for rel in OPTIONAL_FILE_REF.findall(line):
                        target_skill = rel.split("/", 1)[0]
                        if target_skill not in ids:
                            continue
                        if not (SKILLS / rel).is_file():
                            missing.append(f"{path.relative_to(ROOT)}:{no}: `{rel}`")
        self.assertEqual(missing, [], "可选跨 skill 文件锚点在源仓必须真实存在")


class LinkTest(unittest.TestCase):
    def links(self, skill: str):
        for path in runtime_files(skill):
            for no, line in prose_lines(path):
                for target in LINK.findall(INLINE_CODE.sub("", line)):
                    if re.match(r"^[a-z][a-z0-9+.-]*:|^\{\{|^<", target):
                        continue
                    yield path, no, target, (path.parent / target).resolve()

    def test_skill_and_reference_links_resolve(self) -> None:
        broken = []
        for skill in skill_ids():
            for path, no, target, resolved in self.links(skill):
                if "examples" in path.relative_to(SKILLS / skill).parts:
                    continue
                if not resolved.exists():
                    broken.append(f"{path.relative_to(ROOT)}:{no}: {target}")
        self.assertEqual(broken, [])

    def test_cross_skill_links_are_declared(self) -> None:
        groups = dependency_groups()
        skills_root = SKILLS.resolve()
        offenders = []
        for skill in skill_ids():
            own = (SKILLS / skill).resolve()
            for path, no, target, resolved in self.links(skill):
                if resolved == own or own in resolved.parents:
                    continue
                where = f"{path.relative_to(ROOT)}:{no}: {target}"
                if skills_root not in resolved.parents:
                    offenders.append(f"{where}（链出 skills/，安装后必断）")
                    continue
                other = resolved.relative_to(skills_root).parts[0]
                if other not in groups.get(skill, set()):
                    offenders.append(f"{where}（{skill} → {other} 未登记依赖组）")
        self.assertEqual(offenders, [], "跨 skill 相对链接须在 README「依赖组」登记")


if __name__ == "__main__":
    unittest.main()
