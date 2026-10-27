"""Mixed native list and non-list descriptions keep independent ownership."""
import pytest
from lexbench_webfetch.stable_tasks import evaluate_stable_task, source_record_hash

CARD = '<section><p>Beta</p><p>Second complete description.</p></section>'
LIST = '<ul><li><a>Alpha</a><p>First complete description.</p></li></ul>'


def contract(minimum):
    return {'version': 1, 'schema': 'name_description', 'minimum_records': minimum,
            'stable_text_anchors': []}


@pytest.mark.parametrize('closed', [False, True])
@pytest.mark.parametrize('list_first', [False, True])
def test_owned_list_and_non_list_record_are_both_kept_once(closed, list_first):
    html = '<main>' + (LIST + CARD if list_first else CARD + LIST) + '</main>'
    result = evaluate_stable_task(html, contract(2), allow_closed_title_cards=closed)
    assert result['stable_task_pass'], result
    assert result['stable_complete_record_count'] == result['stable_unique_record_count'] == 2
    assert {r['fields']['name'] for r in result['stable_records']} == {'Alpha', 'Beta'}
    assert sorted(r['fields']['description'] for r in result['stable_records']) == [
        'First complete description.', 'Second complete description.']


@pytest.mark.parametrize('extra', [
    '<ul><li><p>name</p><p>description</p></li></ul>',
    '<ul><li>Orphan title</li></ul>',
    '<ul><li><p>Parent name</p><p>Parent description.</p><ul>'
    '<li><p>name</p><p>description</p></li></ul></li></ul>',
])
def test_invalid_list_cannot_suppress_or_contaminate_fixed_non_list_record(extra):
    rule = contract(1)
    fields = ['description', 'name']
    rule['source_membership'] = {'kind': 'fixed', 'fields': fields,
        'record_hashes': [source_record_hash(
            {'name': 'Beta', 'description': 'Second complete description.'},
            fields, 'name_description')]}
    result = evaluate_stable_task('<main>' + extra + CARD + '</main>', rule,
                                  allow_closed_title_cards=True)
    assert result['stable_task_pass'], result
    assert result['stable_complete_record_count'] == result['stable_unique_record_count'] == 1
    assert result['stable_source_membership'] == 'fixed'
    assert 'source_record_mismatch' not in result['stable_task_errors']


def test_nested_owned_list_does_not_reappear_as_non_list_record():
    html = '<main><ul><li>Category<ul><li><p>Alpha</p><p>First complete description.</p>' \
           '</li></ul></li></ul>' + CARD + '</main>'
    result = evaluate_stable_task(html, contract(2), allow_closed_title_cards=True)
    assert result['stable_task_pass'], result
    assert result['stable_complete_record_count'] == result['stable_unique_record_count'] == 2


def test_missing_non_list_description_cannot_borrow_from_owned_list():
    html = '<main><section><p>Beta</p></section>' + LIST + '</main>'
    result = evaluate_stable_task(html, contract(2), allow_closed_title_cards=True)
    assert not result['stable_task_pass']
    assert result['stable_complete_record_count'] == 1
