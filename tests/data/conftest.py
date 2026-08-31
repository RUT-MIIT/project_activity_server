"""Фикстуры для тестов модулей data/."""

from __future__ import annotations

from pathlib import Path
import sys

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
if str(DATA_DIR) not in sys.path:
    sys.path.insert(0, str(DATA_DIR))
