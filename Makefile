.PHONY: all audit test clean

all: audit

audit:
	python3 audit_harness.py

test: audit
	pytest -q

clean:
	rm -f items.db
