"""The standalone scorer must preserve the independent reference boundary."""
import json
import subprocess
import sys

import pytest


@pytest.mark.parametrize("include_body,passed", [(True, True), (False, False)])
def test_cli_scores_fixed_posts_without_runtime_reference(tmp_path, include_body, passed):
    body = ("Orchard workers recorded every tree before sunrise. They inspected "
            "the irrigation channels and published the complete harvest schedule.")
    task = {
        "id": "post-feed", "name": "Article feed", "url": "https://example.test/feed",
        "category": "article", "track": "articles", "task_kind": "body", "expected_any": [],
        "acceptance_contract": {"version": 1, "schema": "body_text", "minimum_records": 0,
                                "page_patterns": ["Article feed"]},
        "source_benchmark": {"mode": "article_post_collection", "post_contract": {
            "version": 2, "hosts": ["example.test"], "entry_path": r"/post/[0-9]+",
            "html_record_selector": "article", "html_permalink_selector": "a.time",
            "html_author_selector": ".author", "html_body_selector": ".body",
            "minimum_posts": 1,
        }},
    }
    (tmp_path / "task.json").write_text(json.dumps(task))
    (tmp_path / "answer.txt").write_text(
        "# Article feed\n\n## Alice [Today](https://example.test/post/1)\n\n" + (body if include_body else ""))
    command = [sys.executable, "-m", "lexbench_webfetch.cli", "score",
               "--task", str(tmp_path / "task.json"),
               "--response", str(tmp_path / "answer.txt")]
    result = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    scored = json.loads(result.stdout)
    assert scored["passed"] is passed
    assert scored["measured"] is True
    assert "article_reference_status" not in scored["metrics"]


@pytest.mark.parametrize("argument", ["--comments-reference", "--reference-context"])
def test_cli_rejects_removed_reference_arguments(tmp_path, argument):
    result = subprocess.run([
        sys.executable, "-m", "lexbench_webfetch.cli", "score",
        "--task", str(tmp_path / "unused-task.json"),
        "--response", str(tmp_path / "unused-answer.txt"),
        argument, str(tmp_path / "unused-reference.json"),
    ], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr
