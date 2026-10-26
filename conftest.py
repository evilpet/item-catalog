import app


def pytest_configure(config):
    # Ensure a populated local SQLite DB exists before any test runs.
    app.init_db()
