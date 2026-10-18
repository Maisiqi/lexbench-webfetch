# Evaluation protocol

A sample is one declared method–task logical result. Choose the complete task population, methods, versions, repetitions, timeout, concurrency and retry policy before calls. Keep the four suites separate unless a combined population and deduplication policy were declared in advance.

## Inputs and delivery

Use the original dataset verified by the suite's `source-inputs.json`. The public `tasks.json` exposes task requirements for inspection and integration; it omits complete reference text and capture metadata and cannot replace the executable frozen dataset. The original catalog binds complete task definitions through SHA-256.

A method receives the task URL and prompt. Follow the declared task kind: return body text, structured records with the required identities and links, discover the specified resources, or deliver the requested file. A successful HTTP request or nonempty response alone is insufficient. Method-specific alternate task requirements are not allowed.

Task requirements are data: expected markers, fact groups, forbidden output, minimum length, body coverage, structure and resource/file contracts are selected by the task. Missing reference coverage is unavailable, not zero or a perfect score. Binary task acceptance and text-quality diagnostics are separate. LexBench owns `score_attempt`, the shared `task_passed` predicate and file-byte acceptance. Browser Eval calls the same installed implementations. Other harnesses can use `lexbench_webfetch.evaluation.evaluate_response` or the `score` command without Browser Eval; disclose the benchmark/scorer revision when comparing scores.

When an adapter selects answer fields from a retained native response, validate that projection before scoring. `score_attempt` accepts `native_response`, `native_files` and `native_diagnostic` for this check; the execution harness owns persistence and hash verification. Declare every score-bearing body, metadata, file, title and final-URL source. Missing-field defaults may only be empty; they cannot supply an answer absent from the response. Direct `evaluate_response` and CLI inputs are the submitted answer itself, so their caller remains responsible for acquisition provenance.

## Live sources and frozen evidence

Input validation proves that supplied bytes match the frozen version. It does not prove that a live website still matches that version. A publishable live-site cohort must independently verify task-relevant reference scope before calls and again after the complete declared scope. If source content changes, preserve the attempt and investigate the shared cause; do not silently refresh references or omit failed cases.

Retain the benchmark commit, suite and dataset hashes, every physical call, raw output, delivered files, exact acceptance result, error, method version and evaluator revision. Hash-bind any auxiliary evidence. Keep credentials, cookies, private page captures and internal execution logs out of public packages. The benchmark code license grants no redistribution rights to third-party content.

## Scores and timing

Report task acceptance as passed/evaluated with the declared denominator and unavailable count. Give each metric its unit and population. Report mean, P50 and P95 over the same population. Retain failed calls in the declared cohort; report all-call timing separately from each method's conditional successful-call distribution. A success-only latency distribution does not describe all attempted tasks.

Declare the score-bearing call and timing boundary before execution. If retries are allowed, retain every call, select the final response rather than the best response, and report total retry execution cost separately from any final-call latency. One retried task remains one logical sample. Record warm/cold start, local/remote execution, conversion and network differences.

## Results and corrections

A result submission must identify the immutable input and code revisions, full declared method–task matrix, saved output hashes, verdicts and denominators, errors, timing boundaries, missing results, source verification and review scope. Keep measured artifacts in a separately licensed evidence release with a stable location and integrity manifest. No leaderboard or automatic submission service is maintained here.

A requirement correction creates a new benchmark revision, with accepted and rejected scenario controls. A scoring implementation correction must fix the shared cause and rescore the complete affected scope without overwriting prior evidence. Changes to execution inputs require new calls. Independent result review is a separate operation; machine checks do not imply human review.
