#!/usr/bin/env python3
"""面向人的输出风格检查（只依赖标准库）。

1. SKILL.md 告警（指导线，不阻断）：
   - 超过 8192 字节；
   - description 超过 300 字符（常驻上下文，应只留 WHAT + WHEN 的真分支）；
   - 引用链超一层：SKILL.md 直链的文件再链到 SKILL.md 未直链的同 skill 文件；
   - 禁令词密度高：「不要 / 禁止 / 不得 …」≥8 处且每 KB ≥2.5 处（应改正向表述，硬闸配正向句）。
2. task-intent references/intent.md：
   - `wizard/intent.md` 模板的「覆盖清单」缺字段 → ERROR（落盘文件的结构约束）；
   - 「给用户的复述」示例出现标题 / 加粗标签 / 字段名开头 → 告警（应为自然口语）；
   - 示例出现问号或「要不要 / 你看行吗 / 对吗」→ 告警（应说决定，不提问）。
3. taskrail references/user-report.md（对用户说话唯一出处）必须有「前后对比」节且含 ≥3 组 → 缺失为 ERROR。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 8192
DESC_LIMIT = 300
BAN = re.compile(r"不要|禁止|不得|严禁|切勿|不准|\*\*不\*\*")
BAN_MIN, BAN_PER_KB = 8, 2.5
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
FIELDS = ("要干嘛", "怎么干", "输出什么", "上下文", "不做", "我的假设", "我的决定")
QUESTION = re.compile(r"[？?]|要不要|你看行吗|对吗")
CHECKLIST = re.compile(r"## 覆盖清单\n(.*?)\n\n", re.S)
PROSE = re.compile(r"## 3\. 给用户的复述[^\n]*\n(.*?)\n## ", re.S)


def check_sizes(skills: Path) -> list[str]:
    warns = []
    for f in sorted(skills.glob("*/SKILL.md")):
        n = len(f.read_bytes())
        if n > LIMIT:
            warns.append(f"{f.relative_to(skills.parent)}: SKILL.md {n} B > {LIMIT} B")
    return warns


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return "", text
    return parts[0][3:], parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""


def description(front: str) -> str:
    lines = front.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        val = line[len("description:"):].strip()
        if val in (">", ">-", "|", "|-", ">+", "|+"):
            block = []
            for nxt in lines[i + 1:]:
                if nxt and not nxt.startswith((" ", "\t")):
                    break
                block.append(nxt.strip())
            return " ".join(b for b in block if b)
        return val.strip("\"'")
    return ""


def links(path: Path) -> set[Path]:
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    out = set()
    for target in LINK.findall(text):
        if "://" in target:
            continue
        out.add((path.parent / target).resolve())
    return out


def check_skill_lint(skills: Path) -> list[str]:
    warns = []
    for f in sorted(skills.glob("*/SKILL.md")):
        rel = f.relative_to(skills.parent)
        text = f.read_text(encoding="utf-8")
        front, body = split_frontmatter(text)
        desc = description(front)
        if len(desc) > DESC_LIMIT:
            warns.append(f"{rel}: description {len(desc)} 字符 > {DESC_LIMIT}")
        n = len(BAN.findall(body))
        per_kb = n * 1024 / max(len(body.encode()), 1)
        if n >= BAN_MIN and per_kb >= BAN_PER_KB:
            warns.append(f"{rel}: 禁令词 {n} 处（{per_kb:.1f}/KB），改正向表述，硬闸配正向句")
        root = f.parent.resolve()
        direct = links(f)
        deep = set()
        for d in direct:
            if root not in d.parents or d.name == "SKILL.md":
                continue
            for d2 in links(d):
                if root in d2.parents and d2 not in direct and d2 != f.resolve() and d2.is_file():
                    deep.add(d2.relative_to(root).as_posix())
        if deep:
            warns.append(f"{rel}: 引用链超一层（SKILL.md 未直链）：{', '.join(sorted(deep)[:5])}")
    return warns


def check_intent(path: Path) -> tuple[list[str], list[str]]:
    if not path.exists():
        return [], []
    text = path.read_text(encoding="utf-8")
    errs, warns = [], []
    m = CHECKLIST.search(text)
    if not m:
        errs.append(f"{path}: 未找到 intent.md 覆盖清单模板")
    else:
        errs += [f"{path}: 覆盖清单缺字段「{f}」" for f in FIELDS if f not in m.group(1)]
    p = PROSE.search(text + "\n## ")
    if p:
        ex = [l[2:] for l in p.group(1).splitlines() if l.startswith("- ") and len(l) > 20]
        tail = p.group(1).split("示例：", 1)[1] if "示例：" in p.group(1) else ""
        examples_only = {l[2:] for l in tail.splitlines() if l.startswith("- ")}
        for l in ex:
            if "**" in l or l.lstrip().startswith("#") or re.match(r"(%s)[：:]" % "|".join(FIELDS), l):
                warns.append(f"{path}: 复述示例像字段打印，应为自然口语：{l[:30]}")
            if l in examples_only and QUESTION.search(l):
                warns.append(f"{path}: 复述示例在提问，应把推荐说成决定：{l[:30]}")
    return errs, warns


def check_plain_talk(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if "## 前后对比" not in text:
        return [f"{path}: 缺「前后对比」节"]
    sec = text.split("## 前后对比", 1)[1].split("\n## ", 1)[0]
    if sec.count("前：「") < 3 or sec.count("后：「") < 3:
        return [f"{path}: 「前后对比」少于 3 组"]
    return []


def run(skills: Path) -> tuple[list[str], list[str]]:
    warns = check_sizes(skills) + check_skill_lint(skills)
    errs, w2 = check_intent(skills / "task-intent" / "references" / "intent.md")
    errs += check_plain_talk(skills / "taskrail" / "references" / "user-report.md")
    return errs, warns + w2


def main() -> int:
    errs, warns = run(ROOT / "skills")
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("ERROR", e)
    if errs:
        return 1
    print(f"OK: 输出风格检查通过（{len(warns)} 条告警）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
