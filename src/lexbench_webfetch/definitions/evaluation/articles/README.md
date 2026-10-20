# Article suite authoring

The registered `articles` suite (`articles-v7`) contains 100 qualified URLs: 95 fixed articles
and five changing post collections. `cohort.json` preserves candidate identities
and revision history; `rules.json` contains all 100 verified contracts. Public
tasks, the catalog and input manifest bind the complete executable dataset.
Full reference bodies and source observations remain external.
See the [PR review decisions](../../../../../docs/reviews/pr-5.md) for revision 10 evidence and tradeoffs.

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
Revision 6 caps body regions at five by merging adjacent reviewed components.
All 95 body references and title/comment/post contracts remain byte-identical
to revision 5; 57 cases have fewer regions. Wider regions reduce sensitivity
to a small missing paragraph, while complete-region omissions still fail.
Revision 7 replaces runtime comment matching with fixed coverage rules on the
20 cases with actual initially displayed comment text. The other 75 fixed cases
have no comment rule: 74 have no displayed records, and 069 shows only hidden/spam
placeholders. Every classification retains hash-bound independent evidence.
Body text, title contracts, body regions and all five post contracts are unchanged.
Revision 8 raises comment floors: baselines of at most five require every record;
larger baselines require 80%, rounded up. Only numeric comment floors change.
Revision 9 replaces the five runtime-reference post contracts with fixed coverage
contracts: minima 4, 8, 4, 4 and 16 for 038, 039, 040, 041 and 101 respectively.
All 95 fixed tasks remain byte-identical. The five collections preserve their
URLs, page-identity checks and stable anchors; only their post contracts and explanatory review text change.
Revision 10 removes ten brittle exact anchors in 010, 027 and 093 and bounds text comment parsing in all 20 comment cases using reviewed body endings and subsequent section labels. Body references, titles, numeric floors and post contracts remain unchanged.
Previous `articles-v1` through `articles-v6` inputs and all four earlier suites remain unchanged.

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
a fixed-article case must also require the qualified full article text.
Changing collections use the separately disclosed post-coverage contract. Likewise,
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
The historical reference must contain the complete qualified displayed article/post body, not a
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
ranges. Current segmentation version 3 allows at most five regions. Merge adjacent
reviewed components at their existing boundaries, preserving complete text and
order. Legacy segmentation versions remain readable for prior frozen inputs.
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

Only cases with evidenced initially displayed comment text receive a version 2
comment contract. Include comments and replies displayed after automatic initial
loading, including below-viewport content that needs no action to load. Exclude
anything requiring clicking, expansion, tab switching, pagination, login or
scroll-triggered loading. Closed disclosures, clipped continuations and inactive
panels do not count. An empty selector during loading is not evidence of absence.

A valid record contains its own nonempty author and actual nonempty comment text.
Reply relationships, exact names, historical wording and per-comment links are
not requirements. Ordinary comments and replies may be flattened. Image-only
records and hidden/deleted/spam placeholders do not establish text coverage.
Distinct source record IDs remain distinct even when their text matches. Without
record IDs, repeated identical author-and-text pairs count once. Source identity may serve
as the author for visible pingbacks. HTML uses the reviewed selectors; text and
Markdown need recognizable author-and-body records within the comment section.
Author headings, standalone linked or bold names are supported; colon-labelled
authors require an explicit Markdown comment-section heading or the reviewed body ending.
Current text contracts locate the comment component after that ending, or use an
explicit comment heading if the ending is absent. Reviewed standalone end labels
and equal-or-higher headings terminate the component. A navigation label alone
cannot establish it. These hints are not additional required output anchors;
they keep article text and subsequent recommendations from supplying comments. Bare names and
metadata-only text are ambiguous and are not guessed as valid comments.

The minimum equals the independently reviewed valid record count when that count
is at most five; otherwise it equals 80% of that count, rounded up. The baseline
is frozen at authoring time, not refreshed for each test. This tests comment coverage:
missing the whole section or returning fewer valid records fails, while names,
wording and totals may change. It cannot prove every visible comment was captured,
or detect omissions above the minimum. Do not describe it as exhaustive comment
completeness. A site that later stops displaying comments requires a dataset
revision; historical presence does not establish permanent presence.

No fresh comment reference is acquired or required at scoring time. Historical
qualification still binds the complete independent source files by SHA-256 and
supports the presence/absence decision. Absent pages retain that evidence but
have no runtime comment contract. A date-only historical observation does not
invent a precise timestamp. Version 1 comment verification remains supported for
older frozen datasets; its runtime references and reply ownership requirements
do not apply to version 2 coverage rules.

## Changing post collections

Version 2 post contracts count distinct owned post-detail links with a nonempty
attributed author and visible post text. A genuinely empty outer post can qualify
through its attributed nonempty quoted text. A link and author alone do not count.
Duplicate links count once; quote-only links are not separate outer records.
HTML uses the reviewed selectors; ordinary linked-author Markdown is supported.
Keep the declared page-identity and stable-text checks. Do not freeze current
post identities, author names or wording.

Qualify scope from at least two independent direct initial loads. Preserve
historical qualification records and hash-bound source files outside Git.
The minimum equals the observed valid record count for baselines up to five,
or 80% rounded up above five. Only automatically displayed records qualify;
clicking, expansion, switching, login, pagination and scroll-triggered loading
remain out of scope. A displayed quote excerpt represents that excerpt only.

No runtime post reference or reference context is required for version 2.
These fixed floors detect missing fields and insufficient post coverage. They
do not prove complete per-post text, current membership, source identity beyond
the checked fields, or freshness. A website changing its initial display or
structure requires review and a dataset revision, not an automatic conclusion
that an extraction method failed.

Legacy version 1 post contracts remain supported for previous frozen datasets.
They require `--list-reference` and `--reference-context`, including matching
context identity and a fresh independent observation. They compare all declared
owned text components against that reference. Missing, stale or mismatched
references leave legacy cases unmeasured. The execution harness must establish
comparable page states; freshness alone does not establish comparability.

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
stable groups, actual title and sufficient valid initially displayed comment records should pass,
including reasonable Markdown/whitespace changes.
Title-only, navigation-only, wrong article, repeated opening, omitted body
regions, missing titles/comments and absent mandatory groups must fail. Keep controls synthetic in CI;
real reference validation results stay outside Git. Do not call evaluated
products while authoring. Run `make check` and submit a feature-branch PR.
