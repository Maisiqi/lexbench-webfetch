# Third-party content

The Apache-2.0 license covers project-owned code, documentation and task requirements. Initial definitions and input-checking concepts originate in [Browser Eval](https://github.com/lexmount/browser-eval); its LexMount copyright notice is retained in NOTICE.

Original website text, document files, media, screenshots and frozen reference captures retain their source terms and are not included here. Public accessibility and a source URL do not grant redistribution permission. Task definitions retain source URLs and compact acceptance requirements; full historical reference inputs must be obtained separately under an appropriate authorization basis.

WebMainBench, WCXB and WebArena are separate projects and are not redistributed as LexBench Web Fetch suites. Cite their owners and follow their terms when using them through an execution harness.

## Scoring dependencies

Exact versions and resolved hashes are in `pyproject.toml` and `uv.lock`.

| Library | Use | License |
| --- | --- | --- |
| [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing | MIT |
| [Soup Sieve](https://github.com/facelessuser/soupsieve) | CSS selectors | MIT |
| [APTED](https://github.com/JoaoFelipe/apted) | Optional tree-edit scoring | MIT |
| [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz) | Optional text matching | MIT |

These libraries retain their own licenses. Installing the `tree` extra enables the optional scoring dependencies.
