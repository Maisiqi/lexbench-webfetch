"""Native list items own their name/description without borrowing siblings."""
import pytest
from lexbench_webfetch.stable_tasks import evaluate_stable_task

CONTRACT = {'version': 1, 'schema': 'name_description', 'minimum_records': 2,
            'stable_text_anchors': []}

@pytest.mark.parametrize('second,passed', [
    ('<a>Beta</a><p>Second description.</p>', True),
    ('<a>Beta</a>', False),
    ('<p>Second description.</p>', False),
    ('<a>Alpha</a><p>First description.</p>', False),
])
def test_native_list_ownership(second, passed):
    html = '<main><ul><li><a>Alpha</a><p>First description.</p></li><li>' + second + '</li></ul></main>'
    assert evaluate_stable_task(html, CONTRACT)['stable_task_pass'] is passed


def test_nested_list_is_not_counted_twice_and_hidden_item_cannot_count():
    html = '<ul><li><ul><li><a>Alpha</a><p>First description.</p></li></ul></li>' \
           '<li style="display:none"><a>Beta</a><p>Second description.</p></li></ul>'
    result = evaluate_stable_task(html, CONTRACT)
    assert result['stable_complete_record_count'] == 1
    assert not result['stable_task_pass']
