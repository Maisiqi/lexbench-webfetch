"""Projection defaults cannot introduce facts absent from native responses."""
import json

import pytest

from lexbench_webfetch.answer_projection import project_native_answer
from lexbench_webfetch.metrics import task_passed
from lexbench_webfetch.scoring import score_attempt


@pytest.mark.parametrize('field,default', [
    ('images', ['https://example.test/forged.png']),
    ('links', [{'text': 'Invented', 'href': 'https://example.test/forged'}]),
    ('extras', {'images': ['https://example.test/forged.png']}),
    ('videos', ['https://example.test/forged.mp4']),
])
def test_nonempty_defaults_cannot_supply_native_answers(field, default):
    declaration = {'schema_version': 2, 'content_format': 'text',
                   'content_pointer': ['content'], 'answer_fields': {
                       field: {'pointer': [field], 'default': default}}}
    case = {'url': 'https://example.test/page', 'expected_any': [],
            'task_kind': 'resource', 'content_score_applicable': False,
            'expected_resources': [{'id': 'asset', 'urls': ['https://example.test/forged.png']}]}
    with pytest.raises(ValueError, match='defaults must be empty'):
        score_attempt(case, b'', ok=True, native_response=b'{"content":""}',
                      metadata={'native_answer_projection': declaration, field: default})


@pytest.mark.parametrize('present', [False, True])
def test_empty_default_keeps_missing_and_native_resource_distinct(present):
    url = 'https://example.test/native.png'
    payload = {'content': '', **({'images': [url]} if present else {})}
    declaration = {'schema_version': 2, 'content_format': 'text',
                   'content_pointer': ['content'], 'answer_fields': {
                       'images': {'pointer': ['images'], 'default': []}}}
    content, fields = project_native_answer(payload, declaration)
    case = {'url': 'https://example.test/page', 'expected_any': [],
            'task_kind': 'resource', 'content_score_applicable': False,
            'expected_resources': [{'id': 'asset', 'urls': [url]}]}
    metrics = score_attempt(case, content.encode(), ok=True,
                           native_response=json.dumps(payload).encode(),
                           metadata={'native_answer_projection': declaration, **fields})
    assert task_passed(True, metrics, 'resource') is present
