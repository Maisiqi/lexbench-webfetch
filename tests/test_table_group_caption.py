"""Caption fields belong to subsequent records in the same table section."""
import copy
import pytest
from lexbench_webfetch.composite_tasks import evaluate_composite_acceptance, validate_composite_acceptance


def contract():
    return {'version': 1, 'groups': [{
        'id': 'orders', 'kind': 'table', 'minimum_records': 2, 'identity_column': 'id',
        'required_columns': [
            {'id': 'id', 'kind': 'integer', 'aliases': ['ID']},
            {'id': 'name', 'kind': 'text', 'aliases': ['Name']}],
        'group_caption': {
            'table_selector': 'table.orders', 'row_selector': 'tr.record',
            'cell_selector': 'td:not(.hidden)', 'caption_selector': 'tr.caption',
            'pattern': r'Country: (?P<value>[A-Za-z ]+) - \d+ items',
            'field': {'id': 'country', 'kind': 'text', 'aliases': ['Country']},
        }}]}


def row(i):
    return f'<tr class="record"><td>{i}</td><td>Person {i}</td><td class="hidden">Wrong</td></tr>'


def caption(country='Argentina', attrs=''):
    return f'<tr class="caption" {attrs}><td colspan="2">Country: {country} - 2 items</td></tr>'


def table(body):
    return '<table class="orders"><tbody>' + body + '</tbody></table>'


def result(source, rules=None):
    return evaluate_composite_acceptance(source, rules or contract(), base_url='https://example.test')


def test_html_caption_binds_each_following_row():
    report = result(table(caption() + row(1) + caption('Brazil') + row(2)))
    assert report['composite_acceptance_pass']
    records = report['composite_group_results'][0]['records']
    assert [x['country'] for x in records] == ['Argentina', 'Brazil']


@pytest.mark.parametrize('source', [
    table(row(1) + row(2)),
    table(row(1) + row(2) + caption()),
    '<table>' + caption() + '</table>' + table(row(1) + row(2)),
    table(caption()) + table(row(1) + row(2)),
    table(caption(attrs='hidden') + row(1) + row(2)),
    table(caption(attrs='style="display:none"') + row(1) + row(2)),
    table(caption() + row(1) + caption('') + row(2)),
    table(caption() + '</tbody><tbody>' + row(1) + row(2)),
    table(caption() + row(1)),
])
def test_missing_hidden_late_or_other_table_caption_cannot_supply_rows(source):
    assert not result(source)['composite_acceptance_pass']


def test_markdown_caption_rows_bind_and_reset():
    source = '| ID | Name |\n| --- | --- |\n| Country: Argentina - 2 items |\n| 1 | One |\n| Country: Brazil - 2 items | |\n| 2 | Two |'
    assert result(source)['composite_acceptance_pass']
    assert not result(source.replace('| Country: Argentina - 2 items |\n', ''))['composite_acceptance_pass']
    assert not result(source.replace('| Country: Brazil - 2 items | |', '| Country: - 2 items |'))['composite_acceptance_pass']


def test_markdown_caption_cannot_cross_table_boundary():
    source = '| ID | Name |\n| --- | --- |\n| Country: Argentina - 2 items |\n\n| ID | Name |\n| --- | --- |\n| 1 | One |\n| 2 | Two |'
    assert not result(source)['composite_acceptance_pass']


def test_undeclared_contract_retains_existing_behavior():
    rules = contract(); del rules['groups'][0]['group_caption']
    assert result('| ID | Name |\n| --- | --- |\n| 1 | One |\n| 2 | Two |', rules)['composite_acceptance_pass']


@pytest.mark.parametrize('change', [
    {'pattern': '(.*)'}, {'pattern': '(?P<value>.*)'},
    {'field': {'id': 'id', 'kind': 'text', 'aliases': ['Country']}},
    {'table_selector': ''}, {'extra': True},
    {'field': {'aliases': ['Country']}},
    {'field': {'id': 'country', 'kind': 'unknown', 'aliases': ['Country']}},
    {'field': None},
])
def test_invalid_caption_contract_rejected(change):
    rules = contract(); rules['groups'][0]['group_caption'].update(change)
    with pytest.raises(ValueError): validate_composite_acceptance(rules)


@pytest.mark.parametrize('source', [
    '| ID | Name | Country |\n| --- | --- | --- |\n| 1 | One | Argentina |\n| 2 | Two | Brazil |',
    '<table><tr><th>ID</th><th>Name</th><th>Country</th></tr><tr><td>1</td><td>One</td><td>Argentina</td></tr><tr><td>2</td><td>Two</td><td>Brazil</td></tr></table>',
])
def test_explicit_normalized_country_column_is_accepted(source):
    assert result(source)['composite_acceptance_pass']


def test_actual_header_is_not_replaced_with_invented_header():
    header = '<tr><th>Wrong</th><th>Name</th></tr>'
    assert not result(table(header + caption() + row(1) + row(2)))['composite_acceptance_pass']
    header = '<tr><th>Name</th><th>ID</th></tr>'
    assert not result(table(header + caption() + row(1) + row(2)))['composite_acceptance_pass']


def test_equal_rows_outside_selector_are_not_selected_by_value():
    from lexbench_webfetch.structured_tables import grouped_table_surface
    group = contract()['groups'][0]
    group['group_caption']['row_selector'] = 'tr.record:nth-child(n+3)'
    source = table(caption() + row(1) + row(1) + row(2))
    surface = grouped_table_surface(source, group)
    assert surface.count('| 1 | Person 1 | Argentina |') == 1
    assert surface.count('| 2 | Person 2 | Argentina |') == 1


@pytest.mark.parametrize('selector', ['table.orders', 'tr.record', 'tbody'])
def test_caption_expansion_preserves_table_exclusions(selector):
    rules = contract()
    rules['groups'][0]['table_scope'] = {'exclude_selector': selector}
    source = table(caption() + row(1) + row(2))
    assert result(source)['composite_acceptance_pass']
    assert not result(source, rules)['composite_acceptance_pass']


@pytest.mark.parametrize('prefix', ['', '<table><tr><th>Other</th></tr></table>\n'])
def test_mixed_html_preserves_markdown_caption_rows(prefix):
    source = '| ID | Name |\n| --- | --- |\n| Country: Argentina - 2 items |\n| 1 | One |\n| 2 | Two |'
    assert result(prefix + source)['composite_acceptance_pass']
    assert not result(prefix + source.replace('| Country: Argentina - 2 items |\n', ''))['composite_acceptance_pass']


@pytest.mark.parametrize('name', [r'A\|B', r'A\\|B', 'A|B'])
def test_caption_cells_round_trip_literal_backslashes_and_pipes(name):
    source = table(caption() + row(1).replace('Person 1', name) + row(2))
    report = result(source)
    assert report['composite_acceptance_pass']
    assert report['composite_group_results'][0]['records'][0]['name'] == name


@pytest.mark.parametrize('name', ['A & B', '<value>', 'A|B', r'A\|B'])
@pytest.mark.parametrize('normalized', [False, True])
def test_html_table_literal_values_survive_expansion(name, normalized):
    from html import escape
    value = escape(name)
    source = (f'<table><tr><th>ID</th><th>Name</th><th>Country</th></tr>'
              f'<tr><td>1</td><td>{value}</td><td>Argentina</td></tr>'
              '<tr><td>2</td><td>Two</td><td>Brazil</td></tr></table>' if normalized
              else table(caption() + row(1).replace('Person 1', value) + row(2)))
    report = result(source)
    assert report['composite_acceptance_pass']
    assert report['composite_group_results'][0]['records'][0]['name'] == name


@pytest.mark.parametrize('gap', ['\n', '\r\n', '\t'])
def test_html_caption_cells_normalize_embedded_whitespace(gap):
    report = result(table(caption() + row(1).replace('Person 1', 'Person' + gap + 'One') + row(2)))
    assert report['composite_acceptance_pass']
    assert report['composite_group_results'][0]['records'][0]['name'] == 'Person One'


def test_multiple_caption_placeholders_do_not_overlap():
    rules = contract(); rules['groups'][0]['minimum_records'] = 22
    source = ''.join(table(caption() + row(2*i+1) + row(2*i+2)) for i in range(11))
    report = result(source, rules)
    assert report['composite_acceptance_pass']
    assert len(report['composite_group_results'][0]['records']) == 22
    assert not result(source.replace(row(22), ''), rules)['composite_acceptance_pass']


@pytest.mark.parametrize('gap', [' ', '\n', '\r\n', '\t'])
def test_html_caption_normalizes_internal_whitespace(gap):
    report = result(table(caption('United' + gap + 'States') + row(1) + row(2)))
    assert report['composite_acceptance_pass']
    assert {r['country'] for r in report['composite_group_results'][0]['records']} == {'United States'}


@pytest.mark.parametrize('captured', [False, True])
def test_optional_caption_capture_fails_without_value(captured):
    rules = contract()
    rules['groups'][0]['group_caption']['pattern'] = r'(?P<value>Argentina)?y'
    validate_composite_acceptance(rules)
    source = table('<tr class="caption"><td>' + ('Argentinay' if captured else 'y') + '</td></tr>' + row(1) + row(2))
    assert result(source, rules)['composite_acceptance_pass'] is captured


@pytest.mark.parametrize('depth', [1, 2])
def test_selected_nested_table_retains_its_own_caption(depth):
    inner = table(caption() + row(1) + row(2))
    for _ in range(depth):
        inner = table('<tr><td>' + inner + '</td></tr>')
    assert result(inner)['composite_acceptance_pass']
    assert not result(inner.replace(caption(), ''))['composite_acceptance_pass']
    assert not result(table(caption() + '<tr><td>' + table(row(1) + row(2)) + '</td></tr>'))['composite_acceptance_pass']
