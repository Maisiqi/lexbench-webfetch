"""Extraction policy varies through data without provider-specific code paths."""
import pytest
from lexbench_webfetch.rule_policy import POLICY_PATH, SCORER_POLICY
from lexbench_webfetch.dynamic_reference import entry_facts
from lexbench_webfetch.list_verification import identity
from lexbench_webfetch.article_comments import valid_comment_records
from lexbench_webfetch.scoring import SCORING_SOURCE_FILES


def test_policy_is_part_of_scorer_identity():
    assert POLICY_PATH in SCORING_SOURCE_FILES
    assert SCORER_POLICY['version'] == 1


def test_unseen_dynamic_case_uses_declared_fields_and_rejects_missing_fields(monkeypatch):
    monkeypatch.setitem(SCORER_POLICY['dynamic_cases'], 'new-independent-case', {
        'fields': ['name', 'price', 'shipping'],
        'optional_fields': [{'field': 'shipping', 'index': -1, 'equals': 'Delivery included'}]})
    assert [x['id'] for x in entry_facts('new-independent-case', ['Example\n12\nDelivery included'])] == [
        'entry-1-name', 'entry-1-price', 'entry-1-shipping']
    assert len(entry_facts('new-independent-case', ['Example\n12'])) == 2
    with pytest.raises(ValueError):
        entry_facts('new-independent-case', ['Example'])
    with pytest.raises(ValueError):
        entry_facts('new-independent-case', ['Example\n12\nUnrecognized badge'])
    with pytest.raises(ValueError):
        entry_facts('undeclared', ['Example\n12'])


def test_new_host_identity_is_scoped_to_declared_host(monkeypatch):
    monkeypatch.setitem(SCORER_POLICY, 'list_identity', [
        {'host': 'example.test', 'pattern': r'/item/(\d+)(?:/|$)', 'prefix': '/item/', 'group': 1}])
    assert identity('https://example.test/item/123/title') == 'example.test/item/123'
    assert identity('https://other.test/item/123/title') == 'other.test/item/123/title'
    assert identity('https://example.test/item/abc/title') == 'example.test/item/abc/title'


@pytest.mark.parametrize('label', SCORER_POLICY['article_labels']['COMMENT_CONTROLS'] +
                         SCORER_POLICY['article_labels']['COMMENT_PLACEHOLDERS'])
def test_migrated_labels_still_reject_non_content_without_substring_filtering(label):
    assert not valid_comment_records([{'author': 'Reader', 'text': label}])
    assert valid_comment_records([{'author': 'Reader', 'text': 'I discuss ' + label + ' in this sentence.'}])
