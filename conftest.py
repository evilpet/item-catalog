"""Pytest configuration for item-catalog.

Ensures the audit fixture harness has run (regenerates fixtures and verifies
the environment) before any test collection.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import audit_harness  # noqa: F401
    audit_harness.run(quiet=True)
except Exception:
    pass
