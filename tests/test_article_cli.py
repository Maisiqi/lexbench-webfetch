"""The standalone scorer must preserve the independent reference boundary."""
import json
import subprocess
import sys

import pytest


@pytest.mark.parametrize("context,passed,status", [
    ({"id": "run-1", "started_at": "2026-10-19T01:00:00Z"}, True, "verified"),
    (None, False, "context_mismatch"),
    ({"id": "another-run", "started_at": "2026-10-19T01:00:00Z"}, False, "context_mismatch"),
    ({"id": "run-1", "started_at": "2026-10-19T02:00:00Z"}, False, "stale"),
])
def test_cli_scores_posts_only_with_matching_fresh_context(tmp_path, context, passed, status):
    body = ("Orchard workers recorded every tree before sunrise. They inspected "
            "the irrigation channels and published the complete harvest schedule.")
    task = {
        "id": "post-feed", "name": "Article feed", "url": "https://example.test/feed",
        "category": "article", "track": "articles", "task_kind": "body", "expected_any": [],
        "acceptance_contract": {"version": 1, "schema": "body_text", "minimum_records": 0,
                                "page_patterns": ["Article feed"]},
        "source_benchmark": {"mode": "article_post_collection", "post_contract": {
            "version": 1, "hosts": ["example.test"], "entry_path": r"/post/[0-9]+",
            "html_record_selector": "article", "html_permalink_selector": "a.time",
            "html_author_selector": ".author", "html_body_selector": ".body",
            "required_ratio": 1, "max_reference_age_seconds": 900,
        }},
    }
    reference = {
        "version": 1, "case_id": task["id"], "url": task["url"],
        "scope": "initial_load_only", "context_id": "run-1",
        "observed_at": "2026-10-19T00:59:00Z", "records": [{
            "url": "https://example.test/post/1", "author": "Alice",
            "body_parts": [{"kind": "post", "text": body, "complete_initial_text": True}],
        }],
    }
    for name, value in (("task", task), ("reference", reference), ("context", context)):
        (tmp_path / f"{name}.json").write_text(json.dumps(value))
    (tmp_path / "answer.txt").write_text(
        "# Article feed\n\n## Alice [Today](https://example.test/post/1)\n\n" + body)
    command = [sys.executable, "-m", "lexbench_webfetch.cli", "score",
               "--task", str(tmp_path / "task.json"),
               "--response", str(tmp_path / "answer.txt"),
               "--list-reference", str(tmp_path / "reference.json")]
    if context is not None:
        command += ["--reference-context", str(tmp_path / "context.json")]
    result = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    scored = json.loads(result.stdout)
    assert scored["passed"] is passed
    assert scored["measured"] is passed
    assert scored["metrics"]["article_reference_status"] == status


def test_cli_rejects_non_object_reference_context(tmp_path):
    (tmp_path / "context.json").write_text("[]")
    result = subprocess.run([
        sys.executable, "-m", "lexbench_webfetch.cli", "score",
        "--task", str(tmp_path / "unused-task.json"),
        "--response", str(tmp_path / "unused-answer.txt"),
        "--reference-context", str(tmp_path / "context.json"),
    ], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 1
    assert "Reference context must be a JSON object" in result.stderr
