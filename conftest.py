"""Shared pytest fixtures for the item-catalog test suite.

Provides a fresh, in-memory-style SQLite database (in a temp dir) for every test
so the suite is hermetic: it does not depend on a pre-existing ``items.db`` and
never leaves a database file in the source tree.
"""
import os

import pytest

import app


@pytest.fixture(autouse=True)
def _database(tmp_path, monkeypatch):
    db_path = os.path.join(str(tmp_path), "items.db")
    monkeypatch.setattr(app, "DB", db_path)
    app.init_db()
    yield db_path
