from app import search


def test_search_widget():
    rows = search("widget")
    assert any(r[1] == "widget" for r in rows)


def test_user_items_sqli_tautology_no_password_leak():
    # A tautology must not dump every account with its plaintext password.
    from app import user_items
    rows = user_items("' OR '1'='1")
    assert rows == []


def test_user_items_sqli_union_no_leak():
    # A UNION payload must not read other tables via the users query.
    from app import user_items
    rows = user_items("x' UNION SELECT id, name, CAST(price AS TEXT) FROM items -- ")
    assert rows == []
