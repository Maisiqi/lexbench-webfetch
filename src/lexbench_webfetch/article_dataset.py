"""Compile article contracts against independently reviewed, external full bodies.

The authoring inventory retains unresolved cases. Compilation is fail-closed:
every approved case needs its own complete, hash-bound reference and contract.
No provider, browser adapter or capture orchestration belongs in this module.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from .body_coverage import body_requirements, compact_ngrams
from .models import EvalCase, validate_case
from .paths import contained_path
from .stable_tasks import validate_acceptance_contract

DEFINITIONS = Path(__file__).parent / "definitions/evaluation/articles"


def _acceptance(rule: dict) -> dict:
    acceptance = rule["acceptance_contract"]
    validate_acceptance_contract(acceptance)
    if acceptance["schema"] != "body_text" or not acceptance.get("page_patterns"):
        raise ValueError("Article rules require body text and target identity")
    if any(re.compile(pattern).search("") for pattern in acceptance["page_patterns"]):
        raise ValueError("Article identity patterns cannot match empty text")
    if acceptance.get("stable_text_role", "required") != "required":
        raise ValueError("Declared article stable text must be required")
    reviews = rule.get("stable_text_review")
    if not isinstance(reviews, list) or not rule.get("excluded_regions"):
        raise ValueError("Article rules need stable-region review and exclusions")
    anchor_ids = [anchor["id"] for anchor in acceptance.get("stable_text_anchors", [])]
    if (any(not isinstance(review, dict) for review in reviews)
            or len(reviews) != len(anchor_ids)
            or {review.get("id") for review in reviews} != set(anchor_ids)
            or any(not isinstance(review.get(key), str) or not review[key].strip()
                   for review in reviews for key in ("region", "basis", "observed_on"))):
        raise ValueError("Every declared stable group requires its own source-region review")
    return acceptance


def _base_case(case: dict, rule: dict, acceptance: dict) -> dict:
    task = {
        "id": case["id"], "name": case["name"], "url": case["url"],
        "category": "article", "track": "articles", "task_kind": "body",
        "task_prompt": case["task_prompt"], "expected_any": [], "min_content_chars": 1,
        "acceptance_contract": acceptance,
        "rule_review": {"status": "reviewed", "reason": rule["reason"]},
    }
    validate_case(EvalCase(**task))
    return task


def _compile_post_collection(case: dict, rule: dict, evidence_home: Path) -> dict:
    from .article_posts import validate_post_contract, verify_article_posts
    if case.get("page_type") != "collection":
        raise ValueError("Post collection rules require an explicitly reviewed collection")
    contract = rule["post_contract"]
    validate_post_contract(contract)
    proof = rule["qualification_reference"]
    raw = contained_path(evidence_home, proof["path"], reject_symlinks=True).read_bytes()
    if hashlib.sha256(raw).hexdigest() != proof["sha256"]:
        raise ValueError("Changed article collection qualification reference")
    reference = json.loads(raw)
    records = reference.get("records", [])
    counts = reference.get("source_observation_counts", [])
    if (reference.get("version") != 1 or reference.get("case_id") != case["id"]
            or reference.get("url") != case["url"]
            or reference.get("scope") != "initial_load_only"
            or not isinstance(counts, list) or len(counts) < 2
            or any(type(count) is not int or count < 1 for count in counts)
            or not isinstance(records, list) or not records or len(records) != counts[-1]):
        raise ValueError("Article collections require independent initial-load record review")
    # Validate the historical qualification schema at its captured time. This
    # never certifies freshness for a future evaluation; its caller must provide
    # a separate current reference and execution context to the shared scorer.
    qualification = verify_article_posts(
        "", contract, reference, case_id=case["id"], url=case["url"],
        reference_context={"id": reference.get("context_id"),
                           "started_at": reference.get("observed_at")})
    if qualification["article_reference_status"] != "verified":
        raise ValueError("Every source record needs complete owned post and quote text")
    task = _base_case(case, rule, _acceptance(rule))
    task.update(ground_truth_main_content="", source_benchmark={
        "mode": "article_post_collection", "post_contract": contract,
        "qualification_proof": proof,
    })
    return task


def compile_case(case: dict, rule: dict, evidence_home: Path) -> dict:
    """Require a reviewed complete body; never turn a missing reference into a pass."""
    if rule.get("id") != case["id"] or rule.get("status") != "verified":
        raise ValueError(f"Unresolved article rule: {case['id']}")
    if rule.get("target_kind") == "post_collection":
        return _compile_post_collection(case, rule, evidence_home)
    if rule.get("target_kind") != "fixed_article" or case.get("page_type") == "collection":
        raise ValueError("Collection/post-feed contracts require separate record review")
    proof = rule["body_reference"]
    path = contained_path(evidence_home, proof["path"], reject_symlinks=True)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != proof["sha256"]:
        raise ValueError(f"Changed article reference: {case['id']}")
    body = raw.decode("utf-8")
    if len(body) != proof["chars"] or not body.strip():
        raise ValueError("Empty or incorrectly bound article body")
    scope = rule["reference_scope"]
    if (scope.get("complete_initial_body") is not True
            or not scope.get("start") or not scope.get("end")
            or not body.lstrip().startswith(scope["start"])
            or not body.rstrip().endswith(scope["end"])):
        raise ValueError("Article scope must bind the complete opening and ending")
    acceptance = _acceptance(rule)
    lines = body.splitlines()
    ranges = rule.get("body_regions", [])
    if not 1 <= len(ranges) <= 5:
        raise ValueError("Article scope requires one to five reviewed contiguous regions")
    contract = body_requirements(body)
    regions, next_line = [], 1
    for index, bounds in enumerate(ranges, 1):
        if (not isinstance(bounds, list) or len(bounds) != 2
                or any(type(value) is not int for value in bounds)
                or bounds[0] != next_line or not bounds[0] <= bounds[1] <= len(lines)):
            raise ValueError("Article regions must cover every source line once in order")
        source = "\n".join(lines[bounds[0] - 1:bounds[1]]).strip()
        part = body_requirements(source, structure_hint="whole_declared_component")
        if not part["regions"] or not compact_ngrams(source, 6):
            raise ValueError("Article body cannot yield an empty coverage region")
        region = part["regions"][0]
        region.update(id=f"body-region-{index}", segmentation_method="reviewed_source_lines")
        regions.append(region)
        next_line = bounds[1] + 1
    if next_line != len(lines) + 1:
        raise ValueError("Article regions must include the complete source ending")
    contract.update(regions=regions, segmentation_method="reviewed_source_lines",
                    minimum_region_passes=max(1, len(regions) - 1))
    return {
        **_base_case(case, rule, acceptance),
        "ground_truth_main_content": body,
        "body_requirements": contract,
    }


def compile_dataset(evidence_home: Path, definition_dir: Path = DEFINITIONS) -> dict:
    """Compile the whole approved population, refusing unresolved or omitted cases."""
    sources = {name: (definition_dir / name).read_bytes()
               for name in ("cohort.json", "rules.json")}
    cohort = json.loads(sources["cohort.json"])
    document = json.loads(sources["rules.json"])
    cases, rules = cohort["cases"], document["rules"]
    ids = [case["id"] for case in cases]
    if (cohort.get("schema_version") != 1 or document.get("schema_version") != 1
            or cohort.get("case_count") != len(cases)
            or not ids or len(ids) != len(set(ids))
            or ids != [rule["id"] for rule in rules]):
        raise ValueError("Article cohort and rule inventory differ")
    compiled = [
        compile_case(case, rule, evidence_home) for case, rule in zip(cases, rules)
    ]
    return {
        "schema_version": 1, "id": "articles-v1", "name": "Article retrieval",
        "tool": "web_fetch", "case_count": len(compiled),
        "site_count": len({urlsplit(case["url"]).hostname for case in cases}),
        "runs_per_case": 1, "timeout_ms": 45000, "workers": 1,
        "retry_policy": {"declared_retries": 0,
                         "authoritative_response": "final_physical_call"},
        "interaction_policy": "initial_load_only_no_click_input_scroll_pagination_login_or_ocr",
        "source_bindings": {
            name.replace(".json", "_sha256"): hashlib.sha256(raw).hexdigest()
            for name, raw in sources.items()
        },
        "cases": compiled,
    }
