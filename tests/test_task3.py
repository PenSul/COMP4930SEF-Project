"""Exercise the report's TextCNN and checkpoint selection without downloading news."""

import os
import unittest
from pathlib import Path
from typing import Any, ClassVar
from unittest.mock import patch

import nbformat


class Task3Tests(unittest.TestCase):
    """Run the same model definitions used in the assessed notebook."""

    scope: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        report = Path(__file__).resolve().parents[1] / "project_report.ipynb"
        cells = nbformat.read(report, as_version=4).cells
        cls.scope = {"__name__": __name__}
        with patch.dict(os.environ, TASK3_MODE="preview"):
            for cell in cells:
                if "task3-smoke" in cell.metadata.get("tags", []):
                    exec(compile(cell.source, cell.id, "exec"), cls.scope)

    def test_padding_gradients_and_save_reload(self) -> None:
        self.scope["check_textcnn"]()

    def test_checkpoint_ranking_and_ties(self) -> None:
        rank = self.scope["rank_textcnn_runs"]
        for acc128, f1_128, expected in (
            (0.91, 0.88, 128),  # accuracy comes first
            (0.90, 0.91, 128),  # then macro-F1
            (0.90, 0.90, 64),   # prefer the shorter input on an exact tie
        ):
            with self.subTest(acc128=acc128, f1_128=f1_128):
                rows = {
                    128: {"length": 128, "accuracy": acc128, "macro_f1": f1_128},
                    64: {"length": 64, "accuracy": 0.90, "macro_f1": 0.90},
                }
                self.assertEqual(int(rank(rows).loc[0, "length"]), expected)
