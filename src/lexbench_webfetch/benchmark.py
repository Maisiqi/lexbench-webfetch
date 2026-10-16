"""Verify public definitions and materialize independently acquired frozen inputs."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath

SUITES = Path(__file__).parent / "suites"

# Full reference bodies and source-capture/review payloads stay in frozen inputs.
PUBLIC_TASK_FIELDS = (
    "id", "name", "url", "category", "track", "task_kind", "description", "task_prompt",
    "expected_any", "required_facts", "forbidden_any", "min_content_chars",
    "fact_coverage_threshold", "expected_resources", "resource_output_contract",
    "content_score_applicable", "required_patterns", "acceptance_contract",
    "composite_acceptance", "mutable_body_policy", "body_requirements", "retrieval_hints",
    "source_review_url", "evaluation_url", "expected_final_url", "expected_document_language",
    "expected_document_language_present", "target_language", "target_region",
)


def reference_bindings(value):
    """Keep body-rule structure while binding external reference payloads."""
    if isinstance(value, list):
        return [reference_bindings(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in {"text", "source_text"}:
            if not isinstance(item, str):
                raise ValueError("Body reference text must be a string")
            result[key + "_binding"] = {
                "sha256": hashlib.sha256(item.encode()).hexdigest(), "chars": len(item)}
        else:
            result[key] = reference_bindings(item)
    return result


def public_task(case: dict) -> dict:
    task = {key: case[key] for key in PUBLIC_TASK_FIELDS if key in case}
    if "body_requirements" in task:
        task["body_requirements"] = reference_bindings(task["body_requirements"])
    benchmark = case.get("source_benchmark", {})
    routing = {key: benchmark[key] for key in
               ("mode", "hosts", "entry_path", "minimum_entries", "verification_scope")
               if key in benchmark}
    navigation = benchmark.get("risk_control", {}).get("navigation_contract")
    if navigation is not None:
        routing["risk_control"] = {"navigation_contract": navigation}
    if routing:
        task["source_benchmark"] = routing
    review = case.get("rule_review", {})
    if review:
        task["rule_review"] = {key: review[key] for key in ("status", "reason") if key in review}
    return task


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative:
        raise ValueError(f"Unsafe input path: {relative}")
    target = root / relative
    for part in (root, *target.parents, target):
        if part.is_symlink():
            raise ValueError(f"Symlinked input: {part}")
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Escaping input: {relative}")
    return target


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def registry() -> dict:
    document = read(SUITES / "registry.json")
    if document.get("schema_version") != 1:
        raise ValueError("Unsupported suite registry")
    ids = [row["id"] for row in document["suites"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate suite ID")
    return document


def suite(identifier: str) -> tuple[dict, Path]:
    matches = [row for row in registry()["suites"] if row["id"] == identifier]
    if len(matches) != 1:
        raise ValueError(f"Unknown suite: {identifier}")
    entry = matches[0]
    root = bound_path(SUITES, identifier)
    for relative, expected in entry["files"].items():
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid SHA-256: {relative}")
        if digest(bound_path(root, relative)) != expected:
            raise ValueError(f"Changed suite file: {identifier}/{relative}")
    return entry, root


def validate(identifier: str) -> dict:
    entry, root = suite(identifier)
    catalog = read(root / "dataset-catalog.json")
    tasks = read(root / "tasks.json")
    manifest = read(root / "source-inputs.json")
    if (manifest.get("schema_version") != 2
            or manifest.get("kind") != "frozen_reference_inputs"
            or manifest["catalog_sha256"] != digest(root / "dataset-catalog.json")
            or manifest["dataset_sha256"] != catalog["dataset_sha256"]
            or manifest["files"].get(manifest["dataset"]) != manifest["dataset_sha256"]):
        raise ValueError("Inconsistent frozen input bindings")
    if not (entry["dataset_id"] == catalog["id"] == tasks["id"]):
        raise ValueError("Inconsistent dataset identity")
    declared = catalog["cases"]
    cases = tasks["cases"]
    ids = [case["id"] for case in cases]
    if (len(ids) != len(set(ids)) or ids != [case["id"] for case in declared]
            or len(ids) != entry["case_count"] or len(ids) != catalog["case_count"]):
        raise ValueError("Inconsistent task inventory")
    for task, row in zip(cases, declared):
        for key in ("id", "name", "url", "category", "track", "task_prompt"):
            if key in row and row[key] != task.get(key):
                raise ValueError(f"Task catalog mismatch: {task['id']}/{key}")
    for relative, expected in input_files(manifest).items():
        bound_path(root, relative)
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid input SHA-256: {relative}")
    return {"suite": identifier, "case_count": len(ids), "dataset_sha256": catalog["dataset_sha256"]}


def input_files(manifest: dict) -> dict[str, str]:
    files = dict(manifest["files"])
    for tree, items in manifest["trees"].items():
        for relative, expected in items.items():
            name = f"{tree}/{relative}"
            if name in files:
                raise ValueError(f"Duplicate input: {name}")
            files[name] = expected
    return files


def verify_inputs(identifier: str, source: Path) -> dict:
    result = validate(identifier)
    _, root = suite(identifier)
    manifest = read(root / "source-inputs.json")
    for relative, expected in input_files(manifest).items():
        if digest(bound_path(source, relative)) != expected:
            raise ValueError(f"Changed frozen input: {relative}")
    dataset = read(bound_path(source, manifest["dataset"]))
    catalog = read(root / "dataset-catalog.json")
    if (len(dataset["cases"]) != catalog["case_count"]
            or any(dataset.get(k) != catalog.get(k) for k in ("id", "name", "coverage_plan"))):
        raise ValueError("Frozen dataset inventory differs from catalog")
    tasks = read(root / "tasks.json")["cases"]
    for case, row, task in zip(dataset["cases"], catalog["cases"], tasks):
        encoded = json.dumps(case, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != row["definition_sha256"]:
            raise ValueError(f"Changed task definition: {row['id']}")
        if public_task(case) != task:
            raise ValueError(f"Public task differs from frozen input: {row['id']}")
    return result


def export(identifier: str, source: Path, output: Path) -> Path:
    """Copy only declared inputs after verification; never overwrite a run or input tree."""
    verify_inputs(identifier, source)
    if output.exists() or output.is_symlink():
        raise ValueError("Output must be a new directory")
    if not output.parent.is_dir():
        raise ValueError("Output parent must exist")
    _, root = suite(identifier)
    manifest = read(root / "source-inputs.json")
    stage = Path(tempfile.mkdtemp(prefix=".lexbench-", dir=output.parent))
    try:
        for relative in input_files(manifest):
            target = bound_path(stage, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(bound_path(source, relative), target)
        verify_inputs(identifier, stage)
        # A materialized dataset is intentionally independent of the historical
        # Browser Eval external-input resolver; do not copy source-inputs.json.
        os.rename(stage, output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output / manifest["dataset"]
