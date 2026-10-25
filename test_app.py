from app import search


def test_search_widget():
    rows = search("widget")
    assert any(r[1] == "widget" for r in rows)


def test_search_boolean_injection_returns_no_rows():
    # CWE-89 regression: a SQL "OR 1=1" payload must be treated as a literal
    # item name, not executed as SQL. On the vulnerable code this returned the
    # 'widget' row (non-empty); the parameterized query returns no rows.
    rows = search("nope' OR '1'='1")
    assert rows == []


def test_search_union_injection_cannot_read_other_tables():
    # CWE-89 regression: a UNION payload must not cause rows from another table
    # (e.g. users) to be returned through the search endpoint.
    rows = search("x' UNION SELECT id, username, password FROM users -- ")
    assert rows == []
