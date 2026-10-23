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
wrapper and its text. It is not evidence of a heading-free document. The other 19 cases required separate classification. This correction does not
change the original 63 heading inventories. Feishu's template data alone was
insufficient to prove initial visibility; its later rendered qualification is
documented below.

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
initially brought the mutable-document review to 81 of 82. The subsequently
registered Feishu correction completes these 82 document amendments; its source
conditions and remaining verification limits are documented below.

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
Canva, PayPal and Elsevier. Figma's three earlier observations lacked the required
"The full-stack creative canvas" text. A later initial browser observation
confirms that heading, so it must remain. However, the proposed eight-of-ten
carousel quota is rejected: actual ancestor geometry shows horizontal clipping,
with several loaded cards outside the displayed carousel. DOM presence and
nonzero element rectangles do not prove initial visibility. DingTalk's original
version and meeting labels are also confirmed visible. USPS's current featured
cards differ from the old passport promotion. Revised homepage candidates
remain under review; no carousel quota is registered. Proposed bulk
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

## Literal HTML examples in delivered text

Vue 026 and CSS 043 exposed a serialization defect: their extracted plain-text
examples contain literal `<script setup>` or `<style>` tokens. Mixed-HTML
projection treated these as active raw-text elements and swallowed later real
facts. The leading HTML-document detector was not the cause. An origin HTTP
Content-Type cannot resolve this ambiguity because delivered answers may be
extracted text from an HTML origin.

Optional persisted `answer_format` metadata now distinguishes delivered plain
text from HTML/Markdown. Explicit plain text protects literal tags only on the
temporary content-scoring surface; original bytes, resource evidence and links
remain unchanged. Default behavior and real HTML visibility rules are preserved.
Unknown declarations fail, and saved metadata is replayed through the same CLI
and scoring path. The harness must preserve this declaration for offline replay;
historical outputs without it are not silently reinterpreted. Actual Vue/CSS
positives, removed-fact negatives and prepared-answer controls qualify the fix
against the registered document rules.

## Numeric movie names and two homepage quotas

The IMDb frozen inventory contains 250 movie titles, including the numeric title
`1917`. Its task now uses the existing nonempty-name option; empty names, CTA
labels, wrong hosts and wrong paths remain rejected. This validates the name
field, not the authenticity of an arbitrary supplied title. Original DOM
ownership is not established by the saved typed inventory.

Three initial observations each contain 13 Twitch channels and nine Rakuten
products. Their quotas are now 11 and eight, respectively, using 80% rounded
up. Twitch retains real single-segment channel paths. Rakuten excludes shop
category and information routes from product records. All old stable anchors
and forbidden terms remain. Complete-source, quota-boundary, old-minimum-only
and missing-destination controls qualify these changes: 37 controls across
the three cases pass. The additional observations are separately hash-bound
review inputs; original frozen manifests remain unchanged.

2345 already requires ten records from an observed inventory of ten external
articles. Neither lowering that requirement nor restricting links to the
homepage host is supported, so that task is unchanged.

## Initial retail sections and rendered Feishu headings

The retail returns task previously accepted three facts plus unrelated padding.
The actual initial page has four disclosed prose sections and eight closed
accordion labels. Require their headings, six stable prose clauses and half the
observed body length, while preserving original facts and adding the observed
online-return heading alias. Hidden accordion answers are not required. All 28
source and omission controls pass, including actual compact main HTML. The
original full-page HTML was truncated in scripts and is not used as an HTML
positive. This checks sections and clauses, not verbatim completeness.

Feishu uses source-evidenced custom heading elements rather than native h2/h3.
Optional per-heading HTML selectors recognize those elements only when their
text also matches; hidden elements and closed details remain excluded. Native
headings and extracted text remain supported. All eight declared headings are
source-backed; the existing section-coverage threshold remains the acceptance
threshold. Original five facts and stable anchors remain, with a 1263-character
body floor. The FAQ question is visible, but its collapsed answer is excluded.
The observation used an existing signed-in session with no login or expansion;
the task has no anonymous-access requirement. This is not proof of anonymous
reachability. The observed article matches the old embedded body after removing
whitespace/punctuation and two old renderer icon placeholders.

## Dynamic headings, controls and child-document scope

Blueprint 105's Quick start heading and Grid.js 025's View Source button are now
required stable text rather than prose regions. Other body regions remain
independently required at 80%. The role operation also supports table_row
contracts while preserving table fields, row counts, identity and old anchors;
unsupported schemas still fail without partially changing the case.

Iframe 015 explicitly targets the child list, excluding parent navigation and
the sibling interactive frame. Its 41 parent header/navigation/footer anchors
contradicted that scope. Remove those out-of-scope anchors, retain item facts
and the complete list reference, and require the title immediately before item
0. Actual child HTML and text support this boundary; removing the title or
moving it after the list fails. The repeated word iframe in list rows cannot
substitute for the leading title. Tree 016 retains its three short regions:
they are actual initially displayed nodes, and deleting any one fails.

## RFC status examples and long-section omissions

The exact-bound RFC 9110 HTML-task reference fails the unchanged rule solely
because its legitimate 404 Not Found discussion triggers a forbidden term.
Remove that one exclusion for live-030-rfc-9110, retaining all body regions,
thresholds and facts. The complete reference then passes; a bare error page,
an error with page identity and an error with unrelated padding still fail.
Independent official HTML confirms that the status is substantive RFC content.

A separate measured weakness remains: removing the 3,478-character GET section
still satisfies the current regional body coverage. Retaining its heading while
removing its prose also passes that component. These are body-component findings,
not original full-score positives: the original forbidden-term defect prevented
the complete reference itself from passing. Long-document section requirements
remain under review; the five-region threshold alone does not guarantee that
every section is present.

## Current homepage scope corrections

Figma now requires the two non-carousel design/build destinations inside its
existing body-heading boundaries. All twelve old anchors remain. Complete
source representations pass, but retaining navigation links while deleting
either body destination fails. Removing every carousel link still passes.
A separate initial observation confirms that neither destination nor any
ancestor is transparent, hidden or clipped. The rejected eight-of-ten carousel
proposal is not registered.

USPS now requires three named service destinations in its Featured section,
ending before the postal-store carousel. Card names remain variable. Remove
only the absent Need a New Passport? promotional question; preserve Schedule
an Appointment and add the observed Book Passport Appointment alias. Current
three-card and three earlier four-card sources pass; missing cards, missing
body links, wrong hosts and missing appointment navigation fail. The original
DOM position of the removed question is unavailable and is not claimed.

DingTalk remains unchanged. Proposed product-role requirements were withdrawn
because their carousel scope was unqualified. A second proposal using three
security headings was also rejected: a new initial observation shows opacity
zero on their ancestors. Their presence in extracted text and nonzero DOM
rectangles is insufficient visibility evidence. This preserves a documented
body-coverage limitation rather than claiming it is fixed.

Ibiblio retains its original identity patterns. Current HTML and visible text
satisfy them; older Blog-only captures describe a different historical layout.
An independent defect remains in identity-only acceptance: removing both news
and projects still passed. Add the three substantive Latest/About/Featured
headings with local body and a 1090-character floor. Do not freeze news names,
project names, Welcome copy or Join invitations. Actual registered controls
accept complete current sources and changed invitation copy while rejecting
missing sections, navigation-only and title-plus-padding outputs.

## Video basic-information scope

Do not add description requirements to video-09. Its explicit task asks only
for the video title and publisher and disclaims video-file, subtitle and visual
understanding coverage. The saved title/publisher answer passes, while either
missing field and an empty answer fail. Requiring description text would change
the declared target rather than repair its implementation. A separate broader
video-body task would require its own explicit scope and source evidence.

## WCAG terminology is not a challenge page

The hash-verified WCAG 2.1 reference legitimately discusses CAPTCHA. Remove
only that case's CAPTCHA exclusion; preserve all original body regions, facts,
thresholds and other exclusions. The complete reference now passes. Empty HTML,
a CAPTCHA challenge, a Cloudflare challenge and identity anchors followed by
unrelated padding still fail. Block-page diagnostics remain available; the
presence of a word alone does not override this case's substantive body checks.

The long-document experiments also qualify the proposed heading-only repair:
a complete RFC 9110 GET section deletion is detected by its numbered heading,
but retaining that heading while deleting its body still passes. Additional
source-bound headings or brief facts can detect missing sections without
promising complete coverage of each section. Preserve the five-block limit and
document this limitation instead of claiming that heading presence proves body
completeness.

The same source-qualified defect exists in the fixed Browser Use README. Its
original reference hash is
`e0125e5233473fcf1266c1bdfb5fb3d5e3545ae027b5f954dcceb3d874e50765`.
The original full reference fails only the CAPTCHA exclusion; removing that
exclusion makes it pass. CAPTCHA-only, empty and original identity anchors plus
unrelated padding still fail. This is a case-specific correction, not evidence
that every case's exclusions can already be removed safely.

## Remaining completion audit against the current report

This checklist follows the report's current fourteen priority items, including
its explicit withdrawal of small-block scoring and optional stable anchors.
A registered change is not a claim that the entire item is complete.

| Item | Current evidence and remaining work |
| --- | --- |
| 1. Eighty-two document pages | Structural rules registered for all 82; keep source conditions and serialization caveats recorded above. Final source/export audit remains. |
| 2. Thirty-one homepages | Source-qualified body changes registered; DingTalk proposals rejected on initial visibility evidence. Reconcile all 31 individual decisions before completion. |
| 3. Four access cases | Commit records, documentation body and Ibiblio body corrections registered; original identity constraints preserved. |
| 4. Six dynamic tables | Six source-qualified table contracts registered, including rendered-row limits and graphic cell values. |
| 5. Strict body thresholds | All 148 targeted cases require every retained region at 80%; five-block limit preserved. |
| 6. Ten challenge quotas | Seven quotas registered, including four new source-qualified initial-page counts. Three other sites currently return login or verification pages. Do not infer list sizes from these failures. |
| 7. Short regions and article endings | Registered role/boundary/ending corrections; real short specification cards retained. Final article source-gap decisions remain. |
| 8. Stable-anchor guidance | Mandatory-anchor interpretation retained; verify all affected guide passages together in final audit. |
| 9. Twenty-five replacement sources | All 25 provenance updates registered, with unchanged matching fields and explicit one-observation limitations. All 124 source files are hash-bound external evidence. |
| 10. Forbidden terms | RFC 9110, WCAG and Browser Use demonstrated source conflicts corrected. Broad removal, including 91 homepage cases, remains unqualified and is not claimed complete. |
| 11. Long-document sections | Source-wide heading and necessary-fact audit in progress. Sampled omission tests alone do not cover all sections. Heading or opening presence does not prove full section coverage. |
| 12. Broad record scopes | Risk 248, Twitch and Rakuten scopes corrected. Bilibili's explicit single-resource target retained with controls. |
| 13. Changing links/video description | Third-party news links retained where supported by the task. Video 09 description expansion rejected because the task asks only for title and publisher. |
| 14. Other fixed length floors | All 71 retained top-level 300-character floors were checked: 60 have stronger required document-body minima and 11 require reference body coverage. No case depends on 300 characters alone; do not add a duplicate universal gate. |

## Article duplication and overlapping requirements

Source-based controls resolve the remaining duplication proposals without a
behavior change. Article 051 contains two real About sections, one under h3 and
one under h2. The complete source passes; removing either copy fails the current
body rule (region coverage falls to 38.2% or 36.05%). Do not treat real repeated
source content as a scorer-created duplicate.

Articles 053, 082 and 091 contain respectively one, three and two identical
stable groups. Deduplicating these conjunctions changes diagnostic counts but
not acceptance; the actual source HTML passes either way. Removing a real
source phrase from 082 or 091 can still fail its mandatory stable requirement
while body coverage passes. That is an additional declared obligation, not
proof that the phrase should be made optional. No redundant cleanup revision is
needed under the current mandatory-stable policy.

Article 040 already requires four distinct owned post links with author and
visible post text or attributed quote. Actual complete HTML passes; removing
posts or their bodies fails. Its descriptive profile label is not a scoring
switch, so relabeling it does not repair a demonstrated defect.

Article 093 has no exact duplicate alternative sets. Available source captures
pass the body layer but lack two required embedded-quote groups. They cannot
establish a complete full-score positive, and a deletion from an already failing
baseline is not a valid regression proof. Preserve the requirements pending
qualified evidence about that initially visible embed; do not delete all
body-overlapping requirements to make these incomplete captures pass. External
controls are retained in `051-duplicate-controls.json` and
`body-anchor-overlap.json` in the article-boundary audit evidence.

## Reusable rules, not case-specific repairs

The updated review objective includes the target pages, reference answers and
scoring design. Prefer existing scoring components across suites: stable text
for genuine section headings, body coverage for prose, named-link records for
both products and ranked items, and declared entry scopes for record boundaries.
Do not add production branches keyed to a case ID or website to pass a sample.

The long-article candidate containing 236 added requirements was not applied.
Seven opening phrases had been selected in response to particular deletion
controls, including arbitrary character cutoffs. Withdraw those additions as
overfitting. The replacement candidate uses only source-owned semantic headings,
deduplicates them and excludes requirements already present. It reuses stable
text matching and preserves the existing five-block body check. Heading
presence is an outline check; repeated headings or retained titles can coexist
with missing prose, and those limitations remain explicit.

The case-specific error-word corrections above establish real defects, but
are not the final general policy. Review migration of generic challenge/error
hints to the existing diagnostic type while retaining substantive acceptance
rules and explicit task prohibitions. Do not silently reinterpret a declared
prohibition at score time simply because the reference contains the word.

The four registered challenge-list revisions also reuse existing named-link
counts and entry scopes. Amazon's footer contamination exposed a general
question: a declared end marker that is absent currently lets the text scope
continue to the page end. The consumer audit found existing contracts that intentionally accept a
missing end marker, so the shared fix is opt-in `required_end`, rather than
a changed default or a website-specific footer exception.

## Effective length gates, rather than duplicate thresholds

The current combined revision retains a top-level 300-character minimum in 71
cases, all in webfetch. Inspecting the actual required components resolves the
apparent gap: 60 already require document-body minima between 546 and 153524
characters plus their heading checks, and the other 11 use required reference
body coverage. None of these 71 relies on the 300-character gate alone. Keep the
existing shared components rather than adding a second half-reference limit
simply because a legacy outer field still says 300. Length alone would not
prove that the right body or records were returned. The case-level inventory
is retained externally as `lexbench-fixed300-effective-gates.json`.

## Registered initial-list quotas

Four further webfetch challenge cases now use their independently observed
initial record counts: IMDb 250 gives a minimum of 200, Anthropologie 72 gives
58, Amazon 16 gives 13, and Reddit 25 distinct posts gives 20. These observations
are single independent current captures, not claimed as repeated visits. All
forty full-source and count-boundary controls pass for both HTML and
link-preserving Markdown, including below-threshold, old-three-record and empty
body cases with outside content retained.

Amazon reuses the shared entry scope: `.s-main-slot` bounds HTML; Results to
Related searches or Need help bounds text with `required_end: true`. This
excludes a real footer credit-card product URL that previously supplemented
twelve headphone results. Existing localized product routes and product-ID
deduplication remain. The optional strict-end behavior is shared across domains;
old missing-end contracts retain their default behavior. IMDb retains numeric
film names. Reddit's 27 rendered elements contain two duplicate posts and count
as 25, with the automatically loaded batch independently checked as visible.

JD and Zhihu currently redirect to login, and Dianping to verification. These
are valid rejection controls, not evidence from which to infer list quotas.

## Registered article heading presence

The replacement heading-only revision is now registered for 15 articles with
229 additional genuine section headings. It preserves all previous stable
requirements, five-block body thresholds, endings and projection operations.
All 15 complete independent source representations and all 15 missing-heading
controls passed their candidate checks; each negative explicitly reports a
missing newly required heading. Replay against the registered revision also
passed all 30 source and missing-heading controls.
The seven test-selected opening phrases from the withdrawn candidate are absent.

The full 22-case heading audit also records why other cases receive no addition:
078 has no actual body subsection headings; 079's title/dek, 082's four headings
and 100's only title are already required; 089 adds nothing after removal of the
sample-selected opening phrase. Cases 072 and 093 retain specific source gaps
for an existing submit label and embedded quote. Do not manufacture passing
sources or remove unrelated requirements to hide those gaps. This revision
checks outline presence, not ownership or completeness of every section's body.

## Integration checkpoint and measured limits

The combined revision currently contains 368 revised cases. After integration
of the four list quotas, 15 article heading additions and shared required-end
option, `make check` passed 2838 tests and 338 subtests. This validates the
current integration, not completion of the remaining source audits.

The RFC 9110 candidate includes 302 numeric and appendix headings. Its complete
reference passes and removing the complete GET section fails. Keeping the GET
heading while removing its prose still passes. This is direct evidence that
heading presence cannot certify section-body completeness. The review explicitly
accepts approximate coverage for very long documents while retaining at most
five body blocks; retain that limitation rather than introducing selected
sentence requirements to defeat individual deletion controls.

Current original-URL visits to Huawei and Microsoft cloud redirect to Chinese
pages, so they cannot qualify English required text. The score-only annotation
revision rejects changes to collection inputs such as URLs. A language-specific
URL needs a separately versioned input and verified initial navigation; do not
remove English requirements based solely on a different-language capture.

## Registered replacement provenance

All 25 dynamic replacement cases now record the actual source positions,
observed occurrences and source hashes for 75 existing stable-text anchors.
Eleven missing count-policy descriptions are also filled. Matching alternatives,
record boundaries, required counts and body scoring are unchanged. The combined
revision now contains 380 cases because 12 of these metadata-only corrections
were not previously registered.

The 124 distinct supporting files are hash-bound external review inputs.
Twenty-eight anchors in 11 cases have only one verified saved occurrence;
this is explicitly recorded and does not establish repeated temporal stability.
These additions close missing provenance fields, not the uncertainty about
long-term stability. They do not certify new captures or historical scores.

## Registered fixed-document headings

Thirteen further fixed documents now require their source-declared section
headings, preserving every previous fact and the original body regions. The
registration deduplicates headings already guaranteed by current requirements.
All 13 full reference representations passed the staged combined rules. The
two phpBB cases in the 15-case audit already required their category headings.
PDF figure labels and numbered footnotes were excluded using document heading
syntax; they are not treated as sections.

These additions reuse required facts and do not introduce a new scoring type.
Repeated headings may be satisfied by the table of contents, and retaining a
heading does not prove its section body was retained. The five-block 80% body
check remains an approximate completeness measure, as requested in the review.

RFC 9110 HTML now also has 306 additional required headings: 291 numbered
sections, 11 appendix headings and four genuine front/back-matter headings.
The existing Abstract requirement is retained; TOC and Index do not become
prose-section requirements. All 309 facts passed against the complete bound
reference. The external dataset is independent evidence: its RFC public task
and body bindings match the frozen task, but its whole-file hash is different
and never substitutes for the frozen input binding.
