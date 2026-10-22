# Contributing

Task definitions and acceptance requirements belong here. Task models, acceptance scoring, file checks and compilation also belong here. Browser adapters, scheduling, reference-capture orchestration and report rendering belong in the selected execution harness. Include a task ID and a reproducible accepted/rejected example when reporting a rule problem.

Use Python 3.11 or newer and [uv](https://docs.astral.sh/uv/). Run `uv sync --frozen`, then `make check`. Run `uv sync --frozen --extra test` to install the test tools. Tests use synthetic inputs and need no browser, network access or historical source bundle. Keep the English and Chinese READMEs aligned; other guides use English.

A task revision must explain the intended requirement, preserve the prior input version, and include scenarios that should pass and fail. Update the original dataset, catalog, public task definitions, input manifest and registry together after independent source verification. Do not regenerate old hashes to disguise an input correction. Frozen quotes retain their original language.

Keep measured outputs, captures, credentials and internal review notes outside Git. A result proposal must supply the evidence listed in the [protocol](docs/protocol.md); opening a PR does not add it to a leaderboard. See [THIRD_PARTY](THIRD_PARTY.md) before sharing source material.

Site identity patterns, case-specific field layouts and article language labels belong in versioned policy data (`definitions/evaluation/scorer-policy-v1.json`), not Python branches. This compatibility policy preserves the existing frozen input semantics and is included in the scorer fingerprint. Keep existing policy versions immutable after release; intentional matching changes require a new policy version and accepted/rejected controls. Generic HTML/Markdown syntax, ownership, visibility and deduplication remain code. Site-specific selectors and count floors remain in each task contract.
