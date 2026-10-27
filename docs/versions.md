# Benchmark versions

A benchmark edition fixes the task population, request contract, acceptance
rules, frozen references and scoring source. Its version is independent of
the Python package version. A package upgrade does not upgrade a report.

Use a readable `MAJOR.MINOR.PATCH` together with immutable SHA-256 bindings.
Keep the exact repository commit in the harness dependency lock. A Git tag
such as `bench-v2.0.1` gives a released commit a durable name; never move
or overwrite a published release tag. A tag alone does not identify external
reference bytes or a report's selected task population.

Create `bench-vMAJOR.MINOR.PATCH` tags only in this benchmark repository.
Browser Eval publishes software versions as `vMAJOR.MINOR.PATCH` and records the
full Git commit for execution and report-building code.
A report names the benchmark edition it uses, and the hosting platform's
immutable version ID identifies each published build. Retain benchmark tags
needed by published reports; do not create report, date or review-checkpoint tags.

| Change | Version | Comparing results |
| --- | --- | --- |
| Documentation or presentation; measurement contracts and scorer unchanged | Patch | Direct, with the same execution controls |
| Reviewed scoring/reference correction; original tasks and requests retained | Minor | Recompute both saved cohorts under one edition before comparison |
| Added/removed tasks, different URLs, requests, output scope or retrieval route | Major | Start a separate benchmark series of results |

A minor version is for correcting the existing measurement, not adding a new
scoring dimension under the same name. Expanding stable-label checks into a
main-content benchmark is a major change. The release tool checks concrete
population and request differences; maintainers still review whether a rule
change preserves the intended task. Existing annotation revisions retain
their independent source evidence and executable correction controls.

## Package versions and release approval

Package versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html): compatible fixes use a patch, compatible CLI or Python API additions use a minor, and incompatible public interfaces use a major. While a package remains `0.x`, use a minor for new functionality or breaking changes and a patch for compatible fixes. Document migrations explicitly.

The package version, benchmark edition and hosted report version are independent. Web Fetch benchmark tags use `bench-vMAJOR.MINOR.PATCH`; Web Search benchmark tags use `bench-MAJOR.MINOR.PATCH`. Both repositories use `vMAJOR.MINOR.PATCH` for tooling-only software releases. Browser Eval uses software tags, since it owns execution and reporting rather than a benchmark catalog. A change to task population can require a major benchmark edition while its software support remains backward compatible. Each repository keeps its own version number and release schedule.

Version changes and tags require an explicit human release request. Documentation edits, routine fixes, synchronization and report rebuilds do not automatically bump versions or rewrite a frozen catalog. Release from a reviewed, merged commit after code, catalog and installed-package checks pass. Preserve all existing tags and exact bindings; a readable tag is not a substitute for input or scorer hashes.


## Freeze an edition

`lexbench-webfetch version` checks the installed catalog's complete suite list,
task definitions and frozen reference bindings. When its scorer matches the
published catalog, it returns that edition. A changed scorer returns
`status: "unreleased"`, its source hash, and the unchanged `published_catalog`;
it has no release version or tag until an explicit release.

The published tag fixes the catalog. Full reference inputs remain separately
hash-bound. A report binds its selected population with the sidecar below;
installing a newer catalog never expands that population.

Compile or export the inputs through their existing owner first, including any
registered annotation revision. Freeze the complete selected population before
provider calls:

```sh
uv run --frozen lexbench-webfetch release \
  --dataset /absolute/inputs/dataset.json \
  --output /absolute/inputs/benchmark-release.json \
  --benchmark lexbench-webfetch --version 2.0.1 \
  --scorer-revision <full-40-character-scorer-commit>
```

For a successor, add `--previous /absolute/previous/benchmark-release.json`.
The scorer commit locates the code; the independently computed scoring-source
hash fixes the actual evaluator bytes. Scoring corrections also require a
concrete `--change-note`. The tool rejects
an insufficient version bump and an existing output path. Keep the sidecar
alongside frozen inputs, outside Git. It contains no provider measurements or
local paths. Commit reusable definitions and publish the code through the
normal feature-branch and release process.

```sh
uv run --frozen lexbench-webfetch compare-releases \
  /absolute/old/benchmark-release.json /absolute/new/benchmark-release.json
```

The result is `direct`, `rescore` or `separate`. It checks actual contract
fingerprints in addition to version numbers. Reusing the same version for a
different measurement is an error. A different major edition stays separate
even if some task IDs overlap. An overlap analysis may be diagnostic, but it
does not make the two full-population percentages comparable.

Before publishing a benchmark tag after a squash merge, update the catalog's
`scorer_revision` in a follow-up PR to the full merged commit containing the
scorer. Verify that its scoring-source hash matches the catalog and run
`lexbench-webfetch version`. Do not point new scorer bytes at an old main commit
or publish the tag while the locator still depends on the discarded branch.

## Reports and retained calls

Report builds retain the selected edition, dataset digest and per-result
scoring-source identities. Rebuilding presentation preserves that edition.
Scoring corrections create a new edition and result revision, retaining the
previous report. Do not replace task inputs from an installed package merely
because it is newer.

For a minor correction, reuse successful and failed saved outputs wherever
the original request contract still applies, and recompute their scores under
one scorer. Changed requests need new calls for the affected scope. Preserve
all physical attempts and use the existing final-attempt selection policy.
Execution budgets, method configurations and timing comparability remain
owned by the harness; a matching dataset edition does not establish those.

Historical reports without a readable edition keep their existing exact hash
bindings. Naming one does not change its task snapshot, results, permissions
or original scoring source. Never label a historical subset as the latest
full dataset.
