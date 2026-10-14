"""evals/cases.yaml 结构检查（标准库，按行解析，不依赖 PyYAML）：每条案例有 id / kind / judge / description / given / expect.must，id 不重复。"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("kind:", "judge:", "description:", "given:", "expect:", "must:")


def cases(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^  - id: ", text, flags=re.M)[1:]
    return [(p.split("\n", 1)[0].strip(), p) for p in parts]


class EvalsStructureTest(unittest.TestCase):
    def test_all_cases_well_formed(self) -> None:
        files = sorted((ROOT / "skills").glob("*/evals/cases.yaml"))
        self.assertTrue(files)
        for f in files:
            text = f.read_text(encoding="utf-8")
            self.assertIn("cases:", text, f)
            got = cases(f)
            self.assertTrue(got, f)
            ids = [i for i, _ in got]
            self.assertEqual(len(ids), len(set(ids)), f"{f}: 重复 id")
            for cid, body in got:
                for key in REQUIRED:
                    self.assertIn(key, body, f"{f}:{cid} 缺 {key}")


if __name__ == "__main__":
    unittest.main()
