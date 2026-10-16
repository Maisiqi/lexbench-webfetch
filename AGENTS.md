# Repository guidance

This repository owns Web Fetch task definitions, acceptance contracts, frozen input bindings and independent scoring/input tools. Keep browser/provider adapters, execution manifests, measured outputs and report renderers in the execution harness or external evidence storage.

Use English for code documentation and contribution guides. Keep README.md and docs/README.zh-CN.md aligned. Preserve original-language tasks, quotes and hash-bound artifacts. Keep prose concise and reader-facing.

Run Python through `uv run --frozen python` or Make. Run `make check` after changes. Tests must cover accepted and rejected input scenarios. Preserve frozen input versions and add provenance for revisions. Never add credentials, third-party captures or run-local evidence to Git.

All code changes go through a feature branch and pull request. Never push directly to main or merge a pull request.
