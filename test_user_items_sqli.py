"""Regression test for the SQL injection in app.user_items() (CWE-89).

Before the fix, the caller-supplied username was concatenated into the SQL
text, so a value like "x' OR '1'='1" returned every user with their
plaintext password. After the fix, the value is bound as a literal
parameter and simply matches no row.
"""
from app import init_db, user_items


def test_user_items_no_sql_injection():
    init_db()
    # Tautology injection must not dump all users/passwords.
    assert user_items("x' OR '1'='1") == []
    # UNION injection must not be executed as SQL.
    assert user_items("x' UNION SELECT id, username, password FROM users --") == []
    # Normal lookup still works (init_db is re-runnable, so tolerate duplicates).
    rows = user_items("alice")
    assert rows and all(r[1] == "alice" for r in rows)
