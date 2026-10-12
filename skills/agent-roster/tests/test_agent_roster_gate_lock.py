"""行为锁：瘦身/合并前从正文冻结的门禁句（含 禁止/不得/必须/强制/先读 等），必须仍逐字出现在本 skill 的 SKILL.md + references 全文中。

搬移只能原句搬；确需删除某句时，同一 commit 从 gate_lines.txt 删掉该行并在提交说明写明理由。
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^(?:[-*>]\s+|\d+\.\s+|#+\s+)", "", line)
    line = re.sub(r"\[[^\]]*\]\([^)]*\)", "[link]", line)  # 链接目标/文字随文件搬家而变，不算语义变化
    return line.strip()


def corpus() -> str:
    files = [ROOT / "SKILL.md"]
    if (ROOT / "references").is_dir():
        files += sorted((ROOT / "references").rglob("*.md"))
    return "\n".join(norm(l) for f in files for l in f.read_text(encoding="utf-8").splitlines())


class TestGateLinesPreserved(unittest.TestCase):
    def test_all_gate_lines_present(self) -> None:
        text = corpus()
        wanted = [l for l in (ROOT / "tests" / "gate_lines.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
        missing = [l for l in wanted if l not in text]
        self.assertEqual(missing, [], f"{len(missing)} 条门禁句丢失")


if __name__ == "__main__":
    unittest.main()
