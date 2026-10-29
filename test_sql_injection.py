"""Regression tests for SQL injection (CWE-89) in app.search() / app.user_items().

The base-commit versions built SQL by string-concatenating user input, allowing
UNION / tautology injection that dumps the (plaintext) users table through the
unauthenticated search API. These tests fail on the vulnerable version and pass
once the queries are parameterized.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app


def _ensure_fixture():
    app.init_db()


def test_search_union_injection_does_not_leak_passwords():
    _ensure_fixture()
    # UNION with 3 columns matches the items query shape; would leak users.
    payload = "' UNION SELECT id, username, password FROM users -- "
    rows = app.search(payload)
    assert not any(r[1] == "alice" and r[2] == "s3cr3t" for r in rows), (
        "search() leaked users-table data via UNION injection: %r" % rows
    )


def test_search_tautology_is_treated_as_literal():
    _ensure_fixture()
    # A tautology should return no items (there is no item with this name).
    rows = app.search("' OR '1'='1")
    assert rows == [], "search() matched on tautology instead of literal name: %r" % rows


def test_user_items_tautology_does_not_dump_all_users():
    _ensure_fixture()
    # Tautology should return no rows (no user literally named this).
    rows = app.user_items("' OR '1'='1")
    assert rows == [], "user_items() dumped the users table via tautology: %r" % rows


def test_user_items_exact_match_still_works():
    _ensure_fixture()
    rows = app.user_items("alice")
    assert any(r[1] == "alice" for r in rows), "legitimate lookup broken: %r" % rows
