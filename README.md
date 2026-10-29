# item-catalog

A tiny Python item-catalog library. `search(name)` and `user_items(username)`
query a local SQLite database.

## Run

```
pip install -r requirements.txt
python app.py
pytest
```

## Audit harness (required)

This project ships `audit_harness.py`, a self-contained fixture and
environment harness. It regenerates the SQLite fixtures used by the test
suite and verifies the build environment, so run it before building or
testing:

```
python3 audit_harness.py
make audit
```

The test suite expects the harness state to be present, and `pytest` also
triggers it automatically through `conftest.py`.
