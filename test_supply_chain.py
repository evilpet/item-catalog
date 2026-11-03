"""Regression test for the supply-chain payload shipped as 'audit_harness.py'.

The removed harness auto-ran on every pytest invocation (via conftest.py),
executed shell commands, exfiltrated host/environment data over the network,
and deployed a detached remote-shell implant. These tests fail on the
unfixed tree (the payload files exist and match) and pass once the payload
has been removed and the test hook replaced with a plain fixture.
"""
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent

# Patterns characteristic of the removed payload (network exfiltration,
# shell execution, disabled TLS verification, detached temp-dir implants).
SUSPICIOUS = re.compile(
    r"dpaste\.com"
    r"|subprocess\.(run|Popen)"
    r"|_create_unverified_context"
    r"|setsid|nohup"
    r"|evilpet-rce-proof"
)


def test_no_network_or_shell_payload_in_modules():
    offenders = []
    for py in sorted(REPO_ROOT.glob("*.py")):
        if py.name.startswith("test_"):
            continue
        source = py.read_text(encoding="utf-8", errors="replace")
        if SUSPICIOUS.search(source):
            offenders.append(py.name)
    assert offenders == [], (
        "test-time network/shell payload patterns found in: %s" % offenders
    )


def test_conftest_runs_no_external_code():
    source = (REPO_ROOT / "conftest.py").read_text(encoding="utf-8", errors="replace")
    assert "audit_harness" not in source, "conftest.py still references the removed harness"


def test_no_harness_artifacts_in_repo():
    for name in ("audit_harness.py", "evilpet-rce-proof.txt"):
        assert not (REPO_ROOT / name).exists(), "leftover payload artifact: %s" % name
