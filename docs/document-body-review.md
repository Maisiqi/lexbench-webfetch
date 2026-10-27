# Document-body revision: source qualification

This is the 2026-10-27 follow-up to the 75-case section/definition review in
PR #12, within `review-550-20261023`. It replaces section/definition checks in
59 webfetch cases with five source-bound body regions, each requiring 80%.
The previous 60 candidates were a suitability shortlist, not proof of stability
for exactly two weeks. Capture dates differ; short-term agreement does not
predict future changes.

## Decisions

- Accept body matching for these 59 initial-page/full-README tasks. None asks
  for every individual heading or function to be independently present.
  `os.path` therefore also uses body matching; its three existing anchors remain.
  Fixed reference tables and API descriptions are part of the requested prose;
  none of these cases needs a new record-count rule.
- Remove their PR-added section/definition gates and restore baseline character
  floors. Keep their existing facts, anchors, patterns and other requirements.
  Do not change navigation/footer requirements, task URLs, prompts or frozen bytes.
- Keep the other 16 section cases unchanged: the previously retained 15 plus
  `live-048-websocket-api-websockets`. Its introduction now discusses WebTransport
  and recasts WebSocketStream; complete-reference coverage in the first two
  regions was 65.30% and 66.98%. Earlier comparisons starting at Interfaces
  missed this rewrite. Do not remove that introduction to make the case pass.
- Do not claim that 80% of headings equals 80% of prose. Replacement follows the
  task's full-body objective, not an equivalence between those two measures.
- Reuse version 3 scoring. A small extension to the existing source-projection
  loader permits adding a body gate to a previously diagnostic mutable body;
  it verifies the catalog/reference hashes and removes the obsolete diagnostic
  policy. No new scoring algorithm, browser interaction or site adapter is added.
- Do not tune boundaries to achieve 90%. Four cases pass between 80% and 90%
  in a region; retain their original ranges and publish that margin below.

## Scope and initial-page constraints

References are the existing hash-bound `sources/<case>/reference.txt` files.
Regions are ordered, nonoverlapping ranges, covering the reference continuously
except these reviewed outer-boundary corrections:

| Case | Retained reference range (zero-based, end-exclusive) | Reason |
| --- | --- | --- |
| `live-029-fetch` | 288–292047 | Keep Abstract through the complete IDL Index, including algorithms and references. Exclude publication metadata and the appended, default-closed MDN compatibility panels. |
| `live-044-history-api` | 210–3080 | Keep the complete introduction through the end. Exclude the preceding default-closed Baseline explanation; the title remains an independent required anchor. |
| Other 57 cases | Complete existing reference | No extra trimming to improve current-page scores. |

Five ranges use source line boundaries; exact offsets, text hashes and source
hashes are maintained in the revision's `body_projection` declarations.
Only initial-page content is qualified: no expanding disclosures, switching
in-page tabs, pagination, login actions or other browser interactions.
Current HTML controls apply the existing visible-text extractor, including its
hidden-node and closed-disclosure exclusions; they are not full CSS rendering
proof. Feishu uses a transcription of browser-visible initial-page prose,
with the FAQ still collapsed, rather than its script-only HTML shell.

## Verification

For each of the 59 final contracts:

- Complete frozen reference: body component passes (100% in all five regions).
- Current source control: body component and all existing content acceptance
  requirements pass. This is local source qualification, not a provider run or
  transport/network success claim.
- Headings/navigation alone: fails.
- First half of the reference: fails.
- Delete each of the five regions separately: all five variants fail.

The four lower-margin cases are FastAPI `live-019-navigation-menu` and
`live-027-sponsors` (default-closed examples/explanations), MDN Push
`live-047-push-api` (a closed Baseline explanation), and Redux
`live-070-navigation-menu` (inline-code text serialization differences).
These passed without deleting their prose or lowering 80%.
The table reports body coverage percentages in source order. All rows use five
body regions and no new record rule. The current-source SHA identifies the
external HTML control, or Feishu's visible-text transcription; captures stay
outside Git.

| Case | Reference regions (%) | Current regions (%) | Current source SHA-256 |
| --- | --- | --- | --- |
| [github-repository](https://github.com/lexmount/moli) | 100 / 100 / 100 / 100 / 100 | 99.50 / 99.73 / 100.00 / 100.00 / 98.78 | `03d2eaec46bccb352e5388a99f8879a35bcc98c7b973c36861a2337d488d6a4f` |
| [live-001-python-pathlib-documentation](https://docs.python.org/3/library/pathlib.html) | 100 / 100 / 100 / 100 / 100 | 99.88 / 97.90 / 99.23 / 99.51 / 98.96 | `608942d569a76928723a184f6210d06c3b6c7304fe1f385f6e0fe48d2d018401` |
| [live-002-http-http-modules](https://docs.python.org/3/library/http.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `4c2f3d730dbdbb6220f2092a7a922c5466cc50d8e17a1a2573e0f455e1ef5ed4` |
| [live-004-deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 99.37 | `a14384e81e3b7babac98ce739a8e1e16e67fb6810fd85d22546001d7b78e9db8` |
| [live-006-python-typing-documentation](https://docs.python.org/3/library/typing.html) | 100 / 100 / 100 / 100 / 100 | 99.99 / 99.98 / 98.35 / 97.42 / 98.61 | `1f80a1a1700a3ba30ca1475c98ae5afb6d2d21c8aaf393cedef5ad4b153a6feb` |
| [live-008-service](https://kubernetes.io/docs/concepts/services-networking/service/) | 100 / 100 / 100 / 100 / 100 | 99.98 / 99.97 / 98.75 / 99.82 / 99.13 | `94b5ad58a0ea38ea040a0fa27728fe8297d929777d23c4116fb5b7255419b9e9` |
| [live-009-run-a-stateless-application-usin](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `7141a6e7486e7c6b10362fc42e27224737502ada4fb440c00dfe047379b50f46` |
| [live-012-navigation-menu](https://github.com/django/django) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `dc65e19593128ee1bc78be884412423c76e16005c2179626c4dfe0f8bf906332` |
| [live-013-navigation-menu](https://github.com/sveltejs/svelte) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `2dd26c192b44f2be1aad8b364f44b78fbda61399fd8be91aa4814dd2fc589ed7` |
| [live-015-configmaps](https://kubernetes.io/docs/concepts/configuration/configmap/) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `370fc50dc4799d762a590dbb75dc0e9f33202377e54967f4222d31872fbea56c` |
| [live-016-navigation-menu](https://github.com/openai/openai-python) | 100 / 100 / 100 / 100 / 100 | 100.00 / 99.69 / 99.75 / 99.98 / 99.71 | `7b265b734c4bf36244d0d21b6215c529394571205cc5156fd5b9aa6b7283f42d` |
| [live-017-navigation-menu](https://github.com/langchain-ai/langchain) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `0456b02ee70ba9462460935e2071db4062b3a95f3e3d0858d81070fa1951b949` |
| [live-019-navigation-menu](https://github.com/fastapi/fastapi) | 100 / 100 / 100 / 100 / 100 | 99.57 / 83.04 / 95.97 / 98.00 / 96.88 | `3e3362bd8a49482fdc52ac12c11df8935dd0f7a99604f114a656ee22ba3d52ef` |
| [live-026-getting-started](https://vuejs.org/guide/introduction.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `a255ca9187f6c93b67aeafaf6070bca594b60162f4935da0998413b31b149bba` |
| [live-027-sponsors](https://fastapi.tiangolo.com/) | 100 / 100 / 100 / 100 / 100 | 89.50 / 82.26 / 89.13 / 98.48 / 95.53 | `a6ee494c176ad8631dea29059cfb150fdf77d603d3a2006400d255526d1f0cd1` |
| [live-028-getting-started-with-rails](https://guides.rubyonrails.org/getting_started.html) | 100 / 100 / 100 / 100 / 100 | 99.97 / 100.00 / 99.89 / 99.93 / 99.97 | `e4280799ffdd938be01c28864e5184adac001cb799754b03e10765b08a60867e` |
| [live-029-fetch](https://fetch.spec.whatwg.org/) | 100 / 100 / 100 / 100 / 100 | 99.97 / 99.99 / 99.51 / 99.87 / 99.77 | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` |
| [live-032-api-reference](https://docs.stripe.com/api) | 100 / 100 / 100 / 100 / 100 | 100.00 / 99.51 / 93.83 / 100.00 / 100.00 | `9f5c74602f0dff4aad41998c6c6a103918a867b75d0c1982158cb2fbfe402e9b` |
| [live-041-python-programming-language](https://en.wikipedia.org/wiki/Python_(programming_language)) | 100 / 100 / 100 / 100 / 100 | 95.42 / 95.19 / 93.55 / 99.32 / 94.77 | `a37cce26fca7c01599e20601d3a0ace610ebf6689a2cb90d8e2e8a5a44df49cc` |
| [live-042-document-object-model-dom](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) | 100 / 100 / 100 / 100 / 100 | 99.88 / 100.00 / 100.00 / 100.00 / 99.72 | `47621f7d3b5f071abab71b29ac38ff4c8e3080c35dadd76883792c2b27b53cb1` |
| [live-043-syntax](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) | 100 / 100 / 100 / 100 / 100 | 98.88 / 94.32 / 98.94 / 96.67 / 99.03 | `9ba6d2322b6d3f0178021909449bbf3ec6b313fdd3cacff0d42267e9bf04e81c` |
| [live-044-history-api](https://developer.mozilla.org/en-US/docs/Web/API/History_API) | 100 / 100 / 100 / 100 / 100 | 99.12 / 100.00 / 100.00 / 100.00 / 98.39 | `3626500ac6fe6cdad50b9f4a85a64ad0592fbdd385eea4544ce2c9b105d22bfa` |
| [live-045-cache](https://developer.mozilla.org/en-US/docs/Web/API/Cache) | 100 / 100 / 100 / 100 / 100 | 91.35 / 99.69 / 99.62 / 96.61 / 97.80 | `d515010754a7432ad9d225954b7673f05b1631015bb47b05d3dfab60b820a5c7` |
| [live-046-file-api](https://developer.mozilla.org/en-US/docs/Web/API/File_API) | 100 / 100 / 100 / 100 / 100 | 99.31 / 100.00 / 100.00 / 100.00 / 100.00 | `51f75cc068ac985c1661268d3af6b0d328358b094f10b903259115296b312f8f` |
| [live-047-push-api](https://developer.mozilla.org/en-US/docs/Web/API/Push_API) | 100 / 100 / 100 / 100 / 100 | 81.57 / 100.00 / 99.75 / 100.00 / 99.58 | `31a067d55495b35a42392f2554d6591ba69aa42abe0f099b3c510953c0a1086e` |
| [live-049-functools-higher-order-functions](https://docs.python.org/3/library/functools.html) | 100 / 100 / 100 / 100 / 100 | 99.91 / 99.37 / 99.97 / 99.73 / 99.85 | `ade37a02be5b8871f3a691e4d40ccc445c13593ee2b91b88de3813503b831c2a` |
| [live-050-re-regular-expression-operations](https://docs.python.org/3/library/re.html) | 100 / 100 / 100 / 100 / 100 | 99.96 / 99.87 / 99.64 / 95.35 / 97.56 | `32650070d325ef3787579936baf70116804daecfb8954c41b4d316a18ababf15` |
| [live-052-objects-in-kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `9a570b4b02ec7805c080245e51ae6459a700a44b76ef19be1a0bd4d065692b8d` |
| [live-053-dns-for-services-and-pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `5d6c2d88b268397ccd83c80cb9877fe7b00033779c3ffcf4589acaa2d6d360f3` |
| [live-054-navigation-menu](https://github.com/aio-libs/aiohttp) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `0fc3ce05aa64f2609834a5d6bfe66e38ff6886cb672d747afd2a40e384c8fce4` |
| [live-055-navigation-menu](https://github.com/pytest-dev/pytest) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `815f7d99ef42d825d513d1991547ecf0b9db83ee0c3a5743f479c941041f3524` |
| [live-056-navigation-menu](https://github.com/denoland/deno) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `d1a9caa9754645e37a450f202625aa7fcad6df0879c06ddf7d975b55b24f6ff3` |
| [live-057-navigation-menu](https://github.com/spring-projects/spring-boot) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `24eed49442a29b8cf5bef3076a380ae67f40fe37e377a99c2b1278bd6b00b98f` |
| [live-058-navigation-menu](https://github.com/apache/superset) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 99.47 / 90.66 / 100.00 | `9b2031c0a91c7534d781a0cafdddaf737b08af0c9c0358da3dd0d58b61190b9c` |
| [live-059-navigation-menu](https://github.com/docker/compose) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `b6bfbc888d713c7a93126b20e9fc6070499c5f14e160746d7f7ee0f1092c4881` |
| [live-060-database](https://en.wikipedia.org/wiki/Database) | 100 / 100 / 100 / 100 / 100 | 99.84 / 100.00 / 99.99 / 99.96 / 99.01 | `353564801e02eb5138185179c3b602984c5fde6080de3acb61b2dfb818298c93` |
| [live-061-version-control](https://en.wikipedia.org/wiki/Version_control) | 100 / 100 / 100 / 100 / 100 | 99.58 / 99.29 / 98.59 / 97.92 / 98.48 | `07b67c6a05a92ced7d2c495d66260a6677ed378d356afcf3b205890691e9625c` |
| [live-062-natural-language-processing](https://en.wikipedia.org/wiki/Natural_language_processing) | 100 / 100 / 100 / 100 / 100 | 99.59 / 99.69 / 99.62 / 96.49 / 99.78 | `56edda486621399601f23be96fdadbb88c3b0a8f76d37f74ca83704f7af49d60` |
| [live-063-navigation-menu](https://github.com/astral-sh/ruff) | 100 / 100 / 100 / 100 / 100 | 99.13 / 98.32 / 97.61 / 100.00 / 98.31 | `a62fbeeae02d991d2738c54a594eb81362d8d0cc8389aeb0bf2c304e9fada61f` |
| [live-065-navigation-menu](https://github.com/huggingface/datasets) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `c6041e18a16615cbd73f39477800c6f6bf029563314cbd2fbb003762a45e0d44` |
| [live-066-navigation-menu](https://github.com/open-webui/open-webui) | 100 / 100 / 100 / 100 / 100 | 99.78 / 100.00 / 99.74 / 100.00 / 100.00 | `ff44280db18de1cafd0768c0da1b8f92e2929acdc81f23a40ca186e383dc6147` |
| [live-069-navigation-menu](https://github.com/prettier/prettier) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `6f3f60f877623e3ebaca651e44c2ff280f28a77c8b7759799041cc01aceb8dd3` |
| [live-070-navigation-menu](https://github.com/reduxjs/redux) | 100 / 100 / 100 / 100 / 100 | 99.66 / 83.72 / 98.82 / 99.79 / 99.53 | `4d812a2923b9b421334c52b176355fb21115a8506f0091110224ede3b27ae42a` |
| [live-072-python-itertools-documentation](https://docs.python.org/3/library/itertools.html) | 100 / 100 / 100 / 100 / 100 | 99.92 / 100.00 / 100.00 / 99.98 / 99.98 | `f49ddd4cf26e7768be1d67e618baea7653c8158fa448736bac126a3d130af382` |
| [live-073-python-json-documentation](https://docs.python.org/3/library/json.html) | 100 / 100 / 100 / 100 / 100 | 99.84 / 99.40 / 99.73 / 99.97 / 99.97 | `0df88c993a28b7c6a11e0b38dffaf6d9e6013ac91e374327eff8fdcda7706285` |
| [live-074-python-sqlite3-documentation](https://docs.python.org/3/library/sqlite3.html) | 100 / 100 / 100 / 100 / 100 | 99.34 / 96.50 / 99.53 / 99.18 / 99.63 | `58b28b1e33f69018dd906bca7c7f465cf45d567b3d0d9c267ad3307ce06adfb0` |
| [live-075-python-logging-documentation](https://docs.python.org/3/library/logging.html) | 100 / 100 / 100 / 100 / 100 | 99.94 / 100.00 / 100.00 / 100.00 / 99.75 | `549aebec5f36b75494c523c23b869443480d0e6872ad18fb4cbaa252af999fe9` |
| [live-076-python-unittest-documentation](https://docs.python.org/3/library/unittest.html) | 100 / 100 / 100 / 100 / 100 | 99.98 / 100.00 / 99.81 / 100.00 / 99.98 | `e6449a52d72b4c59f4f4b8ddeb3b3093c3e712d0b9a128fd11900fc7412ac39b` |
| [live-077-python-dataclasses-documentation](https://docs.python.org/3/library/dataclasses.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 99.93 / 99.40 / 99.93 | `926f7a41feb2498f18ee3c87f249aacc800456f8c7819b69ddc3a8fd80c44a59` |
| [live-078-python-collections-documentation](https://docs.python.org/3/library/collections.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 99.69 / 100.00 / 100.00 / 99.85 | `4756578cede5a456e9033da7058165478cf4b416d2c3c25fd928df57235fb5c3` |
| [live-079-python-hashlib-documentation](https://docs.python.org/3/library/hashlib.html) | 100 / 100 / 100 / 100 / 100 | 98.34 / 99.95 / 99.90 / 99.95 / 99.97 | `9818eff0fe9c295c5cd6ddee5095c539bffe11fdd0721092324aa79b48ff909d` |
| [live-080-python-urllib-parse-documentatio](https://docs.python.org/3/library/urllib.parse.html) | 100 / 100 / 100 / 100 / 100 | 98.64 / 99.76 / 98.85 / 99.43 / 99.68 | `4693286c6fb62301b47de31d14f86a6fa1914a6e88f3f217ef7c96fbcd9185e7` |
| [live-081-python-csv-documentation](https://docs.python.org/3/library/csv.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 97.94 | `433e634fe27f6ddca78abca1465797e5e61289f1307c4e8dd9c5a5fd946d81c6` |
| [live-082-python-decimal-documentation](https://docs.python.org/3/library/decimal.html) | 100 / 100 / 100 / 100 / 100 | 99.99 / 100.00 / 100.00 / 99.85 / 99.93 | `91a81ba3f441d5c506cb7f201f6984e50cb79d1ac5a1c850ae24825d1f9bb98e` |
| [live-083-python-datetime-documentation](https://docs.python.org/3/library/datetime.html) | 100 / 100 / 100 / 100 / 100 | 99.30 / 99.34 / 99.93 / 99.75 / 96.40 | `1dc3c0df31e95e3df2057f6b14b0dfcae23b63b7ca5d2ab3b2819cb4051243aa` |
| [live-084-python-concurrent-futures-docume](https://docs.python.org/3/library/concurrent.futures.html) | 100 / 100 / 100 / 100 / 100 | 99.92 / 99.87 / 100.00 / 99.69 / 99.90 | `b0e479dafb17a6104e3cadbd95e05a2a5a9d59cf7e3599ae82ea30997553a1a2` |
| [lm-node-intro](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 99.08 / 100.00 | `8ff214c2ca8c679bb9d14dbbee0a87c385d8263dd44ae843ddbcd16728597f68` |
| [live-021-python-common-pathname-manipulations](https://docs.python.org/3/library/os.path.html) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 99.39 / 100.00 | `aa7def82b8b710f8553ef248837c8e84169049d5fae292a2426cc08de716faa3` |
| [lm-feishu-help](https://www.feishu.cn/hc/zh-CN/articles/485770964672-管理者查看企业-ai-功能使用数据) | 100 / 100 / 100 / 100 / 100 | 100.00 / 100.00 / 100.00 / 100.00 / 100.00 | `5c740a73a7d1ea3489b00b372983b21af45b1a3fa34b3f9ff29f22587695f621` |

## Reproduction and limits

Use `uv run --frozen python docs/data_distribution.py --write` and `--check`
for the registered coverage matrix; run `make check` for the maintained regression
suite. `tests/test_body_reference_projection.py` checks materialization/public
binding equivalence, rejection of changed source/bindings and accepted/rejected
body examples. Each changed case retains registered five-region positive,
boundary, weak-region and missing-region regression controls in `reviews.json`.
Actual source qualification additionally requires the external reference and
current controls identified above; CI does not download these live pages.

Before a formal live evaluation, requalify the selected revision against current
initial-page content. Investigate a failure before changing a rule. If content
has changed materially, publish reviewed, versioned reference/rule updates and
retain their provenance; never silently overwrite frozen inputs or tune rules
to provider outputs.

Coverage changes: body cases 243 → 302; section cases 74 → 16; definition cases
1 → 0 (previous PR state → this follow-up). The generated baseline-to-revision
matrix remains in [data.md](data.md). All other 491 cases are unchanged from
PR head `613cd73`; frozen suite files remain unchanged.
The four full frozen-export validations remain deferred: these source checks
neither replace them nor prove them passed. Historical provider outputs have
not been rescored against this follow-up; earlier provider totals describe the
previous PR revision and must not be presented as current results.

## Follow-up: required prose and volatile labels

The October 27 review found two distinct scoring errors outside the 59 projected
bodies. The Python `html` page accepted a missing `html.escape` explanation;
Scrapy and the PostgreSQL tutorial rejected current content because mandatory
facts and anchors retained an old Python minimum version or release banner.

- `live-007`: require the source-backed usage explanation for `html.escape`,
  alongside the existing substantive `html.unescape` fact. Function signatures
  alone do not establish that their explanations were delivered.
- `live-010`: retain cross-platform support, framework description and installation
  requirements, without fixing the current minimum Python version.
- `live-035`: remove the release-announcement banner from facts and anchors;
  preserve the tutorial directory, its count and destinations, prose and length.

Current official-source controls passed for all three cases. Removing either
Python function explanation, the Scrapy framework description, or the PostgreSQL
directory failed. Historical and simulated future Python version labels also
passed. These checks qualify the changed requirements, not provider performance
or the four deferred complete frozen exports. Captures remain outside Git.

A keyword audit of facts and anchors across all five revised suites also found
versioned specification identities (CSS 2.1, XML 1.0, WCAG 2.1, DB-API 2.0),
commit-pinned documentation, navigation labels such as “Release notes”, and
versions discussed in dated articles. Those are not equivalent to a changing
minimum runtime requirement or temporary announcement, and were retained.
This audit is not proof that every live page will remain unchanged.
