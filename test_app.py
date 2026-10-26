from app import search


def test_search_widget():
    rows = search("widget")
    assert any(r[1] == "widget" for r in rows)


def test_search_sqli_union_no_leak():
    # A SQL injection payload must not leak rows from other tables (users).
    rows = search("' UNION SELECT id, username, password FROM users -- ")
    assert rows == []


def test_search_sqli_tautology_no_bypass():
    # A tautology must not bypass the filter to return unrelated items.
    rows = search("widget' OR '1'='1")
    assert rows == []
