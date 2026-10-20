# Article suite authoring

The registered `articles` suite (`articles-v2`) contains 100 qualified URLs: 95 fixed articles
and five changing post collections. `cohort.json` preserves candidate identities
and revision history; `rules.json` contains all 100 verified contracts. Public
tasks, the catalog and input manifest bind the complete executable dataset.
Full reference bodies and source observations remain external.

Revision 2 adopted five separately approved specific articles (044, 053, 063,
091 and 104). Revision 3 removed 042, 062, 083 and 097 at the user's request.
Revision 4 applies the user's authorization to replace unsuitable cases and
complete exactly 100: it replaces 001, 002, 003, 079 and 082 after direct source
review and removes 004. All original entries and prior cohort hashes remain
in the history. Search-only candidates 043 and 105 were removed before initial
approval. Revision 5 separates actual title checks, adds named semantic body regions and
independent initial-comment contracts for all 95 fixed cases. It corrects 049 to
the canonical OSCHINA article URL, revises 090 to the same URL's current 2026
Pew fact sheet, and replaces 061 with the independently reviewed National
Gallery of Art article. The other 93 fixed-body references are byte-identical.
The previous `articles-v1` input and all four earlier suites remain unchanged.

The four original Weixin cases could not be independently observed because of
an authoring-tool site-safety restriction. The final suite uses different
publishers and does not claim Weixin coverage or evaluated Web Fetch failure.
Retained folded pages have explicit complete-displayed-excerpt scope; they do
not claim the hidden continuation of the original article.

## Existing contracts used as references

The [popular-site tasks](../popular-sites/tasks.json) separate stable site labels
from changing named links (for example, `global-homepage-013-yahoo-co-jp`). The
[dynamic-content tasks](../dynamic-content-100-moli-webfetch/tasks.json) add
independent source counts, same-record fields and full-body regions (for example,
`dynamic-062-zh-sspai-home` and `dynamic-023-en-mui-data-grid-pagination`). Follow
the [source-review guidance](../risk-control/rule-authoring-guide.md) for ordinary
visibility, complete scope and independent evidence.

Reuse those scoring contracts where applicable, but do not copy their current
items or counts. A named-link floor alone cannot establish article completeness:
an article case must also require the qualified full article/post text. Likewise,
an excerpt directory cannot become an article merely because a list contract
can count its links. Existing frozen suites and input versions remain unchanged.

## Required scope

Open the fixed URL and observe its first automatic load, including ordinary
already-loaded content below the viewport. Do not expand, switch tabs within
the page, log in, paginate, accept a wall or scroll to trigger loading.
The user permits reference authors to close a login, subscription or similar
obstruction through its ordinary dismissal control. Preserve before/after
evidence and verify that the article was already loaded and its text did not
change; do not use dismissal to unlock or load additional content. This is a
reference-review exception only. Evaluated Web Fetch tasks still permit no
browser clicks, login, expansion or other content-loading interactions.
The reference must contain the complete qualified article/post body, not a
selection of convenient paragraphs. Keep headings, paragraphs, textual lists,
table text, captions and ordinary body links within their declared scope.
Exclude image lettering, alt text, OCR, hidden markup and collapsed content.
For retained cases with folded prose, disclose a displayed-excerpt scope and
require all ordinarily displayed text within that scope. Preserve the visible
cutoff and expansion control as evidence; do not claim the full original article
or substitute hidden DOM text for the displayed excerpt. A clipping or fading
boundary needs rendered evidence, not an assumption based on accessible text.

For article feeds, require actual post text in addition to record identity,
same-record fields, real owned links where present, and independently observed
record counts. A bare directory or search-snippet list is not an article.
Use a separately reviewed `post_collection` contract for changing feeds; a
fixed-body contract cannot freeze their membership. Do not silently drop difficult platforms. Record authorized replacements or
removals in cohort history, with the original entries and review basis.

## Stable and changing regions

Review every relevant ordinary text region: title, attribution, navigation,
sidebar, footer, controls and the article itself. There is no phrase quota.
Each chosen group needs an original-language phrase, location and reason to
expect stability. Do not freeze current news recommendations, comments,
reaction counts, ranks, personalized account state or current copyright years.
Historical numbers inside a fixed article remain part of its complete body.
Consent prompts depend on session state and are not mandatory site text. Record
any obstruction and any permitted dismissal when reviewing the article scope;
do not accept binding terms or purchase access to obtain the reference.
A nonmodal notice alone does not establish a reading gate: inspect the article's
actual visibility, clipping, inert state and any modal backdrop. Already-loaded
ordinary document text below the viewport remains in scope; hidden or collapsed
body text does not.
Each declared stable group must have a matching review ID, source region,
stability basis and observation date. Page-identity patterns are regular
expressions; escape punctuation when the intended identity is literal text.

Declared stable groups are mandatory in the current fixed-article contracts.
They supplement distributed body coverage; title or navigation matches cannot
replace missing article text. Reviewers divide every source line into contiguous natural chapters,
paragraphs or quotations with readable labels and explicit one-based inclusive
ranges. There is no fixed region-count limit.
Automatic paragraph detection is insufficient for arbitrary DOM line breaks.
Each region must contain enough ordinary text to yield a six-character fragment;
merge shorter labels into their adjacent natural component.
The shared version-3 body scorer checks these complete regions: all need 60%
fragment coverage, and at least all but one need 80% (one region needs 80%).
These are the repository's fragment-coverage tolerances, not a claim that every
character is reproduced. Test loss of complete opening, middle and final
components; do not use whole-document averages to hide a missing ending.

An independently observed visible input placeholder or button value may use an
anchor's `visible_control` selector and attribute. This opt-in applies only to
that anchor, never to body coverage. Hidden controls, passwords, accessibility
metadata and unobserved attributes are not visible text references.

## Titles and original body text

An independently observed actual title is a separate required component. Match
the visible source heading or a standalone Markdown/plain-text title, rather
than an HTML head title, image alt text, hidden heading or code block. Do not
invent titles for titleless short posts or infer image-only titles with OCR.
Preserve every original body sentence, including a first sentence that repeats
the title. A body repetition does not replace a missing title component.

## Initially displayed comments and replies

Each fixed case has a comment contract. Include every comment/reply already
displayed after automatic initial loading, including content below the viewport
that requires no action to load. Do not click, expand, switch tabs, paginate,
log in or scroll to load more. Closed disclosures, clipped continuations and
inactive panels are excluded. For a partially displayed comment, require its
complete readable prefix only; preserve rendered cutoff evidence independently.
An empty selector during loading does not prove that there are no comments.

Comments are changing records, not frozen stable labels. Every evaluation needs
an independent complete initial-page reference, including zero-comment pages.
Require all observed records with their own author, body and parent/reply
ownership; each substantive body needs 80% fragment coverage. Short or
symbol-only text is checked exactly. Preserve image-only record identity only
when independently marked as such; never substitute alt text for visible prose.
Do not freeze visible aggregate comment counters as record counts.

Pass `comments_reference` to `score_attempt` or `evaluate_response`, or use
`--comments-reference` with `--reference-context` for the standalone `score`
command. The caller-owned context supplies `id` and UTC `started_at`. The
reference contains `version: 1`, the exact `case_id` and `url`,
`scope: "initial_load_only"`, matching `context_id`, UTC `observed_at`,
`observation_complete: true`, at least two complete `source_observation_counts`,
and `records`. Each record supplies its own `id`, `author`, `text`, `parent_id`
(null for a root) and `complete_initial_text: true`. A reference must be at most
900 seconds old relative to the caller's context. Missing, stale, mismatched or
unsupported references make the case unmeasured; complete body text alone
cannot pass it. If an observed-absent layout later has comments, review that
layout before measuring it instead of silently ignoring the new records.

Historical contract qualification is separate from runtime measurement. A
single complete historical observation may qualify authoring only when bound
to the complete independent source file's hash. A date without a recorded UTC
time is allowed for that historical review; never invent a timestamp or treat
that reference as fresh evaluation evidence. Source acquisition and provider
adapters belong in the external execution harness. The five existing post
collections continue to check displayed posts, quotes and replies through their
own independent post contracts rather than an extra empty-comment contract.
All five require every initial record. Revision 5 raises the older 80% record
ratios in 038, 040 and 041 to 100%; complete sources pass and each individual
record omission fails.

## Changing post collections

Qualify collection scope from at least two independent direct initial loads.
Bind the complete displayed outer post and each displayed quoted component to
its own record identity and author. A displayed quote excerpt describes that
excerpt, not the full linked original. Do not silently discard truncated outer
posts to make a collection qualify.

The public task contains extraction selectors and coverage requirements, not
frozen current post identities or text. Each evaluation needs a fresh independent
reference plus a caller-supplied evaluation context. The scorer validates the
context identity, observation time and contract age limit before matching
records. A missing, stale or mismatched reference makes the case unmeasured.
Historical authoring references qualify a contract; they cannot certify a later
evaluation. Reference acquisition belongs in the external execution harness.
The standalone `score` command accepts the independent reference through
`--list-reference` and its caller-owned context through `--reference-context`.
The context JSON contains `id` and a UTC `started_at`; the reference supplies
the matching `context_id` and its independently observed `observed_at`.

Each matched record must retain its own author and complete outer/quoted body
components. A contract may explicitly allow a genuinely empty outer text only
when an independent reference marks `empty_outer_text: true` and supplies
nonempty, attributed owned quotes. This never excuses missing ordinary prose
or treats image alt text as body text. All other contracts retain strict
nonempty outer-body requirements. Every declared component region needs 80% fragment coverage. The
collection ratio is separate from component coverage; a quote cannot fill its
outer post, and one post's text cannot satisfy another. Reject duplicate or
unowned candidate records. Validate both HTML and ordinary linked-author Markdown.

## References and validation

Keep complete references, DOM captures, screenshots and review results outside
Git. Bind each body by UTF-8 byte hash, character count, exact opening/ending
and the complete-scope declaration. Independently inspect article boundaries,
overlays, lazy embeds and link ownership. Text extraction alone does not prove
ordinary visibility. Tool-policy or connection failures do not establish that
an evaluated method cannot fetch the article.

`lexbench_webfetch.article_dataset.compile_case` builds one verified fixed
article or post collection against an external evidence directory. `compile_dataset` requires the
entire approved inventory to be verified and refuses missing, reordered or
unresolved rules. No partial population is silently published as the suite.
The current version binds all 100 cases together. Future revisions must resolve
their whole declared population before publishing new dataset, task, catalog
and manifest bindings.

Validate through `evaluate_response`: complete independent body plus required
stable groups, actual title and fresh independent comment reference should pass,
including reasonable Markdown/whitespace changes.
Title-only, navigation-only, wrong article, repeated opening, omitted body
regions, missing titles/comments and absent mandatory groups must fail. Keep controls synthetic in CI;
real reference validation results stay outside Git. Do not call evaluated
products while authoring. Run `make check` and submit a feature-branch PR.
