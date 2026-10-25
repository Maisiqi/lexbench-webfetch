# Shared scoring impact audit

This inventory scans all 550 frozen task definitions. It describes potential
behavior changes, not measured provider-score changes. Frozen tasks and source
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

## Wildcard link identity

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
