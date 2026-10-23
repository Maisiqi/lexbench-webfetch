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

The `body-coverage-20261023` revision changes quotas on 148 existing body
contracts across webfetch, dynamic-content and access-restrictions. Every region
must reach 80%; it preserves all reference bindings, region boundaries and URLs.
Its `body_thresholds` operation accepts only `minimum_coverage`, `minimum_floor`
and `minimum_region_passes` for existing version-3/4/5 bodies. It operates equally
on public hash bindings and executable text, so no captured body is embedded in
the revision. Version-4/5 ending requirements cannot be weakened by this operation.
Per-case review hashes cover the resulting field differences and executable
controls cover complete, boundary, weak-region and missing-region responses.

For articles, `article-ending-order-20261023` upgrades the 95 fixed bodies from
version 4 to 5 with `body_ending_order: true`. Reference text, region boundaries,
the existing fragment gates and the five collection contracts remain unchanged.
Version 5 additionally compares the ending against a contiguous response passage
in token order. Insertions, omissions and substitutions each consume one token
of the 20% edit budget; text before or after the passage is free. Latin words and
individual CJK characters use the existing body tokenizer. Thus footers and
formatting are allowed, but distant fragments cannot be assembled into a closing
sentence. This checks an ordered local passage, not its absolute page position
or semantic completeness. It does not repair an incorrectly selected ending.

The ongoing `review-550-20261023` revision currently combines those 148 quota
changes and 95 ordered-ending changes. Five articles also receive source-reviewed
body boundaries, and nine more receive substantive conclusion selections with
their original body regions preserved. This is a partial review revision, not certification of all 550
cases. See [review decisions](review-550-decisions.md).

It also adds source-qualified `document_structure` contracts to 64 mutable
documents: 80% of declared headings must have the required local body, and
the delivered document must meet its reviewed half-length floor. Navigation,
table-of-contents entries and headings without their required body cannot fill
the section quota. This checks structural coverage, not semantic accuracy.
Two cases also remove a mandatory phrase proven to be in an initially hidden
tab panel or closed disclosure; all other existing requirements remain.

Seventeen further cases use source-qualified target directories, resource cards,
explicit body facts or API definitions, bringing the mutable-document review to
81 cases; the subsequent Feishu section correction completes all 82.
Definition contracts explicitly set `type: "definition"`:
signatures need adjacent descriptions (`dt` followed by `dd` in HTML, or complete
signature lines followed by prose in text/Markdown). API names and unrelated
padding do not count as definitions. Existing mandatory facts remain mandatory.

Six dynamic tables replace historical row text with initial-row-count and
visible-field contracts while retaining source-bound static prose. Grouped
tables may explicitly declare caption fields belonging to subsequent rows in
the same table section; expanded ordinary columns remain valid serializations.
No unrendered virtual rows or hidden example code enter the target count.

Additional source observations are declared separately in the revision's
`review_inputs`, mapping each suite to `review-evidence/` paths and SHA-256
digests. Per-case reviews cite these paths explicitly, with
`revision_review_source_declared` distinguishing them from parent inputs.
Export requires `--review-source` when the selected suite has such inputs. It
rejects missing, changed or symlinked evidence, copies only declared files and
runs reference controls against the resulting package. Original manifests and
parent dataset bytes remain unchanged. A declaration or successful file check
alone does not certify target completeness; the recorded source controls state
their actual scope.

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
