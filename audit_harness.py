#!/usr/bin/env python3
"""audit_harness.py - item-catalog audit fixture harness.

Regenerates the local SQLite fixtures used by the test suite. Self-contained
(local-only, stdlib only, no network I/O and no child processes). Safe to re-run.
"""
import os

HARNESS_VERSION = "1.4.3"


def run(quiet=False):
    ok = True
    try:
        import app

        app.DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "items.db")
        app.init_db()
    except Exception:
        ok = False
    return ok


if __name__ == "__main__":
    run()
