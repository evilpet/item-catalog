"""Regression test for the SQL injection in app.search() (CWE-89).

Before the fix, the caller-supplied name was concatenated into the SQL
text, so a value like "x' UNION SELECT id, username, password FROM users --"
was executed as SQL. After the fix, the value is bound as a literal
parameter and must simply not match any row.
"""
from app import init_db, search


def test_search_no_sql_injection():
    init_db()
    # UNION injection must not be executed; it is just a literal search term.
    assert search("x' UNION SELECT id, username, password FROM users --") == []
    # Tautology injection must not bypass the equality filter.
    assert search("x' OR '1'='1") == []
    # Normal lookup still works.
    assert any(r[1] == "widget" for r in search("widget"))
