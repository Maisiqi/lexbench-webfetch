# Article suite authoring

The user-approved population contains 101 URLs. `cohort.json` preserves their
original candidate identities and approved replacement and removal history;
search-result-only candidates 043 and 105 were
removed before approval. `rules.json` records each case as `verified` or
`unresolved`. This authoring population is not yet a registered frozen suite.

Cohort revision 2 replaces cases 044, 053, 063, 091 and 104 with the five
specific full articles separately approved by the user. Their candidate IDs
carry an `-r2` suffix. The revision records previous and replacement identities,
URLs and page types, the approval date, and the previous cohort hash and Git
commit. The original inventory hash identifies the initial inventory; the
current cohort bytes bind the revised population. No other proposed replacement
is adopted by that approval.

Cohort revision 3 removes only cases 042, 062, 083 and 097 at the user's explicit
request, without replacement URLs. It preserves all four complete original case entries,
the removal basis and date, and the previous cohort hash and Git commit. All
other cases and the four existing frozen suites remain unchanged.

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

For article feeds, require actual post text in addition to record identity,
same-record fields, real owned links where present, and independently observed
record counts. A bare directory or search-snippet list is not an article.
Use a separately reviewed `post_collection` contract for changing feeds; a
fixed-body contract cannot freeze their membership. Preserve unresolved cases
and their reasons rather than dropping difficult platforms from the population.

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
replace missing article text. Reviewers divide every source line into up to
five contiguous natural regions using explicit one-based inclusive ranges.
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
components. Every declared component region needs 80% fragment coverage. The
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
After every case is resolved, bind the executable dataset, public task
projection, catalog and input manifest together and register the suite.

Validate through `evaluate_response`: complete independent body plus required
stable groups should pass, including reasonable Markdown/whitespace changes.
Title-only, navigation-only, wrong article, repeated opening, omitted body
regions and absent mandatory groups must fail. Keep controls synthetic in CI;
real reference validation results stay outside Git. Do not call evaluated
products while authoring. Run `make check` and submit a feature-branch PR.
