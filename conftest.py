"""Pytest configuration for item-catalog.

Initializes the SQLite fixture database used by the test suite.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app  # noqa: E402

app.init_db()
