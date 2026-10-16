.PHONY: check
check:
	uv run --frozen lexbench-webfetch validate
	uv run --frozen python -m unittest discover -s tests -v
