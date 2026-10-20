# PR 5 review decisions

Review source: [PR 5 review](https://app.notion.com/p/lexmount/PR-5-5f4c64dc238c4e7f97eac67e30e7ab4c).
Revision 10 publishes `articles-v7`. These decisions compare the suggestions
with independently saved source evidence and the agreed initial-display scope.
Captures and full article references remain outside Git.

## Accepted changes

- Remove ten brittle exact anchors in 010, 027 and 093: promotional card labels,
  locale-dependent service labels, and localized timestamps. In 010 the card is
  inside authored rich text; it is not an unrelated injected advertisement.
  Original body text remains unchanged. Publication dates in 015, 044, 053 and
  104 remain part of their stable references.
- Bound plain-text comments to the reviewed component in all 20 comment cases.
  Prefer the known body ending, falling back to an explicit comment heading.
  A bare navigation label cannot establish scope. Stop at reviewed subsequent
  labels or a same/higher-level heading. End labels take precedence when a
  historical section marker is also the post-comment form label.
- Permit comment records after the known body ending without requiring an input
  placeholder such as 005's reply prompt. This prevents a missing form hint from
  rejecting otherwise sufficient comments. Author attribution remains required.

Each changed rule records its removed anchors or a `comment_boundary_review`
with the source path and SHA-256. End labels were checked after the last source
comment record, rather than guessed from all mandatory page anchors. Body bytes,
titles, count floors and the five post contracts are unchanged.

## Suggestions not adopted

| Suggestion | Decision and evidence |
| --- | --- |
| Require full DOM text for folded 008, 011 and 015 | Loaded text does not establish displayed text. Saved geometry shows ancestor clipping; 011 and 015 also have faded continuation controls. The references preserve their independently observed displayed excerpts. Ordinary below-viewport document text remains in scope. Expanding these references would contradict the agreed scope. |
| Downgrade visible control labels because Markdown cannot match them | All 19 current control anchors across 13 cases pass when the visible label is supplied as plain Markdown; omitting it fails. The selector adds HTML extraction, not an HTML-only requirement. Keep visible labels mandatory. This does not establish that real providers preserve them. |
| Rename the first release to v1 and remove legacy readers/CLI flags | No article suite existed on main, but six hash-bound external input versions already exist. Reusing their identities or deleting readers would break those artifacts. Preserve v1–v6 and publish v7, as repository guidance requires. This is not a claim of deployed external consumers. |
| Remove suspicious ending in 063 as an agent artifact | Saved source DOM contains the sentence in `aside.inst-cite > p.inst-cite__hint`; the independent accessibility capture also contains it. It is source material, not an instruction to the agent. Preserve the reference. |
| Require real provider runs before this review can finish | The user chose to review without running providers. Existing source-capture checks and constructed accepted/rejected inputs test the rules, but do not substitute for measured provider runs. Provider execution remains a subsequent harness task, explicitly absent from this PR. |

## Retained limits and follow-up scope

Keep the existing body tolerance: every region needs 60% coverage, all but one
need 80%, and a single region needs 80%. Partial omissions can therefore pass;
complete-region deletion is rejected. No claim of character-perfect completeness
is made. Navigation and stable footer requirements remain mandatory.

Post rules test fields and fixed count floors, not complete changing text,
freshness or exact current membership. Fixed comment rules likewise cannot prove
every displayed comment was captured. These limits are documented in the suite
authoring guide and PR description.

Monthly source maintenance, added platform/Weixin coverage, richer report
categories and smaller future PRs are reasonable future work, not corrections to
these rules. No schedule or additional provider/report functionality is added.
Weixin authoring access failure is not evidence of provider failure. Future
changes must preserve source provenance and publish new input bindings.

## Validation scope

Regression tests cover comment start/end ambiguity, missing form hints, article
and footer decoys, malformed scope, and legacy contracts. External controls use
20 independently qualified comment cases with six accepted/rejected projections
each (120 checks). These projections are not provider outputs. Existing visible
control tests cover HTML and Markdown, missing labels and hidden controls.
Repository-wide validation is run with `make check`; frozen input verification
checks the complete 100-case executable dataset. Full captures and control
reports remain external, referenced by the rules' evidence bindings.
