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
| 1. 82 document pages | Use shared document structure and substantive body-length requirements rather than a title/navigation-only check. All 82 have reviewed rules and source-byte checks. Complete HTML controls and source-field projections are distinguished; source serialization and export limits remain explicit below. |
| 2. 31 product/brand homepages | Require actual stable functionality or named records where independently supported. Do not freeze campaign slogans, product prices or hidden carousel/tab content. The broader 44-case audit records 32 body-strengthening changes, two navigation fixes, one evidence-only retention and nine explicitly justified retentions. |
| 3. Four access cases | 047 uses its actual documentation/help entry structure; 192 retains mandatory body requirements. 027 and 050 use one five-field linked-table check requiring eight unique owned commit destinations, replacing duplicate table checks. A small shared auxiliary-node scope prevents decorative links and hidden details from corrupting row extraction. |
| 4. Six changing tables | Check required fields and actual rendered rows, not historical values. Preserve surrounding required prose. Exclude rows requiring pagination, interaction or virtual scrolling. |
| 5. Body thresholds | All 148 targeted cases require every retained region at 80%, with at most five regions. Original source text and hashes remain frozen. |
| 6. Ten challenge-list quotas | Seven quotas use observed counts and an 80% minimum. JD, Zhihu and Dianping returned login/verification pages; retain their existing requirements rather than invent counts. Cross-suite duplicates remain. |
| 7. Short regions and endings | Preserve real short specifications; move genuine headings/labels to mandatory stable text where appropriate. Use actual author endings with ordered matching. Dynamic 051 uses a required title/subtitle instead of a weak short region and accepts the actual English labels. |
| 8. Stable-anchor guidance | Sections 2, 6, 11 and 14 consistently require selected stable text by default. Adding body or record rules does not automatically make anchors optional. |
| 9. 25 replacement sources | Register actual source locations and observations, including record-count provenance. Remove 28 of 75 anchors across 11 cases with only one verified observation; keep source-bound body and record requirements. All 11 complete source controls pass and error-page controls fail. |
| 10. Error-page words | Remove qualified generic lexical guesses without adding duplicate diagnostic lists. 292 cases are qualified, including Vant, Microsoft, Apple and Douyin after current source controls. Retain 25 identity-oriented contracts whose challenge guard would be lost; eight others lack a qualified complete positive, as detailed below. Explicit output exclusions are treated separately. |
| 11. Long-document headings | Add real section headings, not sampled opening phrases, navigation or embedded-card metadata. Audit covers 22 articles, 15 documents and RFC 9110. Heading presence plus five-block coverage is an approximate completeness check, not proof that every sentence survives. |
| 12. Broad record scopes | Tighten risk 248, Twitch and Rakuten using target ownership and link identity. Retain Bilibili's one-resource target: a homepage-wide quota would change the task. |
| 13. Changing links and video text | Keep legitimate third-party news links for 2345. Video 09 asks only for title and publisher; do not add a description/subtitle task. |
| 14. Fixed 300-character floors | Retain 71 floors already backed by stronger gates: 60 document-body minima and 11 reference-body requirements. An additional universal half-length gate is redundant. |

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
- **Explicit exclusions:** retain React cart button/advertisement exclusions and
  Swagger's cookie-banner exclusion. Fresh sources contain these regions and
  the tasks explicitly exclude them. Complete target answers pass; adding the
  excluded content fails without breaking other required facts.

## Implementation boundary

Existing shared types handle stable text, reference-body coverage, named links,
tables, composite groups and resource targets. Earlier necessary shared changes
support document structure, strict body/ending revisions, reference-preserving
role changes, explicit answer formats, scoped identity and evidence binding.
Most additional contracts are opt-in. Two shared corrections enforce already
declared body facts and deduplicate wildcard destinations; their complete
frozen-case inventory is in [the shared impact audit](review-550-shared-impact.md).
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

## Verification and limits

The final integration check passed 2971 tests and 338 subtests in 181.37 seconds.
The registered review contains 500 entries, including evidence-only records.
All 969 external review-input bindings were checked against the preserved bytes,
including the qualified Microsoft, Apple and Douyin source-replay controls.
The article suite was exported from its hash-verified frozen inputs with the
selected revision: all 95 available reference controls passed. Full frozen-input
exports for the other four suites have not yet been reverified; source-level
controls and unit tests are not substitutes for those exports.

The 288-case diagnostic migration was checked against actual source artifacts:
238 prior results were reused only after matching complete contract, proof and
source hashes; 50 additional cases were replayed. Task-specific negative controls
are used: an identity-only answer is valid when the task requests only identity.
One replay assembly error duplicated a menu's facts; its corrected control and
the original failed run are both retained.

Complete HTML, Markdown or explicit source-field projections are distinguished.
A projection is not evidence that absent DOM ownership or historical visibility
was observed. Five-block body matching does not prove whole-section completeness.
Single observations do not prove long-term stability. Blocked/error pages do not
supply list-count evidence. These limits are not hidden by weakening requirements.

Detailed evidence and remaining-case dispositions belong in the registered review
records and external audit collection, rather than an expanding development log.

## V2 review decisions

- Remove the independent body-threshold and ending revision files: their
  operations already exist in the selected revision. Patch contract fields and
  anchors by identity rather than repeat unchanged contracts. The initial
  conversion produced identical effective definitions for all 550 cases.
- Remove the Grommet SVG accessibility-label extension. Its Complete cells are
  visible graphics, not numerical text. Four distinct visible names remain
  required, with the surrounding headers and body requirements preserved.
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
- Remove 288 newly added diagnostic-list overrides. Qualified generic lexical
  exclusions remain removed; explicit task exclusions are a separate policy.
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

These controls do not establish that every homepage boundary or every retained
error-word rule is correct. Those items require their own source checks. Shared
behavior changes and their complete frozen-case inventory are recorded in
[the impact audit](review-550-shared-impact.md).

### V2 homepage ownership checks

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

Weather already uses generic article paths, Hao123 uses publisher article IDs,
and 1688 uses product records without fixed names or prices. Their known-label
navigation controls yield zero qualifying records. Namu already accepts arbitrary
wiki article paths; its known-label shell yields 22 against 68 required records.
Retain these contracts rather than add unverified selectors. Namu, Hao123 and
1688 captures do not preserve navigation ancestry; these are bounded known-label
negative controls, not exhaustive DOM proofs. Spotify, OpenAI and USPS use actual
section labels for their composite boundaries, so their boundaries are retained.

### Remaining generic error-word decisions

A synthetic omitted-content control supplies every mandatory stable label plus
verification text, but no body records. Removing generic exclusions makes this
control pass for 25 retained identity-oriented homepages; current rules reject it.
This is a counterexample to blanket removal, not an observed website failure or
proof that every retained word is ideal. Adding unrelated body requirements just
to remove those words would exceed this minimal revision.

The other eight retentions have specific source limits:

| Cases | Evidence and decision |
| --- | --- |
| Webfetch challenge 02, 04, 06 | JD, Zhihu and Dianping observations return login/verification pages. No qualified complete target establishes a safe removal. |
| Dynamic 061 Juejin | The preserved observation is `/hot/articles`, while the task requests `/`; do not change the task URL to fit evidence. |
| Dynamic 056 Vant | Complete English observations conflict with existing Chinese facts. The separately qualified correction for dynamic 051 does not establish this case's language binding. |
| Dynamic 014 RSuite | Source records pass, but the existing Resolvers anchor is absent. Removing an error-word list does not resolve that source/contract discrepancy. |
| Dynamic Angular phones | Complete source facts pass, but the record parser yields one against twenty required. Do not lower the quota merely to qualify this migration. |
| Douyu homepage | Three saved sources miss two mandatory anchors. No verified minimal anchor correction is available. |

These eight remain unchanged; their failed qualification is not evidence that the
proposed removal is intrinsically wrong, or that the existing contracts are fully
validated. The original task and frozen inputs are preserved.
