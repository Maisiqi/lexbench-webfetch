# Data layout and rights

The suite registry is `src/lexbench_webfetch/definitions/registry.json`. Its suite directories contain the current inputs. It binds every shipped suite file by SHA-256 and records each population's ID and size.

| File within a suite | Role |
| --- | --- |
| `tasks.json` | Public task instructions and acceptance requirements, with body-reference text replaced by SHA-256/character-count bindings, and no full reference bodies or capture logs |
| `dataset-catalog.json` | Original ordered task inventory, source URLs and complete task-definition hashes |
| `source-inputs.json` | Exact executable dataset and external reference-file hashes |

The initial versions were imported from Browser Eval commit `894b38f8`. The current access-restriction suite selects the later frozen version declared in the registry. Source commits and per-file hashes are in `provenance.json`. Original catalog and manifest bytes are retained, including original dataset IDs and task languages. Their names may contain historical method labels; those labels identify frozen input versions and confer no method-specific acceptance exception.

Public task requirements are maintained in this repository. Frozen historical catalogs and manifests also live under `definitions/evaluation/` with their original relative paths and bytes. Browser Eval resolves its historical logical paths through this installed package. It retains experiment profiles and compact hash bindings, rather than duplicate definition files.

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

It also adds source-qualified `document_structure` contracts to 67 mutable
documents: 80% of declared headings must have the required local body, and
the delivered document must meet its reviewed half-length floor. Navigation,
table-of-contents entries and headings without their required body cannot fill
the section quota. This checks structural coverage, not semantic accuracy.
Heading IDs default to `section-1`, `section-2`, and so on; `body_required`
defaults to `true`. Explicit IDs and empty-section exceptions remain supported.
Two cases also remove a mandatory phrase proven to be in an initially hidden
tab panel or closed disclosure; all other existing requirements remain.

The remaining fifteen reviewed documents use source-qualified target directories,
resource cards, explicit body facts or API definitions, completing all 82 cases.
Definition contracts explicitly set `type: "definition"`:
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
source. Complete HTML passes even with the generic label removed; removing
the warning fails while section structure still passes. Other facts, section
requirements and the body-length floor are unchanged.

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
