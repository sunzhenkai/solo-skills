#!/usr/bin/env python3
"""面向人的输出风格检查（只依赖标准库）。

1. SKILL.md 超过 8192 字节：告警（指导线，不阻断）。
2. task-intent references/intent.md：
   - `wizard/intent.md` 模板的「覆盖清单」缺字段 → ERROR（落盘文件的结构约束）；
   - 「给用户的复述」示例出现标题 / 加粗标签 / 字段名开头 → 告警（应为自然口语）。
3. taskrail contract 必须有「对用户说话」共用节且含 ≥3 组前后对比 → 缺失为 ERROR。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 8192
FIELDS = ("要干嘛", "怎么干", "输出什么", "上下文", "不做", "我的假设", "要你拍板的")
CHECKLIST = re.compile(r"## 覆盖清单\n(.*?)\n\n", re.S)
PROSE = re.compile(r"## 3\. 给用户的复述[^\n]*\n(.*?)\n## ", re.S)


def check_sizes(skills: Path) -> list[str]:
    warns = []
    for f in sorted(skills.glob("*/SKILL.md")):
        n = len(f.read_bytes())
        if n > LIMIT:
            warns.append(f"{f.relative_to(skills.parent)}: SKILL.md {n} B > {LIMIT} B")
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
        for l in ex:
            if "**" in l or l.lstrip().startswith("#") or re.match(r"(%s)[：:]" % "|".join(FIELDS), l):
                warns.append(f"{path}: 复述示例像字段打印，应为自然口语：{l[:30]}")
    return errs, warns


def check_plain_talk(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if "## 对用户说话" not in text:
        return [f"{path}: 缺「对用户说话」共用节"]
    if not (path.parent / "user-report.md").is_file():
        return [f"{path}: 缺 user-report.md（对用户汇报唯一出处）"]
    sec = text.split("## 对用户说话", 1)[1].split("\n## ", 1)[0]
    if sec.count("前：「") < 3 or sec.count("后：「") < 3:
        return [f"{path}: 「对用户说话」前后对比少于 3 组"]
    return []


def run(skills: Path) -> tuple[list[str], list[str]]:
    warns = check_sizes(skills)
    errs, w2 = check_intent(skills / "task-intent" / "references" / "intent.md")
    errs += check_plain_talk(skills / "taskrail" / "references" / "contract.md")
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
