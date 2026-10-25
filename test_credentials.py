"""CWE-798 regression test: no hardcoded default credential is shipped.

The original init_db() seeded a fixed user with the guessable password
's3cr3t' straight from source. The fix generates a per-install random password,
so the seeded credential must no longer equal the shipped literal.
"""
import sqlite3

import app


def test_seeded_password_is_not_the_shipped_literal():
    conn = sqlite3.connect(app.DB)
    row = conn.execute("SELECT password FROM users WHERE username = 'alice'").fetchone()
    conn.close()
    assert row is not None, "expected seeded user 'alice'"
    assert row[0] != "s3cr3t", "hardcoded default credential is still shipped in source"
    assert len(row[0]) >= 12, "seeded password is not sufficiently long/random"
