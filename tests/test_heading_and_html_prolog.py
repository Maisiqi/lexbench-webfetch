"""Page anchors accept visible headings and ignore HTML prolog comments."""
import pytest

from lexbench_webfetch.metrics import task_passed
from lexbench_webfetch.scoring import score_attempt


@pytest.mark.parametrize('answer,passed', [
    ('Alpha\n## Beta', True), ('Alpha\n   ### Beta ###', True),
    ('Alpha\n#Beta', False), ('Alpha\n####### Beta', False),
    ('Alpha\n\\## Beta', False), ('Alpha\n    ## Beta', False),
    ('Alpha\n## Wrong', False), ('```\nAlpha\n## Beta\n```', False),
    ('~~~\nAlpha\n## Beta\n~~~', False),
])
def test_only_atx_markers_are_presentation(answer, passed):
    case = {'url': 'https://example.test/page', 'min_content_chars': 1,
            'acceptance_contract': {'version': 1, 'schema': 'body_text', 'minimum_records': 0,
                'stable_text_anchors': [{'id': 'title', 'alternatives': ['Alpha Beta']}]}}
    metrics = score_attempt(case, answer.encode(), ok=True)
    assert task_passed(True, metrics) is passed


@pytest.mark.parametrize('prolog', ['', '<!DOCTYPE html>', '<!-- layout -->',
                                    '<!DOCTYPE html><!-- layout -->\n<!-- another -->'])
@pytest.mark.parametrize('body,passed', [('<h1>Public Page</h1>', True),
                                       ('<p data-title="Public Page">Other text</p>', False),
                                       ('<!-- Public Page --><p>Other text</p>', False),
                                       ('<script>Public Page</script><p>Other text</p>', False)])
def test_comments_before_html_do_not_change_visible_anchor_scope(prolog, body, passed):
    case = {'url': 'https://example.test/page', 'min_content_chars': 1,
            'acceptance_contract': {'version': 1, 'schema': 'body_text', 'minimum_records': 0,
                'stable_text_anchors': [{'id': 'title', 'alternatives': ['Public Page']}]}}
    metrics = score_attempt(case, (prolog+'<html><body>'+body+'</body></html>').encode(), ok=True)
    assert task_passed(True, metrics) is passed
