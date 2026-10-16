"""多 worker 附录契约。"""
from __future__ import annotations
import unittest
from pathlib import Path

MW = (Path(__file__).resolve().parents[1] / "references" / "multi-worker.md").read_text(encoding="utf-8")


class ParallelBroadcastTest(unittest.TestCase):
    def test_default_serial_note(self) -> None:
        self.assertIn("默认串行", MW)

    def test_broadcast(self) -> None:
        self.assertIn("改共享面先广播", MW)

    def test_flagship(self) -> None:
        self.assertIn("样板先行", MW)


if __name__ == "__main__":
    unittest.main()
