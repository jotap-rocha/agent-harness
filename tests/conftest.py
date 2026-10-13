"""Conftest global: neutraliza diferenças de encoding do Windows (cp1252) nos subprocessos."""

from __future__ import annotations

import os

# Subprocessos Python herdam o ambiente; UTF-8 evita UnicodeEncodeError (ex.: "↔") em stdout cp1252.
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
