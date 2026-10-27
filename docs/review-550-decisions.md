# Review of the 550-case rule set

This review follows the independent 550-case report dated 2026-10-23.
Suggestions are evaluated against the actual task and independently observed
sources, not provider outputs. The requested scope is minimal rule revision:
reuse existing scoring types, preserve frozen inputs and avoid site-specific
code, new website inputs or unrelated architecture changes.

The selected score-only revision is `review-550-20261023`. Its per-case
decisions, source hashes, field changes and regression IDs are recorded in
`src/lexbench_webfetch/definitions/annotation-revisions/reviews.json`.
Source captures stay outside Git and are declared through `review_inputs`.
A registered case may contain evidence metadata only; the number of entries is
not the number of changed scoring rules.

## Report disposition

| Report item | Decision and evidence |
| --- | --- |
| 1. 82 document pages | Initial review added structure/content checks. The [2026-10-27 follow-up](document-body-review.md) replaces section/definition gates in 59 source-qualified full-body tasks with five-region 80% matching; 16 section cases remain. Frozen references and independent anchors are preserved. Source qualification and full-export limits remain distinct. |
| 2. 31 product/brand homepages | Require actual stable functionality or named records where independently supported. Do not freeze campaign slogans, product prices or hidden carousel/tab content. The broader 44-case audit records 32 body-strengthening changes, two navigation fixes, one evidence-only retention and nine explicitly justified retentions. |
| 3. Four access cases | 047 uses its actual documentation/help entry structure; 192 retains mandatory body requirements. 027 and 050 use one five-field linked-table check requiring eight unique owned commit destinations, replacing duplicate table checks. A small shared auxiliary-node scope prevents decorative links and hidden details from corrupting row extraction. |
| 4. Six changing tables | Check required fields and actual rendered rows, not historical values. Preserve surrounding required prose. Exclude rows requiring pagination, interaction or virtual scrolling. |
| 5. Body thresholds | All 148 targeted cases require every retained region at 80%, with at most five regions. Original source text and hashes remain frozen. |
| 6. Ten challenge-list quotas | Seven quotas use observed counts and an 80% minimum. JD, Zhihu and Dianping returned login/verification pages; retain their existing requirements rather than invent counts. Cross-suite duplicates remain. |
| 7. Short regions and endings | Preserve real short specifications; move genuine headings/labels to mandatory stable text where appropriate. Use actual author endings with ordered matching. Dynamic 051 uses a required title/subtitle instead of a weak short region and accepts the actual English labels. |
| 8. Stable-anchor guidance | Sections 2, 6, 11 and 14 consistently require selected stable text by default. Adding body or record rules does not automatically make anchors optional. |
| 9. 25 replacement sources | Register actual source locations and observations, including record-count provenance. Remove 28 of 75 anchors across 11 cases with only one verified observation; keep source-bound body and record requirements. All 11 complete source controls pass and error-page controls fail. |
| 10. Error-page words | Remove generic lexical vetoes in all 325 affected cases, without adding diagnostic lists. Existing content requirements decide the verdict. The four explicit output-exclusion lexical vetoes were also removed during the duplicate-task review below. |
| 11. Long-document headings | Require source-owned section content: RFC 9110 uses local section checks, while twelve reference-bound cases use same-count content facts instead of title-only facts. Existing body coverage remains; neither mechanism proves every sentence survives. |
| 12. Broad record scopes | Tighten risk 248, Twitch and Rakuten using target ownership and link identity. Retain Bilibili's one-resource target: a homepage-wide quota would change the task. |
| 13. Changing links and video text | Keep legitimate third-party news links for 2345. Video 09 asks only for title and publisher; do not add a description/subtitle task. |
| 14. Fixed 300-character floors | The initial audit retained 71 floors backed by stronger gates. The 59-case body follow-up restores baseline floors while replacing its added section/half-length gates with source-bound coverage; no universal extra length gate is added. |

## Document-body follow-up

See [Document-body revision](document-body-review.md) for all 59 cases, current
region percentages, excluded non-body ranges and the WebSocket retention.
The remaining 491 cases are unchanged by this follow-up. Previous historical
output results below precede this body-rule change; they are not a rescore of it.

## Important source-based decisions

- **Microsoft:** require three named non-carousel stories. Same-card titles and
  destinations must belong together; an adjacent generic button cannot fill a
  missing story. Current and historical field-projection controls pass.
- **Apple:** require three actual text-title/CTA cards. Exclude six logo/hidden
  headings; remove the obsolete MacBook Air promotion and accept Home as the
  observed navigation successor of TV & Home. Preserve other anchors.
- **Samsung:** accept Privacy as the actual footer label alongside Privacy Policy.
  Do not require hidden product cards. This is a label fix, not new body coverage.
- **Naver:** require actual feed records and deduplicate identities. Query keys
  are required only on the declared path families; ordinary path identities
  remain valid. Hidden carousel entries cannot fill the quota.
- **Douyin:** reuse named-link extraction for actual div href attributes.
  Thirty-nine initial rendered cards establish a minimum of 32; one empty
  placeholder is excluded. Repeated destinations, missing titles and titles
  outside their cards fail. No video URLs are fabricated.
- **Aliyun:** remove only four retired cloud-market menu literals whose old
  destinations also disappeared. Preserve the other 41 anchors. Do not treat
  differently named categories at different URLs as equivalent aliases.
- **Quark and DingTalk:** do not add requirements for content hidden in the
  initial rendered page. Quark keeps its existing functional requirements.
- **Huawei, Microsoft cloud and Shopify:** locale-dependent root URLs may return
  Chinese content. Do not silently change task URLs or add unrelated translated
  marketing alternatives. Shopify's official English entry confirms its existing
  English requirements, but that different URL is not a new frozen input here.
- **Shein:** the current maintenance page is not a qualified product-list source;
  do not derive a new quota from it.
- **Article 072:** use the existing visible-control rule for the actual submit
  input value; add genuine article headings. Plain innerText omits input values.
- **Article 093:** preserve the embedded quotation. The original automatic
  accessibility capture contains it; the existing qualified projection changes
  only that iframe and matches the frozen body. Reject card metadata and a
  registration CTA as proposed article headings.
- **Video 09:** the complete observed title and publisher total 19 characters.
  Replace the arbitrary 20-character floor with one while retaining both
  mandatory facts. Missing either field still fails.
- **Duplicate fixed records and exclusions (2026-10-27):** accept the review's
  demonstrated cross-suite inconsistency. Ten identical URL/prompt pairs now
  reference one contract per task. Complete record fields are bound together
  to the existing hash-verified source references, preventing invented records
  or swapped authors from passing on structure alone. The references match the
  frozen webfetch manifest; they are not the four missing complete input bundles.
  Membership is explicitly fixed; genuinely changing lists remain unfrozen.
  Remove the remaining four lexical vetoes (review stars, cart/ads, Swagger
  cookies and product recommendations). Explicit prompt exclusions justified
  the old intent, but do not justify failing any answer containing those words.
  Do not propagate these bans to the other suite. Required records, fields and
  counts remain enforced; extra unrelated text is not independently rejected.
  Catalog parsing preserves complete blank-line card boundaries around standalone
  prose, so a prefixed notice cannot become a price-first card's title. Missing
  fields remain rejected. This does not certify that every unwanted UI region
  has been excluded.


## Diagnostic-field cleanup

Before integrating main, 36 structured cases retained historical facts that
were only diagnostics. Main commit `4aa3cb2` now enforces every declared fact
alongside records. Therefore retain the 16 cases without a qualified fixed-record
replacement as mandatory fact checks; replace only the 20 duplicate fixed-record
cases' redundant facts with complete source membership. Do not infer that all
structured facts are optional. Frozen definitions stay unchanged, and diagnostic
fact averages are not comparable across this annotation/scorer change.

The follow-up audits the 16 remaining structured cases rather than treating
all their facts as diagnostic. Six cases contain 13 facts exactly implied by
unchanged mandatory anchors; remove only those duplicate fact groups (all six
fact thresholds are 1.0). Header presence is retained where it is a separate
requirement from typed row parsing. Fixed example records and completed-load
labels are not assumed to be live rankings merely because the suite is dynamic.

| Cases | Decision and evidence |
| --- | --- |
| HeroUI, Material Angular, UOL Play | Remove duplicated Name/Role/Status, No./Name/Weight/Symbol, and UOL Play facts; identical mandatory anchor groups remain. |
| Tabulator, Vuetify usage, MUI Data Grid | Remove duplicated page-title/View Source/Usage/API facts only. Keep nonduplicate example identities and descriptive/completion requirements. |
| EUI, Syncfusion, RSuite, PrimeVue | Keep explicit field/header requirements. Row typing alone is not proof that every original header appears; no source-qualified alias relaxation is proposed. |
| Webscraper, USGS | Keep category/site/time-window identity. These are not frozen product prices or old earthquake events. |
| Grid.js | Keep the frozen initial completed-load status and declared headers. This is an initial example-state requirement, not a new rule that every changing list must always have two items. |
| PrimeNG, TDesign, Swagger Petstore | Keep fixed example names/statuses and API identities; generic field counts are not a replacement for those source facts. No new complete source qualification is claimed for this retention. |

The two inherited diagnostic anchor roles contradict their explicit per-case
rules in `first-30-rule-review.md` section 21 and `remaining-70-rule-review.md`
section 56. Restore required stable text for Devuan (20 groups), preserving its
five body regions. This is an authored-policy correction, not a claim of a new
complete Devuan source replay. For ibiblio, qualified current HTML proves that
11 groups remain present; the old institutional sentence and `Logos` are absent.
Remove those two obsolete groups and require the other 11, alongside the existing
identity pattern and section requirements. Full source passes; omitting required
navigation fails. Frozen definitions and their historical diagnostics stay intact.

## Section ownership and page completeness

Navigation, feedback controls, references and related links remain page content.
The section requirements discussed here were added in this PR; they are not
pre-existing main-branch requirements. Keep references and related links in
section coverage. For the six Kubernetes cases (live-004, live-008, live-009,
live-015, live-052 and live-053), Feedback is a Yes/No helpfulness widget:
retain its heading in the coverage calculation, with `body_required: false`.
Empty compatibility placeholders also waive local body. This does not waive
substantive sections or remove navigation from the requested answer.
All six hash-bound complete sources and sources retaining only the Feedback
heading within that widget pass section checks; headings-only answers fail.

For both RFC 9110 cases, local section-body checks replace the added heading-name
facts. All 18 main sections need local content; the existing five 80% reference
regions and original mandatory facts remain. Complete HTML and plain text pass;
removing Methods while retaining the TOC fails. Deleting each main chapter from
the plain-text source also fails. Numbered outline entries and wrapped titles
cannot supply prose. This does not claim that every sentence is preserved.

Twelve reference-bound long-document cases (Wikipedia AI, Node.js, WCAG, XML,
Arch, Free Pascal, Dolphin, RFC 6455 and four paper tasks) replace 85 added
title-only facts with 85 short facts
from the corresponding section content. Titles in a TOC or citations cannot
supply these facts: each selected text is absent outside its DOM-aligned section
in the saved reference. All twelve complete plain references pass; deleting each
selected section fails its content fact. Eight complete HTML sources now pass the
full task. Node.js needed one additional scope correction: its frozen reference
includes three closed README details blocks despite the task requiring no
expansion. An existing hash-bound projection retains all default-visible ranges
and summaries, excluding only the three DOM-verified collapsed interiors. The
original HTML, complete reference and visible-only reference pass; removing any
of the four retained ranges fails. The 80% threshold, original reference hash and
shared visibility policy are unchanged. The other eleven cases keep their frozen
body regions. The four paper tasks also pass after line-wrap hyphenation removal
and Unicode normalization. No extra facts or new parser are added.

A data-only move to section structure was insufficient in plain text: repeated
citation labels and unformatted TOC entries can supply apparent local body. The
source-owned content facts address that demonstrated gap without generalizing a
new heading-order or plain-text TOC parser. This applies to the twelve reviewed
reference-bound cases, not live mutable documents without frozen prose.

## Implementation boundary

Existing shared types handle stable text, reference-body coverage, named links,
tables, composite groups and resource targets. Earlier necessary shared changes
support document structure, strict body/ending revisions, reference-preserving
role changes, explicit answer formats, scoped identity and evidence binding.
Most additional contracts are opt-in. Two shared corrections enforce already
declared body facts and deduplicate wildcard destinations; their complete
frozen-case inventory is in [the shared impact audit](data.md#shared-scoring-impact-audit).
No domain-specific scorer branch is introduced.

A necessary shared table exclusion option adds 18 lines and removes three across
two production files. It reuses existing table cleanup; absent options preserve
old behavior. Both affected sites pass 40 real-source controls, including valid
eight-row HTML/Markdown and a missing real destination. No new extraction type or
website-specific branch is added. New language-specific website inputs remain
outside this rule revision.

The original tasks, reference manifests and case identities are not rewritten.
Independent review sources cannot replace frozen parent inputs. Changes are
reviewed in [PR #12](https://github.com/lexmount/lexbench-webfetch/pull/12),
targeting the original repository’s main branch.

## Directory scope controls

Ten reviewed directory/content-link pages were checked at the composite-group
level using complete source HTML, target-container HTML, HTML outside that
container, and an outside-link Markdown projection. All complete and target
controls pass; all outside controls fail. These are group-level controls, not
full-task or frozen-suite export claims. Existing path, identity and quota
requirements suffice for the observed non-curl controls; do not add blanket
scope configuration without a demonstrated gap.


The page count is not the group count. The saved controls cover seven single-group
pages (`lm-python-tutorial`, `live-005`, `live-022`, `live-024`, `live-035`,
`live-040`, `live-051`), three directory groups in `lm-rust-learn`, four in
`live-039-welcome-to-redis-docs`, and the climate-card/focus-area groups in
`live-037-breadcrumb`: ten pages and sixteen groups. This includes every
`target-directory-*` group in the current webfetch revision (fourteen groups
across nine pages). The outside-link projections fail each of these groups.

Curl is the confirmed exception before revision: 42 outside links could satisfy
its 37-record quota in a link projection. The existing start-pattern mechanism
now starts at Documentation Overview, and the root breadcrumb is excluded from
the record path. Complete HTML and Markdown still pass. CSS 2.1 is itself a
specification directory, so its table of contents remains target content.

Grouped-table extraction and caption-specific schema, selector and capture checks
live in `structured_tables.py`. Composite groups retain their shared field-type
validator; no duplicate field validator or reverse module dependency is added.

The NOAA climate-card group also passes complete-page and `main#main` controls
with four records. Removing main leaves zero qualifying records in both HTML
and link-preserving text. Keep the existing route-qualified four-record rule;
this source control does not justify another scope field. These are group-level
checks, not a complete-task verdict.

## Annotation edit ownership

Score-only edit handlers live together in `annotation_revisions.py`. An ordered
handler map applies field updates, contract patches, thresholds, ending upgrades,
reference projections, region moves and final removals. JSON key order does not
change these dependencies. Frozen-parent checks and review verification remain
in the benchmark loader. All 550 revised public cases and review results match
the preceding dispatcher on the same current rule data.

## Retained implementation choices

- Section checks consume the already decoded visible-text surface, fixing
  literal `&` headings without adding format flags throughout the parser stack.
  Explicit plain-text handling still protects PDF angle brackets. Regression
  tests cover ampersands, literal entities, angle brackets and real hidden HTML.
  The artifact bytes remain unchanged. Keep this local correction instead of
  broadening the format-plumbing change across unrelated scoring paths.

- Keep section-contract validation at the scoring entry point: callers may pass
  mutable dictionaries directly to `score_attempt`, without using the dataset
  loader. A valid direct call succeeds; a subsequent invalid section floor is
  rejected. Loader-only validation would leave this supported path unchecked;
  no trusted-object cache or parallel unchecked scoring API is introduced.

- Definition support follows actual markup: the reviewed `os.path` source has
  35 `dt` entries, each followed by a `dd` explanation. Removing definition mode
  rejects the complete source. The declared Feishu title selectors match `div`
  elements; its source has no native `h2` elements. Removing those selectors
  likewise rejects the complete article. Keep both opt-in mechanisms rather
  than substituting title-presence checks that lose local-content ownership.
  Local `dd` content includes nested parameter descriptions; blanket removal of
  nested lists rejects valid descriptions. This structural check does not prove
  semantic relevance of every nested term. The bound `os.path` source contains
  no nested `dd dl` lists; accepted/rejected synthetic controls cover locality.

- Do not impose a blanket 20-heading cap. All 17 affected mutable-document
  cases lack frozen body-coverage requirements, so the proposed 80% prose
  fallback is absent. Three ordinary documents already have more than 20
  level-one/two headings; the definition case has 35 actual function entries.
  Truncating these lists would discard checks without a source-based boundary.
  Omitted default IDs and body-required flags reduce serialization without
  changing which sections are checked.

## Optional review evidence

Independent evidence bindings preserve the basis of the rules. Of 529 review entries, 242 cite independent sources and 18 cite no
frozen source at all. Removing those citations would erase their registered
basis; substituting `dataset.json` would falsely imply that the frozen file
supports the observation. The article-072 comparison below also shows that
reverting a rule does not necessarily repair an incomplete frozen reference.
Keep hash-bound provenance and optional executable controls, while requiring
all original frozen input checks. Independent observations qualify only the
stated source and controls; they do not certify historical provider outcomes
or replace the four unavailable exact input bundles. No captured page content
is committed to this repository.

For 137 entries whose sole rule change clears generic forbidden words, use the
frozen task as the policy-change source and retain the existing shared scoring
regressions. Fresh observations are unnecessary for that correction. Removing
232 exclusively referenced external bindings and repeated per-case explanations
saves 202,584 bytes across the two JSON files without changing any scoring rule.
Available body/reference checks remain active; absent executable references
remain explicitly unverified.

Export verifies the original frozen inputs regardless of `--review-source`.
Omitting that option skips only declared independent review files; it does not
skip frozen sources or mark missing evidence as passing. Available reference
results remain in the report. Export success materializes inputs; it does not
certify reference acceptance. A failed candidate plus omitted independent evidence
remains unverified, with its failed candidate and both completion flags retained;
without an omitted alternative, all-failing executable controls reject export.
A missing positive with omitted review evidence
is unavailable, while an accepted negative control still fails. Supplied review
evidence remains hash-checked and complete. Source registrations are retained:
they provide provenance and executable positive controls for revised rules.
The articles frozen-input export without review evidence materializes all 100
cases: 94 changed-case controls pass and article-072 is unavailable. Its failed
body-only candidate remains recorded; neither completeness flag is true. This
is an export check, not a claim of full positive-reference qualification.
A separate check scores the exact frozen article-072 body under both original
and revised annotations. Both pass body coverage and fail page identity plus
the same 19 existing stable anchors. Thus this incomplete body is not evidence
that the revised headings introduced a regression; reverting those changes
would not make it a complete page control. Removing navigation requirements to
force this body-only reference to pass would contradict the task.

### Rules supported only by independent observations

The following 18 review entries have no registered frozen-source citation:

- **access-restrictions**: `risk-diverse-192`.
- **popular-sites**: `china-homepage-088-figma-com`, `global-homepage-086-usps-com`, `global-homepage-020-naver-com`, `global-homepage-028-microsoft-com`, `global-homepage-056-apple-com`, `global-homepage-038-samsung-com`, `global-homepage-085-douyin-com`, `china-homepage-026-aliyun-com`.
- **webfetch**: `web-retail-returns`, `lm-feishu-help`, `challenge-01`, `challenge-08`, `video-09`, `dynamic-reviews-graphql`, `dynamic-react-cart`, `dynamic-swagger`, `dynamic-product-reviews`.

Their registered observations support the revised rules for the observed page
state. Rescoring a saved answer means testing those saved bytes against the
chosen rule edition; it does not prove that the newer observation describes
the page when the old answer was collected. Report the rule edition and this
limitation when comparing historical scores. These citations do not qualify
missing frozen reference answers or replace a frozen-input export.

## Verification and limits

The integration check passed 3040 tests and 342 subtests. Six Feedback
entries waive local prose; other rule changes from the preceding revision remain
unchanged. Shared review reasons preserve the same resolved explanations.
The registered review contains 529 entries, including evidence-only records.
The 738 retained external review-input bindings come from the hash-verified evidence set,
including the qualified Microsoft, Apple and Douyin source-replay controls.
The article suite exports from its hash-verified frozen inputs without an
external review directory: 94 changed-case controls pass and article-072
remains unverified. Neither completeness flag is true. With the optional verified evidence
directory, all 95 changed-case controls pass; `changed_rules_complete` is true,
but whole-task `complete` remains false because some controls cover only the
changed body rules. Reference selection continues after a scoped success to
prefer a later full-task success. Rechecking the same hash-bound article
sources qualifies 17 full tasks, 75 body-only controls and three body-plus-added-
stable-text controls; all 95 changed-rule controls pass. Full frozen-input
exports for the other four suites have not been reverified; source-level
controls and unit tests are not substitutes for those exports.

Keep the original `lexmount-doc` URL, acceptance rules and failed measurement.
The available diagnostics show an execution-path limitation, not a proven
rule defect; they do not establish that every provider succeeds elsewhere.
Preserve native safety checks and avoid case-specific DNS exceptions. Diagnostic
captures and provider measurements remain outside Git; the PR records the
supporting observations. Changing the URL requires a MAJOR dataset edition under
[versions.md](versions.md), with a qualified replacement and source controls.


Complete HTML, Markdown or explicit source-field projections are distinguished.
A projection is not evidence that absent DOM ownership or historical visibility
was observed. Five-block body matching does not prove whole-section completeness.
Single observations do not prove long-term stability. Blocked/error pages do not
supply list-count evidence. These limits are not hidden by weakening requirements.

Detailed evidence and remaining-case dispositions belong in the registered review
records and external audit collection, rather than an expanding development log.

## Rule design and controls

- Grommet requires four distinct visible names, with surrounding headers and
  body requirements preserved. Its graphical Complete cells are not numbers.
- Consolidate access 027 and 050 into one linked-table group: age, message,
  author, files and changed lines must belong to the same row, with eight unique
  commit destinations. A `token` field requires a complete explicit pattern;
  it accommodates values such as `-17 / +29` without weakening ordinary text
  fields. Forty source-derived HTML/Markdown controls cover complete input,
  each missing field, missing/repeated/wrong-host links and seven records.
- Select primary source headings for 14 long documents instead of nested
  headings. Keep original required facts. Complete reference texts pass;
  deleting their selected primary headings fails. One-word titles
  are not inherently invalid: a real Methods or Goals section can be useful.
- Remove Note, Caution, Table of Contents and the linked Cloud/Documentation/
  Roadmap/Discord navigation heading from seven section lists. Their complete
  HTML sources still pass and removing substantive headings fails.
- Reject the blanket replacement of section checks with title facts and total
  length. `test_title_facts_and_total_length_do_not_replace_section_body_checks`
  demonstrates that a linked table of contents plus unrelated footer text
  passes the proposed substitute but fails the section rule. The rule checks
  local body ownership, not similarity to an old paragraph.
- Do not merge mandatory short labels into long regions merely to remove the
  role-change operation. `test_merging_required_short_labels_into_long_prose_can_hide_their_loss`
  demonstrates that an answer missing the entire short label can still reach
  80% after that merge. The existing bounded operation verifies the frozen
  label and keeps it mandatory separately from prose coverage.
- Keep explicit answer-format support. Two full PDF reference texts containing
  code-like angle brackets failed when treated as HTML; declaring their actual
  plain-text format restores correct scoring without reducing body thresholds.
- Remove 28 singly observed replacement-source anchors. All 11 affected full
  source pages pass and challenge-only pages fail. Record observation counts
  once per case and retain hashes identifying the source of each kept anchor.
- Stripe now requires its three actual primary sections rather than twenty
  entries mixing sections, promotional cards and API property labels. Complete
  saved HTML passes; removing the primary headings fails.
- Six actual-case controls (Netflix, Brave, Telegram, Instructure, Feishu and
  ibiblio) confirm that title facts plus total length admit navigation with
  unrelated padding. Retain their local section-body checks.
- Retain ordered endings for all 95 opted-in articles: the failure mode is
  missing or reordered ending content, not a website-specific exception. All
  95 frozen references pass, with minimum ending similarity above 92% against
  the unchanged 80% threshold. Historical scorer versions remain unchanged.
- Retain grouped-table support for Syncfusion. All three actual HTML sources
  yield twelve complete rows; removing the country-caption association yields
  zero. Ordinary table matching cannot preserve the requested fields.

These controls do not establish that every homepage boundary is correct.
Each boundary requires its own source checks. Shared
behavior changes and their complete frozen-case inventory are recorded in
[the impact audit](data.md#shared-scoring-impact-audit).

### Homepage ownership checks

GitHub, Zoom, Volcengine and Elsevier now scope product records to their verified
main containers and accept future paths within the same product families. Zoom
uses `main#main`: its navigation dropdowns also contain `main` elements, so a
bare `main` selector is insufficient. Generic Explore products buttons cannot
supply product names. Three saved initial rounds each show twelve named main
carousel products; their 80% quota is ten, replacing the previous quota based on
fourteen page-wide destinations. The fresh anonymous HTML also returns twelve
named products after generic buttons are excluded.

GitHub and Zoom pass complete fresh anonymous HTML controls. Volcengine and
Elsevier pass their three saved, link-preserving text projections. Their fresh
HTTP DOM verifies ownership only: Volcengine's SSR omits rendered navigation,
and Elsevier returns a different locale. Neither is claimed to be a new full
positive for the old complete-page language/anchor requirements. Main removal
and footer-link controls fail, while renamed valid product destinations pass.
The record controls and source hashes are registered outside frozen inputs.

These selectors are observed site structure, not a promise that future redesigns
will retain them. Text boundaries use section or footer labels, rather than
current product names; an omitted required boundary fails closed. Tests cover
both HTML and Markdown, new product paths, navigation/footer-only records,
missing boundaries and Zoom's misleading navigation `main` elements.

Figma reuses the named-link contract instead of a separate composite group.
Its two design/build links must occur in `main#main`; text uses the Get started
action and required Figma Socials footer boundary. Remove the obsolete hero
slogan and the two campaign-heading anchors that previously defined the scope.
Three saved owned-link projections and fresh anonymous HTML pass. Removing main
leaves navigation/footer links but no qualifying entries. Regression tests also
accept changed campaign headings and reject footer-only or unbounded text.

Microsoft, Apple and Douyin also remove generic error-word exclusions. Their
complete source and record-omission controls pass with the current rules, while
identity-only and challenge-only answers fail. The older weak-identity rationale
no longer applies after their actual content requirements were added.

### Remaining homepage route decisions

The small homepage quotas follow the observed target regions: Microsoft has
three visible non-carousel story cards, Apple has three visible text-heading
tiles (six image/hidden-title tiles are excluded), and Figma has two visible
non-carousel design/build destinations. These checks supplement retained page
requirements; they do not claim that two or three records cover every homepage
component. Exact observations and omission controls remain in each review entry.


PayPal and NIH accept new destinations within their observed functional route
families instead of enumerating current feature names. All three preserved source
projections pass. Known navigation/stable-label shells yield four of eight and
seven of nine required records respectively, and fail. New distinct destinations
pass; duplicate or utility links cannot fill a missing record. These controls do
not establish complete DOM ownership: some navigation links can still contribute.

Do not broadly accept arbitrary Canva paths: the proposed generalization admits
44 navigation destinations against a quota of 16 in all three saved observations.
Retain its narrower source-qualified routes until a complete original-locale DOM
can support an ownership rule. Current browser access redirects to a different
locale; that is not a substitute input. NIH's fresh browser request returns a
verification page, so no new DOM claim is made for it either.

Weather already uses generic article paths. Its earlier text projections lost
article links when displayed headings differed from link labels containing video
durations. Restoring only uniquely matched URLs from the same hash-verified
observations yields 17, 13 and 13 distinct records; all three projections pass
the unchanged quota of 11. This corrects the test fixture, not the contract, and
does not establish complete DOM ownership. Hao123 uses publisher article IDs,
and 1688 uses product records without fixed names or prices. Their known-label
navigation controls yield zero qualifying records. Namu already accepts arbitrary
wiki article paths; its known-label shell yields 22 against 68 required records.
Retain these contracts rather than add unverified selectors. Namu, Hao123 and
1688 captures do not preserve navigation ancestry; these are bounded known-label
negative controls, not exhaustive DOM proofs. Spotify, OpenAI and USPS use actual
section labels for their composite boundaries, so their boundaries are retained.

### Content-only verdict policy

Generic login, verification and error words are not sufficient to reject
content. All 325 affected cases use their positive content requirements instead
of generic lexical vetoes, including identity-oriented cases and cases with
unverified source coverage. No diagnostic lists or additional task requirements
are needed for this policy.

A synthetic answer containing every required label plus verification text can
still satisfy an identity-oriented contract. That exposes the limits of those
content requirements; the extra words are not evidence that the required content
is absent. Do not invent stronger requirements solely to reject that synthetic
answer. Missing required labels, prose or records still fails existing checks.
The frozen prompts still request exclusions such as ad/button content, but the
revision no longer enforces their former lexical vetoes. This is a known gap,
not evidence that the complete output-exclusion requirement is satisfied.

### Output-exclusion review disposition (2026-10-27)

The companion parser findings are accepted: review containers and peer headings
now bound each review before source hashing, and owned HTML list records no
longer suppress the non-list parser. Regression controls cover correct records
with sibling footers, changed or missing review text, nested body containers,
peer versus nested headings, and mixed valid/invalid list records without
double-counting or borrowing fields. Source membership remains strict; no
footer phrases or source-record hashes are special-cased. These shared parser
corrections also apply outside the selected annotation revision. They do not
change declared coverage counts; historical provider outputs have not been
rescored for this follow-up.
The HTML record path retains sibling article containers without requiring a
`main` wrapper, and removes supported `Name:` / `Description:` field labels
before comparing values. List/article/mixed controls cover labeled and unlabeled
records, missing fields and changed descriptions; document-body root selection
keeps its existing single-article default.
Nested records are consumed before their enclosing article, and a review uses
its innermost dated container rather than every single-date ancestor. Wrapping
correct records in another section/article must not merge them; an undated
sibling must not fill in a missing review body.
Date-only presentation blocks may retain their enclosing container's directly
owned prose; independent child articles cannot provide missing review text.
Equivalent `div` review cards retain their dated header with their own body.
Non-list sections are parsed within their ownership boundary, including empty
grouping wrappers; a name in one sibling section cannot borrow a description
from another. Nested presentation text remains with an owning title.

Review comment [4386548264](https://github.com/lexmount/lexbench-webfetch/pull/12#discussion_r4386548264)
correctly identifies this gap. `test_duplicate_public_scores` confirms that
complete Swagger operations with a prefixed Cookie notice pass, while a notice
alone and fabricated operations fail in both suites. These controls establish
positive content validation, not removal of unwanted UI.

Do not restore the lexical veto: the same words can occur in legitimate quoted
or explanatory content, and the requester explicitly excludes word-presence
rejection. The proposed ownership-aware exclusion is not implemented in this
follow-up. Plain text does not reliably retain UI ownership; adding an HTML-only
detector would leave the text path unchecked, while inferring ownership from
phrases would recreate the rejected veto. A new cross-format exclusion contract
needs separately qualified positive and negative examples. That is beyond this
minimal parser correction. Preserve the original prompts and disclose that
Cookie banners, cart/advertising UI and related-product material are not
independently rejected. Closing the review discussion records this explicit
non-adoption, not a claim that the exclusion defect was fixed.

The following source and recognition limitations are not resolved by removing
generic lexical vetoes:


| Cases | Evidence and decision |
| --- | --- |
| Webfetch challenge 02, 04, 06 | JD, Zhihu and Dianping observations return login/verification pages. Normal target coverage is not verified. This is missing positive evidence, not proof that the frozen rule is incorrect; do not replace the URL, disable scoring or delete required content merely to accept the observed shell. Preserve the original tasks and report this qualification gap. |
| Dynamic 061 Juejin | Both saved visits started at `/hot/articles` but ended at the task homepage `/`. Their complete HTML already passes with 20 records; no rule change is needed for those pages. These redirects do not establish a direct-homepage collection control, so retain that qualification and the original task URL. |
| Dynamic 056 Vant | The frozen task explicitly declares en-US and the English final URL. Accept the observed English introduction and LICENSE alongside the original Chinese alternatives. Both saved HTML observations pass; removing either text fails. The observations have identical bytes, and these controls use restored review references rather than a complete frozen-suite export. |
| Dynamic 014 RSuite | Fixed adjacent native-link labels being concatenated into Resolversschema-typed. Resolvers exists in both saved HTML sources. Both complete pages now pass; removing or hiding that label fails. No required anchor is removed. |
| Dynamic Angular phones | Fixed HTML normalization losing native list-item boundaries. The complete captured page now yields 20 records and passes in both suites; removing a record or description fails. The 20-record quota and original required text remain. |
| Douyu homepage | Remove only the two old fixed navigation labels absent from all three complete observations. Preserve the other 19 anchors and named-record requirements. Complete projections pass; omitted links and retained-label omissions fail. |

All eight receive the same generic-word removal. The Angular parsing defect is
resolved separately without changing its rules. The RSuite native-link boundary defect is also resolved separately. The Douyu two-label correction is independently source-backed. The Vant correction follows its own explicit English target binding. The other four
source/contract discrepancies are not resolved by the generic-word policy correction. The original tasks and frozen inputs are
preserved.
