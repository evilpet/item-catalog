"""CWE-89 regression tests for user_items().

On the original code these payloads injected SQL and returned other users'
credentials / arbitrary tables. The parameterized query treats the input as a
literal username, so none of these payloads return rows.
"""
from app import user_items


def test_user_items_boolean_injection_returns_no_rows():
    # "OR 1=1" must not dump other users' credentials. 'bob' does not exist,
    # so the parameterized query returns no rows.
    rows = user_items("bob' OR '1'='1")
    assert rows == []


def test_user_items_union_injection_cannot_read_other_tables():
    # A UNION payload must not inject arbitrary rows from other tables.
    rows = user_items("x' UNION SELECT 999, 'INJECTED_FLAG', 42 -- ")
    assert rows == []


def test_user_items_subquery_injection_cannot_exfiltrate():
    # A scalar-subquery UNION payload must not leak secrets from other tables.
    rows = user_items(
        "x' UNION SELECT (SELECT count(*) FROM users), "
        "(SELECT password FROM users WHERE username='alice'), "
        "(SELECT price FROM items WHERE name='widget') -- "
    )
    assert rows == []
