.PHONY: check
check:
	uv run --frozen lexbench-webfetch validate
	uv run --frozen --extra test python -m pytest tests -q
