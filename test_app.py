from app import search


def test_search_widget():
    rows = search("widget")
    assert any(r[1] == "widget" for r in rows)
