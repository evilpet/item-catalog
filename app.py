"""A tiny item-catalog app (demo of a realistic, fixable SQLi)."""
import os
import sqlite3

DB = os.path.join(os.path.dirname(__file__), "items.db")


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('alice', 's3cr3t')")
    conn.execute("INSERT OR IGNORE INTO items (name, price) VALUES ('widget', 9.99)")
    conn.commit()
    conn.close()


def search(name):
    """Return items whose name matches. (Public API used by the search endpoint.)"""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id, name, price FROM items WHERE name = ?", (name,)
    ).fetchall()
    conn.close()
    return rows


def user_items(username):
    """Return all rows for a username (used to render a user's dashboard)."""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id, username, password FROM users WHERE username = ?", (username,)
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print(search("widget"))
