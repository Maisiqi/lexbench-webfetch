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


@pytest.mark.parametrize('spec,payload,message', [
    ({}, {}, 'Unknown native file projection'),
    ({'format': 'raw_bytes'}, {}, 'requires bytes'),
    ({'format': 'base64_file', 'pointer': ['file']}, {'file': 7}, 'requires text'),
    ({'format': 'base64_file', 'pointer': ['file']}, {'file': '%%%bad'}, 'invalid base64'),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': {}}, 'require objects'),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': [None]}, 'require objects'),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': [{}]}, 'require objects'),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': [{'base64': 7}]}, 'require objects'),
])
def test_native_file_projection_rejects_invalid_shapes(spec, payload, message):
    from lexbench_webfetch.answer_projection import project_native_files
    with pytest.raises(ValueError, match=message):
        project_native_files(payload, {'files': spec})


@pytest.mark.parametrize('spec,payload,expected', [
    ({'format': 'raw_bytes'}, b'PDF bytes', [b'PDF bytes']),
    ({'format': 'raw_bytes'}, b'', []),
    ({'format': 'base64_file', 'pointer': ['file']}, {'file': 'cGRm'}, [b'pdf']),
    ({'format': 'base64_file', 'pointer': ['file']}, {'file': ''}, []),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': [{'base64': 'cGRm'}]}, [b'pdf']),
    ({'format': 'worker_files', 'pointer': ['files']}, {'files': []}, []),
])
def test_native_file_projection_decodes_only_declared_bytes(spec, payload, expected):
    from lexbench_webfetch.answer_projection import project_native_files
    assert project_native_files(payload, {'files': spec}) == expected


def test_optional_result_fields_preserve_empty_but_reject_invented_defaults():
    from lexbench_webfetch.answer_projection import project_native_result_fields
    declaration = {'schema_version': 2, 'result_fields': {
        'title': {'pointer': ['title'], 'format': 'text_or_none'}}}
    assert project_native_result_fields({}, declaration) == {'title': None, 'final_url': None}
    declaration['result_fields']['title']['default'] = None
    assert project_native_result_fields({}, declaration) == {'title': None, 'final_url': None}
    assert project_native_result_fields({'title': 'Native title'}, declaration)['title'] == 'Native title'
    declaration['result_fields']['title']['default'] = 'Invented title'
    with pytest.raises(ValueError, match='defaults must be empty'):
        project_native_result_fields({}, declaration)


@pytest.mark.parametrize('attribute,expected', [
    ('/image.png?crop=10,20 1x, /large.png 2x',
     ['https://example.test/image.png?crop=10,20', 'https://example.test/large.png']),
    ('data:image/png;base64,YQ== 1x, /large.png 2x',
     ['data:image/png;base64,YQ==', 'https://example.test/large.png']),
    ('/one.png, /two.png', ['https://example.test/one.png', 'https://example.test/two.png']),
])
def test_attribute_projection_preserves_commas_inside_urls(attribute, expected):
    declaration = {'schema_version': 2, 'content_format': 'empty', 'answer_fields': {
        'images': {'pointer': ['elements'], 'format': 'html_attribute_urls',
                   'base_url': 'https://example.test/page'}}}
    payload = {'elements': [{'results': [{'attributes': [{'name': 'srcset', 'value': attribute}]}]}]}
    assert project_native_answer(payload, declaration)[1]['images'] == sorted(expected)
