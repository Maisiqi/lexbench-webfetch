# 550-case review decisions

This is an ongoing review of the [reviewer's proposals](https://app.notion.com/p/lexbench-webfetch-550-c7dbc908b9aa4349839ace3283b7cac5?pvs=24), checked against frozen inputs and saved source HTML. Decisions below distinguish a demonstrated defect from a registered correction. The full review is not complete.

## Registered annotation corrections

`body-coverage-20261023` requires all existing regions to reach 80% for 148 fixed-body cases: 27 webfetch, 42 dynamic-content and 79 access-restrictions cases. Original frozen versions remain unchanged. All 148 exact-bound body references pass the revised body layer; this is not a full-task reference check. The revision is explicitly selected and does not accumulate other annotation revisions.

## Article source boundaries

The source paths below are relative to the external article evidence home, as declared in `evaluation/articles/rules.json`. Captures remain outside Git. A component appearing inside an HTML article container does not, by itself, establish that it belongs to the main prose; its function also matters. Conversely, a link list is not necessarily a recommendation widget.

| Case | Observed evidence | Decision and status |
| --- | --- | --- |
| 035 | `observation-root-04/complete-body.html` contains the opening credit in `figcaption.caption > span.credit`; source body lines 1–2 form an entire scoring region. | Accept the segmentation concern. Treat the image credit separately from prose while preserving its required visible information. Registered in `review-550-20261023`. |
| 037 | Both `body.html` and `dom.html` place the travel-advice sentence in an `h6` inside `div[data-testid="body-body-html"]`. It is the first standalone scoring region. | The saved page supports retaining the notice. Adjusting its role or grouping is justified; deleting it as unrelated site navigation is not. A separate required stable group now preserves it without making it a prose region. |
| 047 | `body.html` contains the next-article heading as `article.article.fmt.article-content > h2#item-4`, followed by the author's related links and series explanation. | Reject the inference that these are automatically inserted recommendations. The very short standalone next-article region is now grouped with related author material, with visible link requirements retained. |
| 063 | `replacement-v2/body.html` places the final URL instruction in `aside.inst-cite[aria-label="How to cite"] > p.inst-cite__hint`. | Accept the ending-boundary concern. This is a real source element, not evidence of a fabricated capture, but it should not stand in for the author's substantive conclusion. Citation information now remains separate from the prose ending. |
| 099 | `page.html` and `body.html` contain the final category link in `span.read-more-categories__links`. The reference ends with sharing/category labels after the appendix. | Accept the boundary concern. Preserve the methodological appendix; move sharing/category information out of the prose ending while retaining the applicable stable requirements. Registered in `review-550-20261023`. |
| 014 | `body.html` places the final reference link inside an ordered list in `div.article-viewer.markdown-body.cache.legacy`, under the author's references section. | Retain the bibliography. Removing it solely because it is a list of links would discard source material used by the article. |
| 087 | `page.html` places the further-reading links in a list inside `div.markdown`, following the conclusion. | Retain the article's further reading. The saved source supports authored reading material, not an unrelated recommendation widget. |
| 088 | `observation-root-02/complete-body.html` places the BibTeX section in `dt-appendix.centered > div.l-body`. | Preserve the article-specific citation metadata. The final paragraph of The Big Picture now receives the ending check; neither discarding all appendices nor treating a final brace as meaningful prose completeness is justified. |
| 051 | The saved `body.html` contains both an `h3` and an `h2` for the repeated about section. The bound reference also contains both copies. | Do not silently deduplicate the expected source text on the assumption that the scorer introduced the duplication. Verify the capture boundary and source ownership before deciding which occurrence belongs in the prose contract. |
| 090 | `revision-r5/body.html` places the first two lines in the fact-sheet collection's parent-term and term-list navigation, before the introductory paragraph. | Exclude these lines from prose coverage and require the collection label, Internet/Broadband and Mobile separately. Preserve the existing Social Media requirement, same URL, annual fact-sheet reference and all other regions. Registered in `review-550-20261023` with separately bound HTML evidence. |

The scope changes for 035, 037, 047, 063 and 099 are now registered in
`review-550-20261023`. Their
exact-bound source bodies pass the revised body layer, and removing each revised
ending fails. Separate stable requirements preserve the moved credits, notices,
citation instructions and footer information. The remaining boundary questions stay under review; the additional ending-only corrections are listed below.

The observations above do not authorize dropping stable navigation, attribution, notices or footer text generally. Body boundaries and required visible page information are separate decisions.

## Ending omission reproduced

The exact `articles-v11` input was verified against its published dataset hash and all 100 public tasks before running the following controls on its 95 fixed bodies. All 95 complete bodies pass. Removing the declared ending fails for 93 and incorrectly passes for 069 and 100. These are body-layer controls, not complete page or provider tests.

| Case | Declared ending length | Ending-fragment recall after removal | Exact ending still present? |
| --- | ---: | ---: | --- |
| 069 | 90 characters | 0.8169 | No |
| 100 | 19 characters | 0.8000 | No |

The cause is scattered fragment reuse: the ending check counts matching six-character fragments anywhere in the response and does not establish their order or locality. It is not necessary for the entire closing sentence to be repeated. Raising the region floor alone does not fix this defect. The correction below rejects these omissions while accepting harmless formatting and small insertions.

The new `article-ending-order-20261023` annotation addresses this matching defect
for all 95 fixed articles, retaining the old fragment gates and adding local
ordered token edit similarity at 80%. All 95 original bodies and all 95 Markdown
blockquote forms pass; all 95 ending-removal controls now fail, including 069 and
100. Synthetic public-scorer controls also cover inserted words, formatting and
scattered fragments. These results qualify the body layer only. Correcting which
source passage constitutes the ending remains separate work. The matcher permits
footers after the closing passage and does not claim absolute end-position or
semantic completeness.

Nine further ending selections are registered in `review-550-20261023` without
removing any existing body region or stable requirement. Each selected passage
was checked against the saved HTML and hash-bound reference. All nine complete
bodies pass; deleting the selected conclusion fails in all nine body-layer controls.

| Case | Required ending | Previous non-conclusion tail retained in the existing requirements |
| --- | --- | --- |
| 014 | Final event-loop analysis | Author bibliography |
| 016 | Final museum-interview paragraph | Credits and magazine subscription promotion |
| 050 | Final release-feature paragraph | Project profile and release resources |
| 065 | Explicit Conclusion paragraph | Author profile and social links |
| 080 | Final research discussion paragraph | Citations and publisher independence statement |
| 081 | Final paragraph of the concluding argument | Data-update notice, endnotes, citation and reuse information |
| 087 | Explicit Conclusion paragraphs | Author's Further reading list |
| 088 | Final paragraph of The Big Picture | Acknowledgments, bibliography and BibTeX metadata |
| 092 | Conclusion's final substantive paragraph and next-article transition | Author profile links |

These ending corrections do not certify that every retained region has an ideal
scope. In particular, keeping bibliographic material and requiring the author's
conclusion are compatible decisions.

## Mutable-document candidates

The initial 63 structural candidates have passed their source-HTML component
controls. Full scoring with unchanged legacy requirements accepts saved-source
representations for 61 of these 63 cases. The two remaining failures were separate
source-scope defects: Tavily's required Unauthorized example is inside a hidden
tab panel, and Fetch's required engine-support sentence is inside a closed
`details` element. Removing only those hidden mandatory facts and their duplicate
stable anchors makes both saved-source positives pass, while padded-TOC and
missing-body controls still fail. The 63 structural contracts and these two
minimal corrections are registered in the combined annotation revision. All 63
saved-source positives also pass with the registered revision applied.

The source-heading inventory also needed correction: Node's heading is wrapped
in an anchor, and the initial candidate generator incorrectly removed that
wrapper and its text. It is not evidence of a heading-free document. The remaining
19-case classification is still under review. This correction does not change
the original 63 heading inventories. Feishu's template data alone does not prove
initial rendered visibility; its proposed headings remain unqualified.

Node's actual `main` element supplies its heading and body, so its separate
contract is now registered as the 64th document correction. The saved-source
positive passes; moving the heading into navigation with padded body text fails.

Seventeen additional cases are registered: nine target directories, three
resource portals, four heading-free documents with explicit body facts, and
the `os.path` API definitions. All 17 complete saved-source positives pass.
Directory negatives retain actual navigation while removing body directory
links; existing facts and length still pass but the target-link gate fails.
API-name lists, empty descriptions and unrelated padding fail the definition
contract. Original fact thresholds and stable anchors are preserved. This
brings the mutable-document review to 81 of 82; Feishu remains under review.

## Dynamic tables

All six corrections are registered with separately hash-bound saved observations;
they are not silently attributed to the original frozen input manifest. The
original body reference remains unchanged, while a projection selects its static
prose and headers. All 18 saved-source positives pass with the registered rules,
and removing the tables fails for all 18.

| Case | Reviewed initial target | Correction |
| --- | --- | --- |
| 027 | 12 grouped rows, minimum 10 | Four visible fields plus country from the preceding group caption; the CSS-hidden fifth cell is not a visible source field. |
| 028 | 12 paging rows, minimum 10 | Require all five visible fields and retain the surrounding explanation. |
| 034 | Two tables, five rows each, minimum four each | Require both tables separately and retain the loading demonstration and explanations. |
| 035 | Three tables, 25 rendered rows each, minimum 20 each | Exclude empty spacers; do not count the conceptual 10,000-row dataset. The frozen reference itself did not contain those 10,000 rows. |
| 043 | Four name/completion rows | Require the completion graphic's accessible value in its own cell; replace historical Alan/Eric facts with static Name/Complete headers. |
| 055 | Five Basic rows, minimum four | Retain the Basic explanation and headers; exclude code hidden by zero height and overflow styling. |

Changed row values pass. For the five tables with companion explanation,
removing that explanation fails the body layer while the record layer remains
satisfied. Case 043 is table-only and receives no invented explanation.

## Body fact gate

An additional implementation defect was found while evaluating the 82 mutable
documents: a `body_text` stable-identity result overwrote failure of independently
declared `required_facts` or `expected_any` checks. A Database-page control with a
missing mandatory fact had zero fact coverage yet passed. The scorer now combines
these gates for `body_text`. Structured collections retain their existing record
semantics and do not acquire historical fact or length requirements. The body
length floor was already enforced; it is covered by a preservation test, not
claimed as a new fix.

## Access-restrictions 192

Reject the claim that diagnostic anchors leave this case with no mandatory checks. Its `page_patterns` independently require the target identity, public library/archive purpose, free resources, subject content and institution. Public-scorer tests accept a minimal synthetic matching identity and reject an error shell and missing required facts. This refutes the claim of an unchecked page; it does not prove exhaustive body coverage or remove the need to assess that separately.

## External-link duplicate counting

The wildcard-host branch of composite named-link groups counted repeated links
as separate records when no additional record fields were declared. A saved
source for access-restrictions 248 produced 30 entries but only 19 distinct
destinations. A source-derived control replacing their destinations with one
shared URL still passed. Counts now use canonical destination identities after
name exclusions, matching the intent of a minimum number of distinct records.
Different hosts remain distinct; fragments and trailing slashes do not create
new records, and query parameters distinguish records only when explicitly
declared as identity keys.

This implementation correction does not finish case 248's scope review. The
19 distinct destinations still include navigation alongside the ten observed
Picks stories; target scope must be qualified separately before changing its
annotation or quota.

The subsequent source-scope correction is now registered: AGP Picks starts at
its standalone section title and ends at its own View all control. Perspectify
likewise uses standalone section boundaries. The original quotas and remaining
groups stay unchanged. The saved page passes with group counts 10/4/7/6;
navigation-only Picks and one repeated story fail with zero and one record.
No publisher-domain restriction or navigation-path blacklist is introduced.

## Repository and documentation entry pages

Access-restrictions 027 and 050 now require eight of ten observed commit rows,
each with age, message, author, file count and changed-line counts. Both saved
observations per case pass, as do normalized Markdown and changed commit
messages. Removing the commit rows, omitting a column or keeping only seven rows
fails. These are record-structure checks; they do not independently verify each
commit destination or require every branch and tag entry. All original stable
requirements remain.

Case 047 is a tracker entry page with documentation and help links, not a long
explanatory article. Its correction requires four of five product-documentation
entries and all three observed help entries, without an invented prose-length
floor. Two saved-source positives pass and body-entry omissions fail. Existing
common-query headings remain mandatory; individual common-query destinations
are not separately verified. The four corrections use seven separately bound
source captures and pass 25 full-score controls plus four section-boundary
regressions.

## Homepage content beyond navigation

Twenty-six source-qualified homepage corrections are registered. They require
observed destinations, functional modules, section prose or product fields in
addition to every original stable anchor and forbidden term. Three saved
observations per case pass full scoring; their 78 source-derived missing-content
controls fail. Labelled-link inventories prove the observed labels and
destinations, but do not establish original DOM ownership. These controls are
not presented as independently captured navigation-only DOMs. Saved observations
are separately bound review evidence and do not replace frozen parent inputs.

Independent integration review rejected removal of 13 mandatory anchors across
five initial candidates. Restoring them preserves all passing sources for Zoom,
Canva, PayPal and Elsevier. Figma's three observations lack the required
"The full-stack creative canvas" text, so its candidate remains withheld.
Dingtalk and USPS likewise retain unresolved source gaps. Proposed bulk
forbidden-word removals remain withheld because the available evidence has not
qualified their false-positive and false-negative behavior.

## Short specification regions

Retain the five short regions in access-restrictions `risk-001`: they correspond
to five separate product specification cards, rather than arbitrary slices of
prose. Two saved initial browser observations at the exact requested URL contain
all five cards. With the registered all-region 80% rule, the complete body passes
and removing any one card fails in five omission controls. These qualify the
body layer only.

The source itself explains an apparent identity mismatch: the URL and document
metadata still name an AMD model, while both rendered observations show an Intel
model heading and the Intel/16 GB/512 GB cards used by the reference. Do not
replace observed content with specifications inferred from the URL slug. This
finding establishes what was displayed, not which product the seller actually
supplies. Other short navigation-only regions require separate scope review.

Cases 045 and 059 place News / All News in a news-module heading and link;
159 places its short slogan in `h1` and Upload in a submit link. These exact-bound
regions now become required stable text instead of prose coverage. Every other
region retains its 80% requirement. Reclassification validates the original
region's hash, preserves the text as a required anchor, and cannot remove all
prose. Public hashed tasks and executable references produce identical revisions.

Six successful HTTP captures qualify the changed body and added-label checks;
their browser counterparts are challenge pages and are not treated as positive
content. Five complete captures pass the full task. The second capture of 059
still lacks original anchor `stable-02`, just as before the revision; that
unrelated requirement is not removed or padded into the source. Missing-prose
and missing-label controls fail. This is a scope correction, not a claim that
all old source/reference discrepancies have been resolved.

## Resource-discovery scope

Reject increasing the Bilibili resource task's quota solely because a single
valid BV link passes. Its prompt explicitly requests one current video-detail
entry; it does not request a homepage inventory, video file or playback test.
An independently observed URL passes, while homepage-only, wrong-host,
malformed-BV and empty outputs fail. Offline address validation cannot prove
that every syntactically valid BV still exists. A broader target would need an
explicitly versioned objective and suitable source evidence, not an arbitrary
link count. This decision does not apply to the separate Bilibili homepage task.

## Challenge-list coverage and localized product routes

Three webfetch challenge quotas are now based on saved first-load observations
at the exact task URLs, rather than old inventories of uncertain initial scope:

| Case | Observed named records | Required records |
| --- | --- | --- |
| challenge-03 | 30, 28, 30 | 23 |
| challenge-05 | 25, 25, 25 | 20 |
| challenge-10-justwatch | 7, 7, 7 | 6 |

Each quota is 80% of the smallest observed count, rounded up. All original
stable anchors and forbidden terms remain. Complete observations and exact-quota
controls pass; three-record and one-below-quota controls fail. The historical
JustWatch inventory contained 46 records, which is not evidence that 46 appeared
in the initial state. Its separate popular-sites task is retained rather than
silently unified. The other seven challenge quotas still need qualified initial
scope evidence.

Amazon challenge-07 also had a distinct route defect: its saved localized
`/-/zh/dp/…` links were all rejected. An additive path alternative accepts the
17 named records in the saved source while wrong hosts, wrong paths and missing
search context still fail. Its existing quota remains unchanged. These four
registered corrections pass 40 full-score source and boundary controls; they
do not claim complete prose coverage or original DOM ownership.

## Twenty-five dynamic replacements

All 25 cases pass complete source controls using their qualified observations,
including later bound observations where earlier captures were incomplete.
Removing target records fails for all 12 structured cases. For the 13 fixed-body
cases, both large body omissions with original anchors retained and final-region
omissions fail. Of 42 individual-region deletion controls, 40 fail; two small
Gridjs Search deletions still match through retained anchors or repeated example
text. Fragment coverage does not establish unique spatial ownership or reject
every partial omission, and these results are not presented as such a guarantee.

The 11 proposed count-policy annotations keep existing minima and all other
requirements unchanged. They document provenance rather than repair demonstrated
acceptance errors, so they are not registered as 11 additional fixes. Mobilités'
old incomplete marker resulted from whitespace-sensitive length comparison:
the historical and current bodies become the same 2,182 characters after
whitespace normalization. The final DataPass r6 source accepts changed numeric
values and rejects dash placeholders. Neither an old marker nor a hash match
alone substitutes for these content controls.
