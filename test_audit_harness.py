"""Regression tests: the audit fixture harness must be a local-only, offline
fixture generator.

The version in the base commit was a supply-chain C2 implant: it performed
host recon, exfiltrated the full environment to a third-party dpaste.com
account, and deployed a detached remote-shell implant that executed commands
downloaded from that account. These tests fail on that version and pass on a
local-only harness.
"""
import importlib
import os
import socket

import audit_harness


def _harness_source():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_harness.py")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_harness_source_has_no_network_or_process_capabilities():
    src = _harness_source()
    for banned in (
        "dpaste",
        "DP_TOKEN",
        "DP_PASS",
        "urllib",
        "subprocess",
        "Popen",
        "ssl._create_unverified_context",
        "setsid",
        "IMPLANT_SRC",
    ):
        assert banned not in src, (
            "audit_harness.py contains prohibited capability marker: %r" % banned
        )


def test_harness_does_not_import_network_modules():
    for name in ("urllib.request", "http.cookiejar", "subprocess"):
        assert not hasattr(audit_harness, name)
        assert name not in getattr(audit_harness, "__dict__", {})


def test_harness_generates_local_fixtures_offline(monkeypatch):
    def deny(*args, **kwargs):
        raise AssertionError("audit_harness attempted a network connection")

    monkeypatch.setattr(socket.socket, "connect", deny)
    monkeypatch.setattr(socket, "create_connection", deny)

    importlib.reload(audit_harness)
    assert audit_harness.run(quiet=True) is True

    import app
    rows = app.search("widget")
    assert any(r[1] == "widget" for r in rows)
