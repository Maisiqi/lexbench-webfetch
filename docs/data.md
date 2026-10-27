# Data layout and rights

The suite registry is `src/lexbench_webfetch/definitions/registry.json`. Its suite directories contain the current inputs. It binds every shipped suite file by SHA-256 and records each population's ID and size.

| File within a suite | Role |
| --- | --- |
| `tasks.json` | Public task instructions and acceptance requirements, with body-reference text replaced by SHA-256/character-count bindings, and no full reference bodies or capture logs |
| `dataset-catalog.json` | Original ordered task inventory, source URLs and complete task-definition hashes |
| `source-inputs.json` | Exact executable dataset and external reference-file hashes |

The initial versions were imported from Browser Eval commit `894b38f8`. The current access-restriction suite selects the later frozen version declared in the registry. Source commits and per-file hashes are in `provenance.json`. Original catalog and manifest bytes are retained, including original dataset IDs and task languages. Their names may contain historical method labels; those labels identify frozen input versions and confer no method-specific acceptance exception.

Public task requirements are maintained in this repository. Frozen historical catalogs and manifests also live under `definitions/evaluation/` with their original relative paths and bytes. Browser Eval resolves its historical logical paths through this installed package. It retains experiment profiles and compact hash bindings, rather than duplicate definition files.

## Dataset composition and scoring coverage

Edition: the registered frozen suites in `registry.json`; revised edition:
`review-550-20261023`. The tables compare declarations under the current scorer,
not results from an older scorer or provider runs. Suite links open maintained
baseline contracts; [revision operations](../src/lexbench_webfetch/definitions/annotation-revisions/review-550-20261023.json)
contain changed rules and shared fixed-record contracts.

<!-- distribution:start -->
### Sample composition

Counting unit: registered case entry; percentages use the suite row total (combined row: 550).
Delivery categories partition entries. Frozen baseline and selected revision have identical composition.

| Suite | Total | Body | Structure | Resource discovery | File delivery | Unique URLs | Unique URL + prompt tasks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [webfetch](../src/lexbench_webfetch/definitions/evaluation/tasks.json) | 150 | 121 (80.7%) | 10 (6.7%) | 16 (10.7%) | 3 (2.0%) | 150 | 150 |
| [popular-sites](../src/lexbench_webfetch/definitions/evaluation/popular-sites/tasks.json) | 100 | 0 (0.0%) | 100 (100.0%) | 0 (0.0%) | 0 (0.0%) | 100 | 100 |
| [dynamic-content](../src/lexbench_webfetch/definitions/evaluation/dynamic-content-100-moli-webfetch/tasks.json) | 100 | 88 (88.0%) | 12 (12.0%) | 0 (0.0%) | 0 (0.0%) | 100 | 100 |
| [access-restrictions](../src/lexbench_webfetch/definitions/evaluation/risk-control/current/tasks.json) | 100 | 100 (100.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 100 | 100 |
| [articles](../src/lexbench_webfetch/definitions/evaluation/articles/tasks.json) | 100 | 100 (100.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 100 | 100 |
| Combined | 550 | 409 (74.4%) | 122 (22.2%) | 16 (2.9%) | 3 (0.5%) | 535 | 540 |

Across suites: **10 exact URL + prompt identities**, represented by **20 entries** (**10 repeated entries**). URL-only uniqueness does not establish task equivalence; different prompts on one URL remain different tasks. Equality uses stored strings, with no URL canonicalization.

### Scoring component matrix

Each cell is **covered cases (percentage of suite entries); declared checkpoints**. An arrow means **frozen baseline → selected revision**; unchanged cells appear once. Components overlap and must not be added into a total case count. A zero means no executable declaration in that component, not a measured failure.

| Component | webfetch | popular-sites | dynamic-content | access-restrictions | articles | Combined |
| --- | --- | --- | --- | --- | --- | --- |
| [Required facts](../src/lexbench_webfetch/metrics.py) | 121 (80.7%); 686 → 111 (74.0%); 433 | 0 (0.0%); 0 | 47 (47.0%); 452 → 34 (34.0%); 107 | 0 (0.0%); 0 → 3 (3.0%); 22 | 0 (0.0%); 0 | 168 (30.5%); 1138 → 148 (26.9%); 562 |
| [Diagnostic historical facts](../src/lexbench_webfetch/metrics.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |
| [Required legacy marker groups](../src/lexbench_webfetch/metrics.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |
| [Required stable anchors](../src/lexbench_webfetch/stable_tasks.py) | 99 (66.0%); 391 → 91 (60.7%); 284 | 100 (100.0%); 2022 → 100 (100.0%); 2052 | 100 (100.0%); 2367 → 83 (83.0%); 2173 | 98 (98.0%); 1553 → 100 (100.0%); 1587 | 100 (100.0%); 3970 → 100 (100.0%); 4229 | 497 (90.4%); 10303 → 474 (86.2%); 10325 |
| [Diagnostic stable anchors](../src/lexbench_webfetch/stable_tasks.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 2 (2.0%); 33 → 0 (0.0%); 0 | 0 (0.0%); 0 | 2 (0.4%); 33 → 0 (0.0%); 0 |
| [Body regions](../src/lexbench_webfetch/body_coverage.py) | 27 (18.0%); 123 → 86 (57.3%); 417 | 0 (0.0%); 0 | 42 (42.0%); 151 → 42 (42.0%); 143 | 79 (79.0%); 296 → 79 (79.0%); 293 | 95 (95.0%); 418 | 243 (44.2%); 988 → 302 (54.9%); 1271 |
| [Article endings](../src/lexbench_webfetch/body_coverage.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 95 (95.0%); 95 | 95 (17.3%); 95 |
| [Ordered article endings](../src/lexbench_webfetch/body_coverage.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 → 95 (95.0%); 95 | 0 (0.0%); 0 → 95 (17.3%); 95 |
| [Required text patterns](../src/lexbench_webfetch/metrics.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 2 (2.0%); 2 | 0 (0.0%); 0 | 0 (0.0%); 0 | 2 (0.4%); 2 |
| [Required page patterns](../src/lexbench_webfetch/stable_tasks.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 2 (2.0%); 8 → 3 (3.0%); 9 | 1 (1.0%); 1 | 100 (100.0%); 101 | 103 (18.7%); 110 → 104 (18.9%); 111 |
| [Fixed name/URL pairs](../src/lexbench_webfetch/stable_tasks.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |
| [Named-link collections](../src/lexbench_webfetch/stable_tasks.py) | 10 (6.7%); 10 → 22 (14.7%); 31 | 43 (43.0%); 43 → 61 (61.0%); 66 | 32 (32.0%); 32 | 18 (18.0%); 24 → 21 (21.0%); 28 | 0 (0.0%); 0 | 103 (18.7%); 109 → 136 (24.7%); 157 |
| [Typed record/table fields](../src/lexbench_webfetch/stable_tasks.py) | 10 (6.7%); 26 | 0 (0.0%); 0 → 1 (1.0%); 2 | 31 (31.0%); 110 → 37 (37.0%); 150 | 12 (12.0%); 52 → 14 (14.0%); 62 | 0 (0.0%); 0 | 53 (9.6%); 188 → 62 (11.3%); 240 |
| [Composite groups](../src/lexbench_webfetch/composite_tasks.py) | 0 (0.0%); 0 → 12 (8.0%); 21 | 0 (0.0%); 0 → 3 (3.0%); 8 | 0 (0.0%); 0 → 5 (5.0%); 8 | 22 (22.0%); 29 → 25 (25.0%); 33 | 0 (0.0%); 0 | 22 (4.0%); 29 → 45 (8.2%); 70 |
| [Document sections](../src/lexbench_webfetch/document_structure.py) | 0 (0.0%); 0 → 10 (6.7%); 104 | 0 (0.0%); 0 → 5 (5.0%); 40 | 0 (0.0%); 0 | 0 (0.0%); 0 → 1 (1.0%); 3 | 0 (0.0%); 0 | 0 (0.0%); 0 → 16 (2.9%); 147 |
| [Definition terms](../src/lexbench_webfetch/document_structure.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |
| [Article title groups](../src/lexbench_webfetch/article_title.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 90 (90.0%); 90 | 90 (16.4%); 90 |
| [Comment contracts](../src/lexbench_webfetch/article_comments.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 20 (20.0%); 20 | 20 (3.6%); 20 |
| [Post contracts](../src/lexbench_webfetch/article_posts.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 5 (5.0%); 5 | 5 (0.9%); 5 |
| [Fixed source record hashes](../src/lexbench_webfetch/stable_tasks.py) | 0 (0.0%); 0 → 10 (6.7%); 133 | 0 (0.0%); 0 | 0 (0.0%); 0 → 10 (10.0%); 133 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 → 20 (3.6%); 266 |
| [Resource groups](../src/lexbench_webfetch/resource_urls.py) | 16 (10.7%); 19 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 16 (2.9%); 19 |
| [File integrity contracts](../src/lexbench_webfetch/file_acceptance.py) | 3 (2.0%); 3 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 3 (0.5%); 3 |
| [Content character floors](../src/lexbench_webfetch/metrics.py) | 121 (80.7%); 121 | 0 (0.0%); 0 → 4 (4.0%); 4 | 92 (92.0%); 92 | 100 (100.0%); 100 | 100 (100.0%); 100 | 413 (75.1%); 413 → 417 (75.8%); 417 |
| [Lexical exclusion terms](../src/lexbench_webfetch/metrics.py) | 150 (100.0%); 689 → 0 (0.0%); 0 | 100 (100.0%); 659 → 0 (0.0%); 0 | 75 (75.0%); 374 → 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 325 (59.1%); 1722 → 0 (0.0%); 0 |
| [Required page identity](../src/lexbench_webfetch/scoring.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |
| [Legacy list contracts](../src/lexbench_webfetch/dynamic_lists.py) | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 | 0 (0.0%); 0 |

### Threshold changes

Values are declared thresholds across all suites (absent values excluded); changed cases include additions/removals. For more than six values, show the range and distinct-value count. Nested composite-group quotas remain in the linked per-task definitions.

| Declaration | Baseline values | Revised values | Changed cases |
| --- | --- | --- | ---: |
| `body_requirements.minimum_coverage` | 0.8: 243 cases | 0.8: 302 cases | 59 |
| `body_requirements.minimum_floor` | 0.6: 148 cases, 0.8: 95 cases | 0.8: 302 cases | 207 |
| `body_requirements.minimum_region_passes` | 1: 30 cases, 2: 38 cases, 3: 25 cases, 4: 79 cases, 5: 71 cases | 1: 16 cases, 2: 22 cases, 3: 39 cases, 4: 31 cases, 5: 194 cases | 188 |
| `body_requirements.version` | 3: 148 cases, 4: 95 cases | 3: 207 cases, 5: 95 cases | 154 |
| `acceptance_contract.minimum_records` | 0–100 (25 values; 502 cases) | 0–200 (33 values; 501 cases) | 27 |
| `acceptance_contract.maximum_records` | not declared | not declared | 0 |
| `acceptance_contract.record_count_policy.required_ratio` | 0.8: 36 cases, 1.0: 11 cases | 0.8: 63 cases, 1.0: 21 cases | 37 |
| `document_structure.minimum_heading_coverage` | not declared | 0.8: 8 cases, 1.0: 8 cases | 16 |
| `document_structure.minimum_body_chars` | not declared | 1–5138 (10 values; 16 cases) | 16 |
| `document_structure.minimum_section_chars` | not declared | 4: 1 cases, 19: 1 cases, 20: 3 cases | 5 |

Baseline unavailable rule declarations: 0.

Revision unavailable rule declarations: 0.

<!-- distribution:end -->

### Counting and acceptance rules

Regenerate with `uv run --frozen python docs/data_distribution.py --write`;
verify with `uv run --frozen python docs/data_distribution.py --check`.
The normal test suite checks totals and documentation drift. This small script
reads registered definitions and applies the revision; it performs no fetching.

A checkpoint is one fact/anchor alternative group, body region, ending,
pattern, named-link collection, fixed name/URL pair, typed field/column, composite group,
section/definition term, source-record hash or resource group. Alternative
spellings do not count as separate checks. A title/comment/post/file contract
counts once; its required record count is a threshold, not additional declared
checkpoints. Typed fields are counted once per collection, not multiplied by
returned rows. Composite groups and their fields/links deliberately overlap.

- **Facts, anchors and patterns:** normalized literal alternatives are checked
  as groups. Required fact coverage uses the task's `fact_coverage_threshold`
  (default 1); required anchors and patterns must all pass. Stable page-pattern groups are also mandatory. Structured-record
  schemas obey declared facts too under the unified main scorer. This revision
  replaces redundant facts in 20 fixed-record cases with stronger complete-source
  membership. Among the other 16 structured cases, 13 duplicate fact groups in
  six cases are already required by identical stable anchors and are deduplicated;
  all nonduplicate facts remain mandatory. No fact-only diagnostic role exists in this scorer.
  The two baseline diagnostic anchor roles are replaced by explicit required
  groups: Devuan retains all 20; ibiblio retains 11 source-present groups and
  removes two obsolete ones. Diagnostic anchor support remains for frozen inputs,
  but no selected-revision case uses it.
- **Bodies and endings:** declared regions use `minimum_coverage`, the floor
  and required-region count in `body_requirements`. This revision sets the 148
  revised body contracts to 80% per region. The 95 article bodies also require
  80% ending similarity, with order enforced in the revision. Endings may occur
  before a footer; absent regions cannot borrow credit from stronger regions.
- **Named and typed records:** records must own their names, links and fields,
  meet declared URL/scope/type rules and `minimum_records`, plus any maximum,
  duplicate or field-specific quotas. Fixed count policies use the observed
  count; variable count policies use the declared ratio rounded up. Count policy
  is separate from source membership: only explicit fixed membership binds
  complete record-field hashes. Changing lists are not required to repeat old
  members. All composite groups must independently meet their thresholds.
- **Sections and definitions:** count matched headings with locally owned body
  text (unless explicitly waived), then require `minimum_heading_coverage`,
  `minimum_section_chars` and `minimum_body_chars`. No whole-section prose match
  is implied. Per-task floors and headings are in the linked contracts.
- **Article components:** required title alternatives, comment ownership and
  `minimum_comments`, and post ownership/permalinks and `minimum_posts` must
  pass alongside the base content checks. They are not optional diagnostics.
- **Resources and files:** resource tasks check declared acceptable URLs/groups
  and output scope; unexpected resources follow the explicit output policy.
  File delivery requires actual bytes, recognized signature, minimum byte size,
  and declared MIME/hash constraints. A URL alone is not a delivered file.
- **Shared verdict:** request success is required. Any enabled mandatory document,
  page-identity or article component must pass. Stable contracts combine with
  every declared fact, literal, length, body, pattern, composite, resource and
  file requirement through `acceptance_checks`; the task kind cannot bypass
  another declared requirement. Undeclared requirements are omitted. Deadline
  overrun fails.
  Encoding corruption, script-only shells and declared truncation have shared
  scorer guards; these are not separate sampled components. A truncation notice
  can be overridden only by exact coverage of every declared body region.
  All revised lexical vetoes are removed; extra notices do not independently fail.
- **Unavailable and diagnostics:** unresolved rules and missing file verification
  are unmeasured, not passing results. Missing required page-identity evidence
  fails that required check. Optional page language/redirect measurements and
  runtime word-overlap diagnostics are not acceptance coverage. Zero declaration,
  an inapplicable component and an attempted check that fails are distinct.

The matrix shows covered-case and checkpoint changes, including removal of
lexical vetoes and the new explicit fixed-source membership. Unchanged coverage
counts do not imply unchanged thresholds or scope: article order, body floors,
record quotas and selection scopes also change. See the
[review decisions](review-550-decisions.md) for those source-qualified changes.
Declared coverage does **not** establish source qualification, historical-output
review, provider pass rates or successful frozen exports. The four full exports
remain deferred; these statistics do not fill that evidence gap.

## External inputs

An approved input directory contains the exact `dataset.json` and, when listed by the manifest, `sources/` and `list-references/` files. `verify-inputs` checks every declared file, the full dataset hash, ordered complete task-definition hashes and public requirements. `export` verifies the source, copies only declared files into a new directory and verifies the copy. Unlisted files are ignored and never exported. No provider calls or downloads occur.

The exported directory intentionally has no `source-inputs.json`: it is a directly materialized, verified input tree. Browser Eval can consume its dataset through `--dataset` without relying on Browser Eval's historical storage paths. Keep the suite manifest and benchmark revision with your experiment metadata.

Complete third-party text, PDFs, media, rendered pages and provider outputs are excluded from this repository. Obtain required inputs under their original terms. There is currently no hosted public input bundle; the public definitions can be inspected independently, while exact historical runs require separately acquired matching inputs. A new capture is a new version and must not be presented as the old frozen suite.

## Score-only annotation versions

Frozen `tasks.json`, catalogs and input manifests retain their original bytes.
Corrections live in `definitions/annotation-revisions/` with a distinct revision
ID, parent task and source-manifest hashes, per-task predecessor hashes and
registered scoring controls. They change acceptance annotations, not collection
URLs, prompts or saved provider outputs.

To export a corrected definition, select its version explicitly:

```sh
uv run --frozen lexbench-webfetch export --suite webfetch --source /path/to/frozen-inputs --output /path/to/new-inputs --revision serialization-20261021
```

The exported dataset receives a new ID and a `definition_revision` binding.
Without `--revision`, export reproduces the original frozen dataset exactly.
A score recomputed with revised annotations must retain both definition hashes
and its original call identities; it is not a new browser run.

Use `acceptance_patch` to change an existing contract without copying unchanged
fields. Its `set` and `remove` fields edit contract properties; `anchors` can
`replace` or `remove` existing IDs and `append` new IDs. Existing order is
preserved. Missing, duplicate or conflicting targets fail. Do not combine a
patch with replacement or removal of the same contract. The frozen task hash
and per-case review hash still bind the complete resulting rule change.

A revision may define `shared_acceptance_contracts` and reference one with
`acceptance_contract_ref` on each identical task's change. References cannot
be combined with a patch, replacement or removal of that contract. Each
expanded change retains its independent frozen-parent and review bindings.

Structured records can declare `source_membership`: `fixed` binds sorted field
names and SHA-256 hashes of normalized complete field tuples; `changing` binds
no historical records. Fixed membership rejects fabricated or mispaired fields,
independently of record counts. Normalization uses existing matching rules,
including compact spaces for name/description records. This is source-record
identity, not a semantic truth check. Undeclared membership keeps prior behavior.
The ten duplicate practice tasks share fixed contracts; no global historical
fact requirement is added to changing lists. All revised tasks omit lexical
`forbidden_any` vetoes; complete content with extra notices may pass.

The `review-550-20261023` revision changes quotas on 148 existing body
contracts across webfetch, dynamic-content and access-restrictions. Every region
must reach 80%; it preserves all reference bindings, region boundaries and URLs.
Its `body_thresholds` operation accepts only `minimum_coverage`, `minimum_floor`
and `minimum_region_passes` for existing version-3/4/5 bodies. It operates equally
on public hash bindings and executable text, so no captured body is embedded in
the revision. Version-4/5 ending requirements cannot be weakened by this operation.
Per-case review hashes cover the resulting field differences and executable
controls cover complete, boundary, weak-region and missing-region responses.

For articles, `review-550-20261023` upgrades the 95 fixed bodies from
version 4 to 5 with `body_ending_order: true`. Reference text, region boundaries,
the existing fragment gates and the five collection contracts remain unchanged.
Version 5 additionally compares the ending against a contiguous response passage
in token order. Insertions, omissions and substitutions each consume one token
of the 20% edit budget; text before or after the passage is free. Latin words and
individual CJK characters use the existing body tokenizer. Thus footers and
formatting are allowed, but distant fragments cannot be assembled into a closing
sentence. This checks an ordered local passage, not its absolute page position
or semantic completeness. It does not repair an incorrectly selected ending.

The `review-550-20261023` revision combines those 148 quota
changes and 95 ordered-ending changes. Five articles also receive source-reviewed
body boundaries, and nine more receive substantive conclusion selections with
their original body regions preserved. Its scope is the explicit per-case
scoring changes in the revision; it does not certify all 550 reference answers
or historical scores. Unresolved source and recognition limitations are listed
in [review decisions](review-550-decisions.md).

The initial review added `document_structure` contracts to 67 documents.
The [2026-10-27 follow-up](document-body-review.md) replaces 59 section/definition
gates with five-region body matching and restores their baseline length floors.
Across all suites, 16 section contracts remain and no definition contract is
currently declared. Retained section contracts require their declared heading
fraction and local/body length floors. Navigation,
table-of-contents entries and headings without their required body cannot fill
the section quota. This checks structural coverage, not semantic accuracy.
Heading IDs default to `section-1`, `section-2`, and so on; `body_required`
defaults to `true`. Explicit IDs and empty-section exceptions remain supported.
Two cases also remove a mandatory phrase proven to be in an initially hidden
tab panel or closed disclosure; all other existing requirements remain.

Other documents from the 82-case review use source-qualified target directories,
resource cards or explicit body facts. The supported definition contract sets
`type: "definition"` (now unused by the selected revision):
signatures need adjacent descriptions (`dt` followed by `dd` in HTML, or complete
signature lines followed by prose in text/Markdown). API names and unrelated
padding do not count as definitions. Existing mandatory facts remain mandatory.

Six dynamic tables replace historical row text with initial-row-count and
visible-field contracts while retaining source-bound static prose. Grouped
tables may explicitly declare caption fields belonging to subsequent rows in
the same table section; expanded ordinary columns remain valid serializations.
No unrendered virtual rows or hidden example code enter the target count.
Composite `table` and `linked_table` groups may explicitly declare
`table_scope: {"exclude_selector": ".auxiliary-details"}` to exclude
source-verified auxiliary HTML nodes before reading cells and links. The option
is limited to tables; absent scopes and Markdown retain their existing behavior.

Additional source observations are declared separately in the revision's
`review_inputs`, mapping each suite to `review-evidence/` paths and SHA-256
digests. Per-case reviews cite these paths explicitly, with
`revision_review_source_declared` distinguishing them from parent inputs.
`--review-source` is optional. Without it, export still verifies every frozen
input and runs available reference controls. Declared review sources are listed
as unavailable; failed available candidates remain recorded. A case with no
passing candidate and omitted review sources is `unavailable`, not `passed`.
An accepted error-page control remains a failure. Supplying `--review-source`
requires every declared review file to match its hash: missing, changed or
symlinked files are rejected, and only declared files are copied. Parent bytes
and source manifests remain unchanged. Export success is not proof that all
reference controls passed; inspect `complete`, `changed_rules_complete` and each
case's verification scope in `annotation-review.json`.


Its `body_projection` operation selects one to five ordered, nonoverlapping
character ranges from the hash-bound original body. Ranges use zero-based,
half-open Python character offsets. The source hash, length and projected text
bindings are verified when exporting executable inputs; the original reference
remains available for historical diagnostics. Attribution, notices and footer
information moved out of prose remain required where applicable.
Version-3 projections retain version 3 and omit the `ending` field; they do not
invent a closing passage for static text accompanying a dynamic collection.
Version-4/5 projections require an ending and produce version 5.

Export qualification distinguishes `full_task`, `body_only` and
`body_and_added_stable_text` controls. A bound body reference can qualify body
changes and strictly appended stable anchors, but cannot certify unchanged page
navigation, comments or other full-page requirements. `changed_rules_complete`
reports qualification of the changed layers; `complete` requires full-task
qualification. Other rule changes still need a full-page reference.

Annotation revisions are alternatives against their declared frozen parent,
not a sequence of cumulative patches. Select and disclose the required revision;
the body-quota revision does not implicitly apply `serialization-20261021`.

## Named-record scope boundaries

`entry_scope.required_end` is an optional boolean, defaulting to false. Setting
it to true requires a nonempty `end_pattern`; text and Markdown answers without
a matching end boundary yield no scoped records. This prevents later page
sections from completing a scoped quota when its boundary is missing. HTML
answers continue to use `html_selector` as their independent boundary. Keep the
default for contracts that intentionally accept an isolated body without its
following section. This option applies to the shared named-record scope and
does not introduce website-specific matching.

## Mixed path and query record identities

Named-link and linked-product contracts may declare a nonempty list of
`identity_query_paths` regular expressions together with `identity_query_keys`.
Patterns match the entire decoded, normalized path with trailing slash removed.
Matching routes require the existing query identity; other routes retain path
identity. For example, `/detail?id=7` can coexist with `/article/8` without
accepting `/detail` as a valid record or counting tracking parameters twice.
Omitting the path policy preserves the existing all-record query requirement.
It cannot be combined with `entry_identity_pattern`, which defines a separate
identity rule. No domain-specific handling is involved.

## Saved answer format

Saved response metadata may declare `answer_format` as `plain_text`, `html`, or
`markdown`. It describes the delivered bytes, not the origin Content-Type.
Plain text preserves literal HTML examples; HTML and Markdown use the visible
content projection. Omission keeps automatic interpretation. Persist the format
with the response and pass it to offline `score --metadata`; an old verdict
cannot supply missing format metadata. Original response bytes, links and file
evidence remain unchanged.

These annotations remain separate from frozen benchmark editions. Use the
[versioning guide](versions.md) to freeze a selected population and scorer or
to compare editions. Neither a package upgrade nor selecting a correction
certifies historical results.

Document structure contracts may set `minimum_section_chars` to require local
alphanumeric content below each required heading (default: 1). This is separate
from the whole-document `minimum_body_chars` floor; another section cannot fill
a missing section's quota. Source-backed floors must preserve legitimate short
content and do not establish semantic equivalence to the source.

Annotation reviews may use a revision-local `shared_reasons` map. A case declares
either an inline `reason` or a `reason_ref`; unknown references, empty reasons and
conflicting declarations are rejected. Exported review records contain the full
resolved reason. Per-case source bindings, change hashes and regression IDs remain
independent.

## Shared scoring impact audit

This inventory scans all 550 frozen task definitions. It describes potential
behavior changes; the saved-output follow-up below reports a partial measured
comparison separately. Frozen tasks and source
bindings are unchanged. The facts gate is a shared behavior correction, not an
annotation-only opt-in: a `body_text` identity anchor can no longer override
already declared `required_facts` or `expected_any`. A missing fact is evaluated
at the case's declared fraction (default 1.0); expected markers retain their
existing any-of semantics. Structured record contracts do not inherit these
gates, since their entries can change over time.

Of 376 frozen `body_text` cases, 104 declare at least one affected requirement:
82 webfetch and 22 dynamic-content cases. The other 272 have no additional fact
or expected-marker requirement from this change. The table lists every affected
case, including cases with an existing threshold; it does not imply that all
104 previously passed bad answers. Length, forbidden-content, reference-body
and revision-specific gates remain separate.

`tests/test_mutable_body_content_gates.py` checks complete and missing content,
4/5 versus 3/5 facts at 80%, missing expected markers, metadata-only facts, no
facts, and structured collections that must not inherit historical markers.

| Suite | Frozen case | Facts | Expected alternatives | Fact threshold |
| --- | --- | ---: | ---: | ---: |
| webfetch | `cowagent-doc` | 3 | 0 | 1 |
| webfetch | `lexmount-doc` | 4 | 0 | 1 |
| webfetch | `github-repository` | 3 | 0 | 1 |
| webfetch | `lm-feishu-help` | 5 | 0 | 1 |
| webfetch | `lm-python-tutorial` | 3 | 0 | 1 |
| webfetch | `lm-node-intro` | 3 | 0 | 1 |
| webfetch | `lm-rust-learn` | 3 | 0 | 1 |
| webfetch | `live-001-python-pathlib-documentation` | 3 | 0 | 1 |
| webfetch | `live-002-http-http-modules` | 3 | 0 | 1 |
| webfetch | `live-003-the-rust-programming-language` | 4 | 0 | 1 |
| webfetch | `live-004-deployments` | 3 | 0 | 1 |
| webfetch | `live-005-python-asyncio-documentation` | 3 | 0 | 1 |
| webfetch | `live-006-python-typing-documentation` | 3 | 0 | 1 |
| webfetch | `live-007-html-hypertext-markup-language-s` | 3 | 0 | 1 |
| webfetch | `live-008-service` | 3 | 0 | 1 |
| webfetch | `live-009-run-a-stateless-application-usin` | 3 | 0 | 1 |
| webfetch | `live-010-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-012-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-013-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-014-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-015-configmaps` | 3 | 0 | 1 |
| webfetch | `live-016-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-017-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-019-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-021-python-common-pathname-manipulations` | 3 | 0 | 1 |
| webfetch | `live-022-until-september-10-get-pycharm-f` | 3 | 0 | 1 |
| webfetch | `live-024-cascading-style-sheets-level-2-r` | 3 | 0 | 1 |
| webfetch | `live-025-api-reference` | 3 | 0 | 1 |
| webfetch | `live-026-getting-started` | 3 | 0 | 1 |
| webfetch | `live-027-sponsors` | 3 | 0 | 1 |
| webfetch | `live-028-getting-started-with-rails` | 3 | 0 | 1 |
| webfetch | `live-029-fetch` | 3 | 0 | 1 |
| webfetch | `live-032-api-reference` | 3 | 0 | 1 |
| webfetch | `live-033-nasa-science` | 3 | 0 | 1 |
| webfetch | `live-035-part-i-tutorial` | 3 | 0 | 1 |
| webfetch | `live-036-build-on-the-openai-api-platform` | 5 | 0 | 1 |
| webfetch | `live-037-breadcrumb` | 11 | 0 | 1 |
| webfetch | `live-039-welcome-to-redis-docs` | 3 | 0 | 1 |
| webfetch | `live-040-documentation-overview` | 3 | 0 | 1 |
| webfetch | `live-041-python-programming-language` | 4 | 0 | 1 |
| webfetch | `live-042-document-object-model-dom` | 3 | 0 | 1 |
| webfetch | `live-043-syntax` | 3 | 0 | 1 |
| webfetch | `live-044-history-api` | 3 | 0 | 1 |
| webfetch | `live-045-cache` | 3 | 0 | 1 |
| webfetch | `live-046-file-api` | 3 | 0 | 1 |
| webfetch | `live-047-push-api` | 3 | 0 | 1 |
| webfetch | `live-048-websocket-api-websockets` | 3 | 0 | 1 |
| webfetch | `live-049-functools-higher-order-functions` | 3 | 0 | 1 |
| webfetch | `live-050-re-regular-expression-operations` | 3 | 0 | 1 |
| webfetch | `live-051-email-an-email-and-mime-handling` | 3 | 0 | 1 |
| webfetch | `live-052-objects-in-kubernetes` | 3 | 0 | 1 |
| webfetch | `live-053-dns-for-services-and-pods` | 3 | 0 | 1 |
| webfetch | `live-054-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-055-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-056-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-057-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-058-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-059-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-060-database` | 3 | 0 | 1 |
| webfetch | `live-061-version-control` | 3 | 0 | 1 |
| webfetch | `live-062-natural-language-processing` | 3 | 0 | 1 |
| webfetch | `live-063-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-064-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-065-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-066-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-067-navigation-menu` | 4 | 0 | 1 |
| webfetch | `live-068-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-069-navigation-menu` | 2 | 0 | 1 |
| webfetch | `live-070-navigation-menu` | 3 | 0 | 1 |
| webfetch | `live-072-python-itertools-documentation` | 3 | 0 | 1 |
| webfetch | `live-073-python-json-documentation` | 3 | 0 | 1 |
| webfetch | `live-074-python-sqlite3-documentation` | 3 | 0 | 1 |
| webfetch | `live-075-python-logging-documentation` | 3 | 0 | 1 |
| webfetch | `live-076-python-unittest-documentation` | 3 | 0 | 1 |
| webfetch | `live-077-python-dataclasses-documentation` | 3 | 0 | 1 |
| webfetch | `live-078-python-collections-documentation` | 3 | 0 | 1 |
| webfetch | `live-079-python-hashlib-documentation` | 3 | 0 | 1 |
| webfetch | `live-080-python-urllib-parse-documentatio` | 3 | 0 | 1 |
| webfetch | `live-081-python-csv-documentation` | 3 | 0 | 1 |
| webfetch | `live-082-python-decimal-documentation` | 3 | 0 | 1 |
| webfetch | `live-083-python-datetime-documentation` | 3 | 0 | 1 |
| webfetch | `live-084-python-concurrent-futures-docume` | 3 | 0 | 1 |
| dynamic-content | `dynamic-057-nutui-jd-com-h5` | 3 | 0 | 1 |
| dynamic-content | `dynamic-019-selenium-dev-selenium` | 2 | 0 | 1 |
| dynamic-content | `dynamic-027-ej2-syncfusion-com-react` | 3 | 0 | 1 |
| dynamic-content | `dynamic-028-ej2-syncfusion-com-react` | 3 | 0 | 1 |
| dynamic-content | `dynamic-040-gridjs-io-docs` | 3 | 0 | 1 |
| dynamic-content | `dynamic-051-youzan-github-io-vant` | 3 | 0 | 1 |
| dynamic-content | `dynamic-054-ant-protable-api` | 3 | 0 | 1 |
| dynamic-content | `dynamic-055-arco-design-vue` | 4 | 0 | 1 |
| dynamic-content | `dynamic-056-vant-ui-github-io-vant` | 3 | 0 | 1 |
| dynamic-content | `dynamic-059-layui-vue-com-zh` | 4 | 0 | 1 |
| dynamic-content | `dynamic-013-en-stable-patternfly-table` | 4 | 0 | 1 |
| dynamic-content | `dynamic-015-015-testpages-iframe-list` | 3 | 0 | 1 |
| dynamic-content | `dynamic-016-en-stable-angular-tree` | 2 | 0 | 1 |
| dynamic-content | `dynamic-018-en-stable-varlet-home` | 4 | 0 | 1 |
| dynamic-content | `dynamic-021-021-scalar-get-operation` | 4 | 0 | 1 |
| dynamic-content | `dynamic-022-en-stable-syncfusion-grid` | 3 | 0 | 1 |
| dynamic-content | `dynamic-034-034-vuetify-server-table` | 2 | 0 | 1 |
| dynamic-content | `dynamic-035-035-vuetify-virtual-table` | 4 | 0 | 1 |
| dynamic-content | `dynamic-039-039-angular-autocomplete-examples` | 4 | 0 | 1 |
| dynamic-content | `dynamic-043-en-stable-grommet-table` | 2 | 0 | 1 |
| dynamic-content | `dynamic-105-blueprint-docs` | 4 | 0 | 1 |
| dynamic-content | `dynamic-107-redoc-cafe-api` | 4 | 0 | 1 |

### Wildcard link identity

Only these frozen composite groups accept arbitrary destination hosts. They now
count distinct canonical destinations instead of differently labelled copies
of one destination. Different hosts remain different destinations. Fragments
and undeclared query parameters do not create additional records; declared
identity query keys do. This affects record counting, not the required quota.
`test_wildcard_links_count_distinct_destinations` covers all four situations.

| Suite | Case | Group | Required distinct destinations |
| --- | --- | --- | ---: |
| access-restrictions | `risk-diverse-248` | `agp-picks` | 8 |
| access-restrictions | `risk-diverse-248` | `perspectify` | 7 |

### Native name/description list ownership

The selected revision contains two `name_description` cases: webfetch and
dynamic-content `dynamic-angular-phones`. Native leaf `li` elements now preserve
record ownership before visible-text flattening. Other schemas and existing
plain-text/Markdown parsing retain their paths. This is a scorer correction, not
a quota or stable-text revision.

The independently saved complete Angular HTML has 20 list items; its SHA-256 is
`f5b9fb1a23f4f23a7a351592f5c617ee9557924bf095cf151bc17204bd45a3e6`.
Both cases pass the complete page. Missing-record and missing-description
controls fail; titles alone cannot supply 20 complete records. Unit controls
also reject duplicate names and hidden items and avoid counting nested list
containers twice. Captures remain outside Git. These source controls do not
replace complete frozen-input exports or historical provider-score comparisons.

### Shared stable-anchor matching

Three shared corrections also affect stable anchors outside the 104 body-fact
cases listed above:

- A missing page-level anchor can use visible native-link labels after the
  normal match fails. `non_record_lines` anchors do not use this fallback;
  declared text exclusions still apply. Link destinations alone are not text.
- An explicit Markdown heading may discard an appended URL with a fragment
  when matching its visible label. Ordinary word suffixes remain significant.
- Case-boundary normalization is applied to both the answer and the expected
  label, avoiding asymmetry for labels such as mixed-case product names.

The frozen definitions contain 499 suite/case entries with nonempty
`stable_text_anchors`: 99 webfetch cases and 100 in each of popular-sites,
dynamic-content, access-restrictions and articles. There are 486 distinct case
IDs because thirteen IDs occur in more than one suite; different contracts or
URLs must not be conflated merely because an ID is reused. This is the potential
scope, not a claim that all outcomes change or that every case has saved
provider output. The 104-case body-fact inventory above describes a separate
shared gate and remains valid.

Native-list name/description parsing is narrower: only `dynamic-angular-phones`
in webfetch and dynamic-content uses it. It excludes navigation/header/footer
and auxiliary containers from record counting, while retaining body-text
fallback parsing. Complete captured HTML still produces 20 records; deleting
a record or its description fails. Auxiliary lists cannot fill the quota.

### Generic-label follow-up

The Deployments case originally required only `Note:` as its second fact and
stable anchor. Its revision now requires the actual warning sentence,
"Do not manage ReplicaSets owned by a Deployment.", from the hash-verified
source. At that review checkpoint, complete HTML passed even with the generic
label removed, while removing the warning failed despite passing section
structure. The document-body follow-up preserves this mandatory warning and
replaces the section gate with source-bound body coverage.

### Saved-output comparison

The shared-scorer comparison covers all 104 affected cases, with ten
hash-verified saved outputs per case. Both scorers receive identical frozen
public task requirements and identical output bytes. The native archive's
historical annotations are aligned to those frozen requirements before either
score is computed; these are not reproductions of its published scores.
The baseline scorer is main d9e2f00. No annotation revision is applied in this
table, so it isolates shared scorer behavior.

| Saved-output group | Cases | Outputs | Main passes | Current passes |
| --- | ---: | ---: | ---: | ---: |
| Dynamic content | 22 | 220 | 76 | 68 |
| Native archive | 81 | 810 | 699 | 699 |
| Lexmount | 1 | 10 | 7 | 7 |
| Total | 104 | 1,040 | 782 | 774 |

The eight changed outcomes are passes becoming failures for mandatory facts.
Seven Vant outputs use the other supported language; the explicit reviewed
annotations accept them. Blueprint loses the required space between `add` and
`@blueprintjs/core`; retain rejection because the installation command changes.

Replay also exposed serialization defects that are fixed before these final
counts: OpenAI Python titles require symmetric case-boundary normalization,
and Kubernetes headings can have fragment URLs appended without separators.
The four original outputs pass after those fixes; deleting required text still
fails. Focused tests reject altered labels, ordinary word suffixes, phrases
present only inside URLs and headings without adjacent body. Redoc's joined
method/path and operation title is also recognized by the corrected matcher;
its source-backed operation-description alternative remains an equivalent fact.

This is not a full replay of every revised annotation or a provider-quality
result. Four exact frozen input bundles remain unavailable, so the comparison
does not replace their export checks.

### Expanded saved-output comparison

The three shared matcher corrections were audited beyond the earlier 104 cases.
Reuse requires identical output bytes, result metadata, selected task contracts
and scorer code. The previous 1,040 outputs (including ten Lexmount outputs)
are reused; 3,780 additional outputs are scored. No provider is called again.
Both sides use the same contract and bytes for each comparison. The baseline
scorer is `d9e2f00` (the scoring implementation is unchanged at the PR base
`b824b1e0`); the reviewed scorer is `3abfeb7`. The navigation-list correction
is separately qualified against both Angular cases and its accepted/rejected
controls. Raw captures and replay artifacts remain outside Git.

| Saved-output cohort | Case IDs | Outputs | Baseline passes | Reviewed passes |
| --- | ---: | ---: | ---: | ---: |
| Native archive | 381 | 3,810 | 1,343 | 1,335 |
| Dynamic archive | 100 | 1,000 | 312 | 304 |
| Lexmount | 1 | 10 | 7 | 7 |
| Total | 382 distinct | 4,820 | 1,662 | 1,646 |

The archives overlap in case IDs and contain different saved runs; case counts
must not be summed. Eighteen outcomes differ, in four cases:

| Case | Pass to fail | Fail to pass | Explanation |
| --- | ---: | ---: | --- |
| `dynamic-051-youzan-github-io-vant` | 8 | 0 | Required language-specific facts under the original annotation; the explicit revised annotation accepts the supported language. |
| `dynamic-056-vant-ui-github-io-vant` | 7 | 0 | Same language/fact distinction. |
| `dynamic-105-blueprint-docs` | 2 | 0 | Missing space in the installation command; remains rejected. |
| `global-homepage-030-weather-com` | 0 | 1 | Two actual visible Hourly links were missed without native-label matching. |

All fifteen Vant outputs pass the explicit revised rules; both Blueprint
outputs remain rejected in the revised controls. The additional dynamic-archive
780 outputs have no outcome changes. The native
archive adds another run of the already known Vant/Blueprint cases and the
weather case. In the weather output, disabling only native-label fallback
restores the failure for `stable-anchor-4`; replacing both Hourly labels while
retaining their destination URLs also fails. This attributes the improvement
to visible text rather than accepting URL-only evidence. The other two shared
normalization corrections add no further final-outcome changes in these saved
runs; this does not imply they never change individual anchor matches.

These are historical-contract comparisons, not complete exports of the current
frozen suites. The earlier 104-case contracts retain their documented alignment;
additional records use their archived contracts. Historical contracts can differ
from current suite contracts, including cases sharing an ID. The selected
archives contain no provider outputs for the 100 article cases or webfetch
`challenge-01`, `challenge-07`, `challenge-08`, `challenge-09`. No historical
provider-result claim is made for those 104 IDs. Existing article reference
controls and the four deferred exports retain their separate scopes.

All 4,820 outputs were rescored with scorer `03d23e7`, using the same
archived bytes, metadata and contracts; all output hashes match the restoration
records. No final pass/fail verdict differs from the preceding comparison:
1,646 pass, with the same 18 differences from baseline listed above. This covers
the later shared table and literal-pattern changes without new provider calls.
The three selected historical table/linked-table cases have 30 outputs and no
rendered HTML tables; nested-table and `thead`/`td` behavior is established by
dedicated accepted/rejected controls, not by claiming those shapes appeared here.

Final scorer `19ba48a` retains the full replay plus targeted revalidation.
All 214 normalized HTML-table answers were rescored after the heading-order
correction. A final surface comparison checked 224 answers containing a table-tag
prefix; the 101 whose normalized text changed were rescored, with no verdict
changes. Other results reuse hash-verified artifacts, metadata and contracts.
This is targeted revalidation, not a second full 4,820-output scoring run.

### Literal input and structural exclusion safeguards

HTML exclusions and table conversion share one parsed document. Headings are
decoded after final serialization, before restoring Markdown cells, even when
all HTML tables were excluded. Scope labels are not reinterpreted as HTML.
Raw-output and code-scoped patterns use the original returned text, independently
of plain-text escaping for prose checks. HTML table normalization preserves
separate nested tables and counts only cells and text owned by each table,
including when a link wraps an inner table. The owning link retains its URL and
its own label, excluding nested-table text; a nested-only label cannot qualify
as an owning linked record. Public scoring controls cover both outcomes. Explicit
`thead` rows retain their column labels even with `td` cells. These shared changes
also affect default contracts, without selecting the annotation revision.
Caption expansion applies declared HTML
table exclusions before discarding selector markup and also processes remaining
Markdown tables in mixed answers. Section checks retain article-local headers
while excluding explicit navigation and table-of-contents containers. Indented code cannot declare
section titles; fenced code closes only on a matching fence at least as long as
its opener, without trailing non-whitespace. Accepted/rejected controls cover
these combinations. Comparing 65 precisely hash-bound section-source inputs
against the preceding parser found no changed section verdicts. Three older
projection records lacked an exact matching source binding and are not included;
this is not a complete historical-output rescore.

## Current document-body qualification

The [59-case document-body review](document-body-review.md) records source scope,
per-region qualification and why WebSocket retains its section contract. Before
a formal live evaluation, qualify the selected revision against current initial-page
content without clicks, tab switching or expansion. Investigate failures and
version any justified changes; never silently replace frozen references. These
checks do not substitute for the four deferred frozen-export validations.
