UV ?= uv
BENCH_PYTHON ?= $(shell cat .python-version)
PY := $(UV) run --frozen --extra test --python "$(BENCH_PYTHON)" python

.PHONY: check test package-check
check: test
	$(PY) -m lexbench_webfetch.cli validate

test:
	$(PY) -m pytest tests -q

package-check:
	@set -eu; \
	dist="$$(mktemp -d)"; run="$$(mktemp -d)"; \
	trap 'rm -rf "$$dist" "$$run"' EXIT; \
	$(UV) build --sdist --python "$(BENCH_PYTHON)" --out-dir "$$dist"; \
	for source in "$$dist"/*.tar.gz; do $(UV) build "$$source" --wheel --python "$(BENCH_PYTHON)" --out-dir "$$dist"; done; \
	$(UV) venv --python "$(BENCH_PYTHON)" "$$run/venv"; \
	set -- "$$dist"/lexbench_webfetch-*.whl; \
	$(UV) pip install --python "$$run/venv/bin/python" "$${1}[test]"; \
	cp -R tests "$$run/tests"; \
	cd "$$run"; \
	$(UV) run --no-project --no-sync --python "$$run/venv/bin/python" python -m pytest tests -q; \
	"$$run/venv/bin/lexbench-webfetch" validate
