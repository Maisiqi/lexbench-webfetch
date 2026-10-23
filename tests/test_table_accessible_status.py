"""Accessible table graphics retain row and column ownership when opted in."""
import pytest
from lexbench_webfetch.composite_tasks import evaluate_composite_acceptance, validate_composite_acceptance
from lexbench_webfetch.dynamic_lists import scoped_html


def contract():
    return {"version": 1, "groups": [{
        "id": "progress", "kind": "table", "minimum_records": 2,
        "include_table_accessible_names": True, "identity_column": "name",
        "required_columns": [
            {"id": "name", "kind": "text", "aliases": ["Name"]},
            {"id": "complete", "kind": "text", "aliases": ["Complete"],
             "pattern": r"Bar meter with value (?:100|[0-9]{1,2}) out of 100"},
        ],
    }]}


def table(graphic='<svg aria-label="Bar meter with value 20 out of 100"></svg>', *, wrapper=""):
    return ('<table ' + wrapper + '><thead><tr><th>Name</th><th>Complete</th></tr></thead><tbody>'
            + ''.join(f'<tr><th scope="row">{name}</th><td>{graphic}</td></tr>' for name in ('Alan', 'Bryan'))
            + '</tbody></table>')


def result(content, rules=None):
    return evaluate_composite_acceptance(content, rules or contract(), base_url='https://example.test')


def test_named_status_graphics_count_in_their_own_rows():
    assert result(table())['composite_acceptance_pass']


def test_existing_contracts_do_not_gain_graphic_names():
    rules = contract()
    del rules['groups'][0]['include_table_accessible_names']
    assert not result(table(), rules)['composite_acceptance_pass']
    rules['groups'][0]['include_table_accessible_names'] = False
    assert not result(table(), rules)['composite_acceptance_pass']


@pytest.mark.parametrize('graphic', [
    '<svg></svg>', '<svg aria-label=" "></svg>',
    '<svg title="Bar meter with value 20 out of 100"></svg>',
    '<svg data-value="20" aria-valuenow="20"></svg>',
    '<img alt="Bar meter with value 20 out of 100">',
    '<svg aria-label="Download"></svg>',
    '<svg aria-label="Bar meter with value 120 out of 100"></svg>',
    '<svg aria-hidden="true" aria-label="Bar meter with value 20 out of 100"></svg>',
    '<svg hidden aria-label="Bar meter with value 20 out of 100"></svg>',
    '<svg style="display:none" aria-label="Bar meter with value 20 out of 100"></svg>',
    '<span aria-hidden="TRUE"><svg aria-label="Bar meter with value 20 out of 100"></svg></span>',
    '<span hidden><svg aria-label="Bar meter with value 20 out of 100"></svg></span>',
    '<span style="visibility:hidden"><svg aria-label="Bar meter with value 20 out of 100"></svg></span>',
])
def test_unavailable_or_unrelated_graphics_do_not_supply_status(graphic):
    assert not result(table(graphic))['composite_acceptance_pass']


@pytest.mark.parametrize('wrapper', ['hidden', 'aria-hidden="true"', 'style="opacity:0"'])
def test_hidden_table_cannot_supply_accessible_names(wrapper):
    assert not result(table(wrapper=wrapper))['composite_acceptance_pass']


def test_status_must_belong_to_complete_column():
    wrong = '<table><tr><th>Name</th><th>Complete</th></tr>' + ''.join(
        f'<tr><td>{name}<svg aria-label="Bar meter with value 20 out of 100"></svg></td><td></td></tr>'
        for name in ('Alan', 'Bryan')) + '</table>'
    assert not result(wrong)['composite_acceptance_pass']


def test_missing_or_duplicate_rows_do_not_meet_count():
    assert not result(table().replace('Bryan', 'Alan'))['composite_acceptance_pass']
    assert not result(table().replace('<tr><th scope="row">Bryan</th><td><svg aria-label="Bar meter with value 20 out of 100"></svg></td></tr>', ''))['composite_acceptance_pass']


def test_visible_aria_hidden_text_keeps_existing_visual_semantics():
    assert scoped_html('<p aria-hidden="true">Visible label</p>').get_text() == 'Visible label'
    assert result(table('Bar meter with value 20 out of 100', wrapper='aria-hidden="true"'))['composite_acceptance_pass']


def test_markdown_text_status_still_passes():
    markdown = '| Name | Complete |\n| --- | --- |\n| Alan | Bar meter with value 20 out of 100 |\n| Bryan | Bar meter with value 30 out of 100 |'
    assert result(markdown)['composite_acceptance_pass']


@pytest.mark.parametrize('value', [1, 'true', None, {}, []])
def test_option_requires_boolean(value):
    rules = contract()
    rules['groups'][0]['include_table_accessible_names'] = value
    with pytest.raises(ValueError, match='boolean table option'):
        validate_composite_acceptance(rules)


def test_option_is_not_available_to_other_group_kinds():
    rules = contract()
    rules['groups'][0]['kind'] = 'linked_table'
    with pytest.raises(ValueError, match='boolean table option'):
        validate_composite_acceptance(rules)
