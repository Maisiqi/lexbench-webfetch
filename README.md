<div align="center">

<img src="docs/assets/overview.png" alt="LexBench Web Fetch — Measure what comes back." width="100%">

**English** · [简体中文](docs/README.zh-CN.md)

[![CI](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml/badge.svg)](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-51735b)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-356a91)](pyproject.toml)

[Tasks](#task-suites) · [Quickstart](#quickstart) · [Scoring](#score-an-answer) · [Versions](#versions) · [Related projects](#related-repositories) · [Contributing](CONTRIBUTING.md)

</div>

LexBench Web Fetch defines 550 Web Fetch tasks and scores returned page text, records with usable links, resources and files. Use the tasks with your own runner or [Browser Eval](https://github.com/lexmount/browser-eval) to compare browsers, extraction tools and hosted services.

This repository owns the task definitions, acceptance rules and frozen input bindings. Browser Eval owns provider calls, timing, evidence and comparison reports.

## Task suites

| Suite | Tasks | Scope |
| --- | ---: | --- |
| `webfetch` | 150 | Web pages, documents, images, video and challenge pages |
| `dynamic-content` | 100 | Content and records loaded after the initial response |
| `popular-sites` | 100 | Content on widely used websites |
| `access-restrictions` | 100 | URLs with previously observed access restrictions |
| `articles` | 100 | Article bodies, initial comments and post collections |

The catalog contains 550 task entries across five suites. Public definitions include task instructions and acceptance rules; complete frozen reference inputs must be obtained separately. See [sample composition and scoring coverage](docs/data.md#dataset-composition-and-scoring-coverage), [data and access](docs/data.md) and [article requirements](src/lexbench_webfetch/definitions/evaluation/articles/README.md).

## Quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
git clone https://github.com/lexmount/lexbench-webfetch.git
cd lexbench-webfetch
uv sync --frozen
uv run --frozen lexbench-webfetch list
uv run --frozen lexbench-webfetch validate
```

These commands check the bundled definitions offline, without a browser or API key.

To export a suite, obtain the frozen files listed in its input manifest and run:

```sh
uv run --frozen lexbench-webfetch export \
  --suite webfetch --source /absolute/path/approved-inputs \
  --output /absolute/path/new-input-directory
```

Export verifies the input hashes and writes the declared files to a new directory. Full reference captures are not distributed in this repository; there is currently no public input bundle. The [data guide](docs/data.md) describes required files and access.

Reviewed scoring corrections are selected explicitly with `--revision`; external review evidence is optional via `--review-source`. Missing evidence is reported as unverified, not passed. See [annotation revisions and scoring details](docs/data.md) and the [550-case rule revision](docs/review-550-decisions.md). These revisions do not certify historical scores.

## Score an answer

Try an accepted and a rejected saved response:

```sh
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/answer.txt
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/missing.txt
```

For real evaluations, use the complete task from a verified dataset. Add `--metadata metadata.json` for structured response fields, or `--file /absolute/path/file` for delivered files. Scoring requirements and result reporting are described in the [evaluation protocol](docs/protocol.md).

## Run browsers and build reports

Follow the [Browser Eval integration guide](https://github.com/lexmount/browser-eval/blob/main/docs/benchmarks.md) to run exported tasks against browsers or services and build comparison reports. Provider accounts, API keys and measured outputs belong to the execution environment. The commands above validate and score saved inputs without calling providers.

## Versions

The current full catalog is benchmark edition `2.0.1` (`bench-v2.0.1`), with 550 entries. The Python tooling package is `0.3.0`. These versions identify different things: the edition fixes tasks, references and scoring; the package versions the commands and Python implementation.

Run `uv run --frozen lexbench-webfetch version` to verify the installed catalog. Use `release` to freeze the exact selected tasks and scorer in `benchmark-release.json`, and `compare-releases` to check whether results can be compared directly, need rescoring or belong to separate populations. Installing a newer package leaves an existing report's edition unchanged. See [versioning](docs/versions.md) for commands and change rules.

## Related repositories

| Repository | Role |
| --- | --- |
| [Browser Eval](https://github.com/lexmount/browser-eval) | Browser/provider execution, saved evidence and comparison reports |
| [LexBench Web Search](https://github.com/lexmount/lexbench-websearch) | Search queries, source references and retrieval scoring |
| [Moli](https://github.com/lexmount/moli) | Browser that can be evaluated with these tasks |
| [WebFetch CLI](https://github.com/lexmount/webfetch-cli) | CLI client for the Lexmount WebFetch service |
| [Artifact Site](https://github.com/lexmount/artifact-site) | Hosting, versioning and sharing of generated reports |
| [Lexbench-Headless-Browser](https://github.com/lexmount/Lexbench-Headless-Browser) | Protocol, automation-driver and web-platform benchmarks |

[Third-party notices](THIRD_PARTY.md) list scoring dependencies and source rights. WebMainBench, WCXB and WebArena are separate benchmarks; they are not part of this 550-entry catalog.

## Contribute

Read [CONTRIBUTING](CONTRIBUTING.md) before changing task requirements or scoring. Run `make check` to validate definitions and tests.

[Security](SECURITY.md) · [Third-party content](THIRD_PARTY.md) · [Apache 2.0](LICENSE)

## Cite LexBench Web Fetch

Use this citation or [CITATION.cff](CITATION.cff), and record the benchmark edition, suites and code revision used. The citation below identifies the tooling package; the catalog edition is `2.0.1`.

```bibtex
@software{lexbench_webfetch_2026,
  author = {{LexBench Web Fetch contributors}},
  title = {LexBench Web Fetch},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/lexmount/lexbench-webfetch}
}
```
